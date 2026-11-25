# Contrats communs DataLift — v1

Version du schéma : **1.0.0**. Implémentation : Pydantic v2, dans `contracts/v1/`.
Les imports publics sont réexportés depuis `contracts` : `from contracts import Supplier`.

Les modèles sont des objets de la couche silver. Les noms Python sont en `snake_case` ; les
alias de champs source permettent de valider les payloads en conservant les noms de l'API.
`model_dump(by_alias=True)` restitue les noms source. Les champs non déclarés sont refusés.

## Identité et lignage

Tous les objets héritent de `CommonModel` et portent :

| Champ | Règle | Source |
|---|---|---|
| `datalift_id` | Identifiant DataLift stable, obligatoire ; ne pas le régénérer à chaque extraction | ADR-005 ; résolution via `silver_identity_map` |
| `source_system` | Logiciel source | `docs/CONVENTIONS.md` |
| `source_id` | Identifiant du record source | `docs/CONVENTIONS.md` |
| `extracted_at` | Horodatage d'extraction UTC, date ISO 8601 | `docs/CONVENTIONS.md` |

Le contrat ne fabrique pas automatiquement `datalift_id` : la résolution des identités est
responsabilité de la table `silver_identity_map` et de DL-113.

## Modèles et champs

Tous les champs métier sont optionnels sauf les identifiants source clés et les liens requis
indiqués ci-dessous. Les alias correspondent aux noms des ressources décrites dans les specs
et aux fixtures de mocks existantes.

| Modèle | Champs métier (nom Python → alias source) | Source |
|---|---|---|
| `Supplier` | `supplier_id` → `SupplierId`; `name` → `Name`; `country` → `Country`; `default_language` → `DefaultLanguage` | IFS `SupplierInfoGeneralSet` : collection et clé confirmées dans `mocks/specs/ifs/SOURCE.md`; champs non clés présents dans `mocks/ifs/seed.json` (mock/reconstitution) |
| `PurchaseOrder` | `order_no` → `OrderNo`; `vendor_no` → `VendorNo`; `order_date` → `OrderDate`; `objstate` → `Objstate`; `contract` → `Contract`; `buyer_code` → `BuyerCode`; `authorize_code` → `AuthorizeCode`; `currency_code` → `CurrencyCode`; `company` → `Company` | IFS `PurchaseOrderSet`, champs listés dans `mocks/specs/ifs/SOURCE.md` |
| `SupplierInvoice` | `company` → `Company`; `invoice_id` → `InvoiceId`; `identity` → `Identity`; `invoice_no` → `InvoiceNo`; `invoice_date` → `InvoiceDate`; `currency` → `Currency`; `due_date` → `DueDate`; montants `NetCurrAmount`, `VatCurrAmount`, `GrossCurrAmount`; `objstate` → `Objstate` | IFS `ManSuppInvoiceSet`; champs d'en-tête décrits dans `mocks/specs/ifs/SOURCE.md` et fixtures `mocks/ifs/seed.json` |
| `InvoiceLine` | `item_id` → `ItemId`; `description` → `Description`; `net_curr_amount` → `NetCurrAmount`; `vat_code` → `VatCode` | Navigation `ManSuppInvoiceItems` et fixture `mocks/ifs/seed.json` |
| `Employee` | Lucca `id`, `remoteId`, `employeeNumber`, `givenName`, `familyName`, `email`, `phoneNumber`, `status`; IFS `CompanyId`, `EmpNo`, `PersonId`, `DateOfEmployment` | OpenAPI Lucca `employee` ; IFS `CompanyPersonSet` décrit dans `mocks/specs/ifs/SOURCE.md` |
| `Project` | `work_effort_id` → `workEffortId`; `work_effort_type_id` → `workEffortTypeId`; `work_effort_parent_id` → `workEffortParentId`; `work_effort_name` → `workEffortName`; `current_status_id` → `currentStatusId`; `reference` → `reference` | Modèle OFBiz `WorkEffort` dans `mocks/specs/progessi/SOURCE.md`; `reference` présent dans `mocks/progessi/seed.json` |
| `TimeEntry` | `time_entry_id` → `timeEntryId`; `timesheet_id` → `timesheetId`; `party_id` → `partyId`; `work_effort_id` → `workEffortId`; `from_date` → `fromDate`; `thru_date` → `thruDate`; `hours` → `hours` | Modèle OFBiz `TimeEntry` et mock Progessi, décrits dans `mocks/specs/progessi/SOURCE.md` et `mocks/progessi/app.py` |

Les champs de montants et d'heures utilisent `Decimal`, conformément aux conventions. Les dates
sont `date` ou `datetime` selon la précision de la source. Les propriétés de chaque champ
contiennent également une annotation `source` dans le JSON Schema généré. Le schéma complet
versionné est fourni dans `contracts/v1/schema.json` et peut être régénéré avec
`python -m contracts.v1.generate_schema`.

## Liens déclarés (ADR-005)

| Lien | Champ de contrat | Cardinalité | Obligatoire |
|---|---|---|---|
| `supplier` | `PurchaseOrder.supplier_datalift_id` | N:1 | oui |
| `supplier` | `SupplierInvoice.supplier_datalift_id` | N:1 | oui |
| `purchase_order` | `SupplierInvoice.purchase_order_datalift_id` | N:1 | non |
| `lines` | `SupplierInvoice.lines` / `InvoiceLine.supplier_invoice_datalift_id` | 1:N | collection vide autorisée au niveau du contrat |
| `employee` | `TimeEntry.employee_datalift_id` | N:1 | oui |
| `project` | `TimeEntry.project_datalift_id` | N:1 | oui |

Les champs `*_datalift_id` sont des références vers les identifiants stables DataLift, pas vers
les identifiants natifs des logiciels. Les actions et la table `silver_identity_map` relèvent
également de l'ADR-005 et du ticket DL-113 ; elles ne sont pas exécutées par ces modèles.

## Limites de la v1 et provenance à confirmer

Les specs IFS sont partiellement reconstituées. `mocks/specs/ifs/SOURCE.md` précise que les
champs autres que les clés de `SupplierInfoGeneralSet`, les champs obligatoires de facture et
plusieurs champs employés/projets ne sont pas tous reproduits/confirmés. Les champs supplémentaires
présents dans les fixtures IFS sont conservés pour compatibilité avec les mocks et sont signalés
comme tels ci-dessus ; ils devront être confirmés sur une projection IFS réelle avant d'être
considérés comme un contrat d'intégration certifié.

Yooz fournit le flux d'export de facture, mais le contenu du fichier exporté n'est pas décrit
par une structure de champs dans la collection Postman déposée. La v1 n'invente donc pas de
champs Yooz spécifiques. Le mapping Yooz → contrat doit être documenté quand le format d'export
est confirmé.

## Validation

```bash
uv run pytest tests/contract/contracts -q
uv run ruff check contracts tests/contract/contracts
uv run ruff format --check contracts tests/contract/contracts
```

## Interface connecteur (DL-36, ADR-004)

`contracts/connector.py` définit la classe abstraite `Connector`, que chaque connecteur de `connectors/<logiciel>/` implémente :

| Opération | Rôle |
|---|---|
| `read_page(object_type, cursor, page_size)` | Lit une page ; `next_cursor` vaut `None` sur la dernière |
| `read(object_type)` | Lit tout, page après page (déjà implémentée à partir de `read_page`) |
| `write(object_type, records)` | Écrit et renvoie les identifiants acceptés et rejetés ; doit être idempotente (règle 5) |
| `describe_schema(object_type)` | Schéma JSON des enregistrements bruts de l'API |
| `health_check()` | Vérifie que l'API répond avec les identifiants actuels |

Les enregistrements sont bruts (noms de champs de l'API) : ils vont en bronze, et le passage au modèle commun se fait dans `pipelines/`. Les erreurs héritent de `ConnectorError` ; `retryable` indique si un nouvel essai peut réussir (`RateLimitError`, `SourceUnavailableError`).

Chaque connecteur appelle `assert_connector_contract` (`contracts/connector_contract.py`) dans ses tests : santé, schéma, écriture, pagination, et absence de doublon quand on rejoue une écriture. Exemple avec un connecteur factice : `tests/contract/test_connector_interface.py`.

## Ontologie : liens, actions, identités (DL-113, ADR-005)

`contracts/v1/ontology.py` :

- `LINKS` : les 6 liens (nom, objet source, objet cible, cardinalité, obligatoire, colonne de clé étrangère, champs des specs qui servent au rapprochement).
- `ACTIONS` : `send_invoice_to_ifs`, `sync_employee_to_ifs` et `send_time_entry_to_ifs`. `action.failed(objet, contexte)` renvoie les préconditions non respectées, qui servent de motif pour mettre l'objet de côté. Le contexte (`ActionContext`) apporte ce que l'objet ne contient pas : statuts validés dans la source, montants des commandes, table d'identités.
- `SILVER_IDENTITY_MAP_DDL` et `IdentityMap` : la table `silver_identity_map`. Un enregistrement source correspond à un seul `datalift_id`.
- `FlowDefinition` : un flux référence une action connue, sur le bon type d'objet, et n'est exécutable qu'une fois `validated` (règle 4).
