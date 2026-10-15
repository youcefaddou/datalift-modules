# Source de la spécification

- Éditeur : IFS
- Format : **reconstitué** (aucune spec OpenAPI publique : IFS la génère par projection depuis une instance, via API Explorer ou `{Projection}.svc/$openapi`)
- Lien vers la documentation officielle : aucune doc publique des projections
- Date de récupération : 2026-10-15
- Conditions d'utilisation vérifiées : sans objet (seuls des faits techniques sont repris, aucun fichier copié ; les transcriptions de vidéos restent hors dépôt)
- Jetons et identifiants retirés de la collection : sans objet

## Sources

| Réf. | Source | Apport |
|---|---|---|
| V1 | Vidéo Marcel Ausan, [Using REST API in IFS Cloud (TECH 21)](https://www.youtube.com/watch?v=3AqWHqz-8hc) | architecture (pages → projections → PL/SQL), convention `<Page>Handling`, `CustomerHandling` et ses collections, règles de `POST` (201, identifiant auto-généré, message « Field … is mandatory and requires a value », doublon refusé), client IAM + OAuth2 client credentials, jeton 1 h |
| V2 | Vidéo Marcel Ausan, [Procure to Pay (22)](https://www.youtube.com/watch?v=dKlte85tRaU) | flux facture : facture fournisseur manuelle « Preliminary Posted », rapprochement avec la réception de commande (« Match all »), puis comptabilisation |
| V3 | Vidéo Marcel Ausan, [User Management (TECH 13)](https://www.youtube.com/watch?v=MSHggCz7t78) | utilisateur → personne (`PersonId`) → employé |
| G1 | [silverhouse3/ifs-cloud-powerbi-odata](https://github.com/silverhouse3/ifs-cloud-powerbi-odata) (vérifié par l'auteur sur IFS Cloud 25R1) | `PurchaseOrderHandling.svc/PurchaseOrderSet` et ses champs, `PurchaseOrderLineNopartSet`, `SuppliersHandling.svc/SupplierInfoGeneralSet`, `$orderby` supporté, `$expand` → `ODP_NOT_IMPLEMENTED`, document de service, jeton `/auth/realms/{realm}/protocol/openid-connect/token` |
| G2 | [knakit/ifs-mcp-server-local](https://github.com/knakit/ifs-mcp-server-local) | champs et types de `CustomerInfoSet`, filtre sur énumération `Champ eq IfsApp.<Projection>.<Type>'Valeur'` |
| F1 | [Forum IFS, facture manuelle](https://community.ifs.com/framework-experience-infrastructure-cloud-integration-dev-tools-50/bpa-to-create-a-manual-supplier-invoice-53162) | `ManSuppInvoiceSet`, clés, navigation `ManSuppInvoiceItems`, champs d'en-tête, `InvoiceId` attribué par IFS |
| F2 | [Forum IFS, nouvel employé](https://community.ifs.com/hcm-human-capital-management-payroll-38/new-employee-rest-api-52445) | `EmployeesHandling`, entité `CompanyPerson` |
| F3 | [Forum IFS, page Compensation](https://community.ifs.com/hcm-human-capital-management-payroll-38/compensation-page-does-not-load-data-mapping-error-due-to-type-mismatch-26505) | `CompanyPersonSet(CompanyId='…',EmpNo='…')` : clés des employés `CompanyId` + `EmpNo` ; `luname`, `keyref`, `Objgrants` sélectionnables ; filtres `ge` / `le` sur dates ; `$expand` utilisé sur les références `…Ref` |
| F4 | [Forum IFS, temps projet](https://community.ifs.com/hcm-human-capital-management-payroll-38/approval-of-project-time-by-project-manager-10715) | les transactions de projet sont « approuvées » (pas « autorisées ») |
| N1 | [Novacura, opération Update](https://docs.novacura.com/flow-ifs-cloud-development-guidelines/flow-development-with-odata/implementation/operation-specific-notes/update) | `PATCH` : `If-Match` obligatoire (`ODP_MISSING_PRECONDITION` sinon), ETag lu par un `GET` sur la clé, `*` désactive le contrôle |
| N2 | [Novacura, erreurs IFS](https://docs.novacura.com/flow-ifs-cloud-development-guidelines/flow-development-with-odata/implementation/response-status-handling/errors-from-ifs), [forum ODP_NOT_ALLOWED](https://community.ifs.com/framework-experience-infrastructure-cloud-integration-dev-tools-50/odp-not-allowed-illegal-operation-7200), [forum ODP_RESOURCE_NOTFOUND](https://community.ifs.com/framework-experience-infrastructure-cloud-integration-dev-tools-50/odata-get-returning-odp-resource-notfound-47810) | codes d'erreur (voir ci-dessous) |
| C1 | Captures de la vidéo V1 (envoyées par Youcef) | format d'une ligne (`@odata.etag` `W/"…"`, `luname`, `keyref` `CUSTOMER_ID=AUSAN^`, `Objgrants`), contexte `$metadata#CustomerInfoSet/$entity` sur 201, schéma complet de `CustomerInfo` (champs obligatoires, longueurs, énumérations `PartyType`, `CustomerCategory`, `IdentifierRefValidation`), erreur **500** `DATABASE_ERROR` + détail `ORA-20124: Error.NULLVALUE: Field [Name] is mandatory for Customer Info and requires a value.`, OpenID Connect (`/auth/realms/<realm>/.well-known/openid-configuration`), facture manuelle `InvoiceType` `SUPPINV`, série `SI`, statut « Prel Posted » |

## Collections

| Projection / collection | Vérifié | Reconstitué |
|---|---|---|
| `CustomerHandling` / `CustomerInfoSet` | tout ce qui est utilisé (V1, C1, G2, confirmé par Youcef) ; **ces règles (champs obligatoires, valeurs par défaut, énumérations) ne valent que pour `CustomerInfo`** | numéro ORA et texte exact de l'erreur de doublon |
| `PurchaseOrderHandling` / `PurchaseOrderSet` | collection, `OrderNo`, `VendorNo`, `OrderDate`, `Objstate`, `Contract`, `BuyerCode`, `AuthorizeCode`, `CurrencyCode`, `Company` (G1) | nom du type d'énumération `PurchaseOrderState` (suit la règle de G2) |
| `PurchaseOrderHandling` / `PurchaseOrderLineNopartSet` | collection et champs (G1) | clés `OrderNo` + `LineNo` + `ReleaseNo`, type `PurchaseOrderLineState` |
| `ManualSupplierInvoiceHandling` / `ManSuppInvoiceSet` | collection, clés, navigation, champs d'en-tête (F1), `InvoiceType` `SUPPINV`, `SeriesId` `SI` (C1) | champs obligatoires, valeur `PrelPosted` de `Objstate`, champs des lignes |
| `SuppliersHandling` / `SupplierInfoGeneralSet` | projection et collection (G1), clé `SupplierId` (Youcef) | autres champs |
| `PersonHandling` / `PersonInfoSet` | projection et collection (G1 et dépôts liés) | champs |
| `EmployeesHandling` / `CompanyPersonSet` | projection et entité (F2), collection `CompanyPersonSet` et clés `CompanyId` + `EmpNo` (F3, vues dans les projections `PersonnelFile…Handling`) | présence de la collection dans `EmployeesHandling`, champs obligatoires, `PersonId`, `DateOfEmployment` |
| `ProjectManagementHandling` / `ProjectSet` | projection (Youcef) | nom de la collection, champs |

## Codes d'erreur IFS

| Code | Quand | Statut HTTP |
|---|---|---|
| `DATABASE_ERROR` | erreur levée par la logique métier PL/SQL, détail `ORA-<n>: <LU>.<CODE>: <message>` (C1) | 500 (C1) |
| `ODP_RESOURCE_NOTFOUND` | lecture par une clé inexistante, ou droits insuffisants sur le site (N2) | 404 (reconstitué) |
| `ODP_NOT_ALLOWED` | opération interdite par le fournisseur OData (N2) | 405 (reconstitué) |
| `ODP_MISSING_PRECONDITION` | en-tête attendu absent, typiquement `If-Match` sur `PATCH` (N1, N2) | 428 (reconstitué) |
| `ODP_DESERIALIZATION_ERROR` | corps non JSON ou `Content-Type` absent, message `Error while de-serializing contents.` (N2) | 400 (reconstitué) |
| `ODP_NOT_IMPLEMENTED` | opération décrite dans la spec mais non implémentée, `$expand` sur certaines collections (G1, N2) | 400 (reconstitué) |
| `MI_MODIFIED_ERROR` | métadonnées de projection périmées après une mise à jour : réessayer la même requête (N2) | 500 (N2), non reproduit |

## Pas encore reproduit

- Projection des temps (flux 3) : `TimeCardHandling` = saisie des temps par l'employé lui-même (Youcef) ; saisie par le manager via une projection du type `TimeCardManagerHandling` (nom non confirmé, introuvable publiquement : à vérifier dans *Debug > Page Info*).
- Chemins `/int/ifsapplications/entity/v1/` (par exemple `PurchaseOrderLineEntity.svc/PurchaseOrderLineSet`, G1).
- Actions et fonctions OData (`FinishInvoice`, `DefaultCopy`), `DELETE`, `$count`, `$expand` sur les références `…Ref` (refusé par le mock avec `ODP_NOT_IMPLEMENTED`, comme G1 l'observe sur ses collections), opérateurs de filtre autres que `eq`.
