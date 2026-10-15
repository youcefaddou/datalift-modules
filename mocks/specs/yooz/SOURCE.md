# Source de la spécification

- Éditeur : Yooz
- Format : collection Postman v2.1 (`yooz_rising_public_api.postman_collection.json`, « Yooz Rising Public API », 222 requêtes, préfixe `yooz/v2/api`, OAuth2)
- Lien vers la documentation officielle : [à compléter] (collection fournie par Youcef Addou)
- Date de récupération : 2026-10-14
- Conditions d'utilisation vérifiées : [à vérifier]
- Jetons et identifiants retirés de la collection : oui, vérifié le 2026-10-15 (auth OAuth2 avec seulement l'URL du jeton et le type de grant, aucun jeton, JWT ni email en clair)

## Périmètre utile (flux 1 : factures fournisseurs vers IFS)

- Exports des factures traitées : `exportResults`, `exportResults/{generatedFileId}`, `dataReports`.
- Référentiels à rapprocher d'IFS : `YZ_SUPPLIER`, `YZ_CURRENCY`, `YZ_TAX_PROFILE`, `YZ_ACCOUNT`, `YZ_PAYMENT_METHOD`, `YZ_INVOICE_CATEGORY` (`/referentials/{referentialCode}`).
- Organisation : `orgUnits`, `users`, `userGroups`, `dimensionSets` (axes analytiques).
