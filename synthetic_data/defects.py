"""Known defects injected into synthetic data, with their ground truth.

Catalog and rules: synthetic_data/DEFECTS.md.

The injector is format-agnostic: records are plain dicts and field names are
passed by the caller, so it works on any source format (Yooz, Lucca, Progessi...).
Each record receives at most one defect, so the ground truth stays unambiguous.
"""

import copy
import json
import random
from collections.abc import Callable
from dataclasses import asdict, dataclass
from decimal import Decimal
from enum import StrEnum
from pathlib import Path
from typing import Any

Record = dict[str, Any]

DEFAULT_RATE = 0.05
HOURS_LIMITS = (Decimal(0), Decimal(24))


class DefectType(StrEnum):
    """The 7 defect types"""

    DUPLICATE = "DUPLICATE"
    AMOUNT_MISMATCH = "AMOUNT_MISMATCH"
    INVOICE_WITHOUT_PO = "INVOICE_WITHOUT_PO"
    UNKNOWN_SUPPLIER = "UNKNOWN_SUPPLIER"
    UNKNOWN_EMPLOYEE = "UNKNOWN_EMPLOYEE"
    HOURS_OUT_OF_RANGE = "HOURS_OUT_OF_RANGE"
    MISSING_FIELD = "MISSING_FIELD"


@dataclass(frozen=True)
class Defect:
    """One injected defect: one line of the ground truth file."""

    defect_id: str
    defect_type: DefectType
    flow: int
    object: str
    record_id: str
    field: str | None
    original_value: Any
    injected_value: Any


class DefectInjector:
    """Injects defects reproducibly (fixed seed) and records the ground truth."""

    def __init__(self, seed: int) -> None:
        self.seed = seed
        # Own random generator: the same seed always picks the same records.
        self._rng = random.Random(seed)
        # (object, record id) already altered: a record never receives two defects.
        self._touched: set[tuple[str, str]] = set()
        # The ground truth, in injection order.
        self.defects: list[Defect] = []

    # One public method per defect type. Each returns a new list: the input is never modified.

    def duplicates(
        self,
        records: list[Record],
        *,
        flow: int,
        obj: str,
        id_field: str,
        rate: float = DEFAULT_RATE,
    ) -> list[Record]:
        """Append copies of some records with a new technical id and the same content."""
        result = copy.deepcopy(records)
        for record in self._pick(result, obj, id_field, rate):
            original_id = str(record[id_field])
            copy_id = f"{original_id}-DUP"
            result.append({**copy.deepcopy(record), id_field: copy_id})
            self._touched.add((obj, copy_id))
            self._record(DefectType.DUPLICATE, flow, obj, copy_id, id_field, original_id, copy_id)
        return result

    def amount_mismatches(
        self,
        records: list[Record],
        *,
        obj: str,
        id_field: str,
        amount_field: str,
        delta: Decimal = Decimal("10.00"),
        rate: float = DEFAULT_RATE,
    ) -> list[Record]:
        """Shift an amount (e.g. the total) so it no longer matches the other amounts (flow 1)."""

        def shifted(value: Any) -> Decimal:
            return Decimal(str(value)) + self._rng.choice((delta, -delta))

        return self._alter(
            records, DefectType.AMOUNT_MISMATCH, 1, obj, id_field, amount_field, rate, shifted
        )

    def invoices_without_po(
        self,
        records: list[Record],
        *,
        obj: str,
        id_field: str,
        po_field: str,
        rate: float = DEFAULT_RATE,
    ) -> list[Record]:
        """Remove the purchase order reference of some invoices (flow 1)."""
        return self._alter(
            records, DefectType.INVOICE_WITHOUT_PO, 1, obj, id_field, po_field, rate, lambda _: None
        )

    def unknown_suppliers(
        self,
        records: list[Record],
        *,
        obj: str,
        id_field: str,
        supplier_field: str,
        known_ids: set[str],
        rate: float = DEFAULT_RATE,
    ) -> list[Record]:
        """Point some invoices to a supplier absent from the supplier list (flow 1)."""
        unknown = self._unknown_id("UNKNOWN-SUPPLIER", known_ids)
        return self._alter(
            records, DefectType.UNKNOWN_SUPPLIER, 1, obj, id_field, supplier_field, rate, unknown
        )

    def unknown_employees(
        self,
        records: list[Record],
        *,
        obj: str,
        id_field: str,
        employee_field: str,
        known_ids: set[str],
        rate: float = DEFAULT_RATE,
    ) -> list[Record]:
        """Point some time entries to an employee absent from the employee list (flow 3)."""
        unknown = self._unknown_id("UNKNOWN-EMPLOYEE", known_ids)
        return self._alter(
            records, DefectType.UNKNOWN_EMPLOYEE, 3, obj, id_field, employee_field, rate, unknown
        )

    def hours_out_of_range(
        self,
        records: list[Record],
        *,
        obj: str,
        id_field: str,
        hours_field: str,
        rate: float = DEFAULT_RATE,
    ) -> list[Record]:
        """Set hours below 0 or above 24 on some time entries (flow 3)."""
        low, high = HOURS_LIMITS

        def out_of_range(_: Any) -> Decimal:
            return self._rng.choice((low - Decimal("1.5"), high + Decimal("1.5")))

        return self._alter(
            records,
            DefectType.HOURS_OUT_OF_RANGE,
            3,
            obj,
            id_field,
            hours_field,
            rate,
            out_of_range,
        )

    def missing_fields(
        self,
        records: list[Record],
        *,
        flow: int,
        obj: str,
        id_field: str,
        field: str,
        rate: float = DEFAULT_RATE,
    ) -> list[Record]:
        """Empty a mandatory field (set to None) on some records."""
        return self._alter(
            records, DefectType.MISSING_FIELD, flow, obj, id_field, field, rate, lambda _: None
        )

    # Ground truth.

    def ground_truth(self) -> dict[str, Any]:
        """Seed and list of injected defects, ready to be written as JSON."""
        return {"seed": self.seed, "defects": [asdict(d) for d in self.defects]}

    def write_ground_truth(self, path: Path) -> None:
        """Write the ground truth as JSON. Decimals are written as strings, never as floats."""
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(self.ground_truth(), indent=2, ensure_ascii=False, default=str)
        path.write_text(text + "\n", encoding="utf-8")

    # Internals.

    def _pick(
        self,
        records: list[Record],
        obj: str,
        id_field: str,
        rate: float,
        field: str | None = None,
    ) -> list[Record]:
        """Choose untouched records (with a value in `field`, if given) at the given rate."""
        candidates = [
            r
            for r in records
            if (obj, str(r[id_field])) not in self._touched
            and (field is None or r.get(field) is not None)
        ]
        if rate <= 0 or not candidates:
            return []
        # At least 1 record, so a small dataset still contains every requested defect.
        count = min(len(candidates), max(1, round(len(candidates) * rate)))
        chosen = self._rng.sample(candidates, count)
        self._touched.update((obj, str(r[id_field])) for r in chosen)
        return chosen

    def _alter(
        self,
        records: list[Record],
        defect_type: DefectType,
        flow: int,
        obj: str,
        id_field: str,
        field: str,
        rate: float,
        new_value: Callable[[Any], Any],
    ) -> list[Record]:
        """Replace `field` on the chosen records with `new_value(old value)` and record it."""
        # Work on a deep copy: the caller's data (the clean dataset) is never modified.
        result = copy.deepcopy(records)
        for record in self._pick(result, obj, id_field, rate, field):
            original = record[field]
            record[field] = new_value(original)
            self._record(
                defect_type, flow, obj, str(record[id_field]), field, original, record[field]
            )
        return result

    def _unknown_id(self, prefix: str, known_ids: set[str]) -> Callable[[Any], str]:
        """Build ids like UNKNOWN-SUPPLIER-0003 that are guaranteed absent from known_ids."""

        def generate(_: Any) -> str:
            number = len(self.defects) + 1
            while f"{prefix}-{number:04d}" in known_ids:
                number += 1
            return f"{prefix}-{number:04d}"

        return generate

    def _record(
        self,
        defect_type: DefectType,
        flow: int,
        obj: str,
        record_id: str,
        field: str | None,
        original: Any,
        injected: Any,
    ) -> None:
        """Add one line to the ground truth, numbered DEF-0001, DEF-0002... in order."""
        defect_id = f"DEF-{len(self.defects) + 1:04d}"
        self.defects.append(
            Defect(defect_id, defect_type, flow, obj, record_id, field, original, injected)
        )
