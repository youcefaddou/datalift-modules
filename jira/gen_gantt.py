"""Gantt du M1 (épopées + sprints + journées Ydays) en PNG.

Usage : uv run --with matplotlib python jira/gen_gantt.py
"""
import contextlib
import io
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    from gen_backlog import EPICS  # même source que le backlog Jira

# Couleurs du logo DataLift : bleu nuit, indigo, bleu, cyan (pas d'orange)
SURFACE, INK, INK2, GRID, BAR, OPT = "#ffffff", "#1a1d3a", "#5a5d72", "#dfe3ee", "#2b6fd6", "#b9bfd0"
BAND, MILESTONE = "#eef3fb", "#3a36c0"
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
D = date.fromisoformat

SPRINTS = [("S0", "2026-10-14", "2026-11-25"), ("S1", "2026-11-26", "2026-12-16"),
           ("S2", "2026-12-17", "2027-01-21"), ("S3", "2027-01-22", "2027-03-03"),
           ("S4", "2027-03-04", "2027-03-24"), ("S5", "2027-03-25", "2027-04-14"),
           ("S6", "2027-04-15", "2027-05-05"), ("S7", "2027-05-06", "2027-05-27")]
YDAYS = ["2026-10-14", "2026-11-25", "2026-12-16", "2027-01-20", "2027-01-21", "2027-03-03",
         "2027-03-24", "2027-04-14", "2027-05-05", "2027-05-26", "2027-05-27"]
MILESTONES = {"2026-12-16": "Oral de validation", "2027-05-27": "Oral final"}

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": INK})
fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=150)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

n = len(EPICS)
x0, x1 = D("2026-10-10"), D("2027-06-02")

# Bandes de sprint alternées + libellé en haut
for i, (name, s, e) in enumerate(SPRINTS):
    if i % 2 == 0:
        ax.axvspan(D(s), D(e) + timedelta(days=1), color=BAND, zorder=0, lw=0)
    mid = D(s) + (D(e) - D(s)) / 2
    ax.text(mid, -1.15, name, ha="center", va="center", fontsize=10, color=INK2, fontweight="bold")

# Journées Ydays : filets verticaux numérotés
for k, d in enumerate(YDAYS, start=1):
    ax.axvline(D(d), color=GRID, lw=1, zorder=1)
for k, d in enumerate(YDAYS, start=1):
    if k in (5, 11):  # journées consécutives : une seule étiquette
        continue
    label = {4: "Y4-5", 10: "Y10-11"}.get(k, f"Y{k}")
    ax.text(D(d), n - 0.35, label, ha="center", va="bottom", fontsize=8.5, color=INK2)

# Barres d'épopées
for row, (_, name, start, due) in enumerate(EPICS):
    s, e = D(start), D(due) + timedelta(days=1)
    ax.barh(row, (e - s).days, left=s, height=0.62, lw=0, zorder=3, color=OPT if "optionnel" in name else BAR)

# Jalons
for d, label in MILESTONES.items():
    final = label == "Oral final"
    ax.axvline(D(d), color=MILESTONE, lw=1.5, ls=(0, (4, 3)), zorder=4)
    ax.plot([D(d)], [-0.62], marker="D", ms=9, color=MILESTONE, zorder=5, clip_on=False)
    ax.text(D(d) + timedelta(days=-3 if final else 3), -0.62, f"{label}\n{D(d):%d/%m/%Y}", va="center",
            ha="right" if final else "left", fontsize=9.5, fontweight="bold", color=MILESTONE,
            bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5), zorder=6)

ax.set_yticks(range(n), [name for _, name, _, _ in EPICS])
ax.set_ylim(n - 0.4, -1.6)
ax.set_xlim(x0, x1)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{MOIS[mdates.num2date(v).month - 1]} {mdates.num2date(v).year}"))
ax.tick_params(axis="both", length=0, colors=INK2)
ax.tick_params(axis="y", colors=INK, labelsize=10.5)
for s in ax.spines.values():
    s.set_visible(False)

fig.suptitle("DataLift — Planning du M1", x=0.012, ha="left", fontsize=17, fontweight="bold", color=INK)
fig.text(0.012, 0.915, "13 épopées, 8 sprints calés sur les journées Ydays (Y1 à Y11). Barre grise : épopée optionnelle.",
         fontsize=10.5, color=INK2)
fig.tight_layout(rect=(0, 0, 1, 0.9))

out = Path(__file__).resolve().parents[1] / "docs" / "assets" / "gantt_datalift_m1.png"
fig.savefig(out, facecolor=SURFACE)
print(out)
