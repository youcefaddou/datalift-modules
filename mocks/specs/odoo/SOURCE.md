# Source de la spécification

- Éditeur : Odoo S.A. (Odoo Community, module Notes de frais `hr_expense`) ; remplace Notilus, voir `docs/decisions/ADR-007-odoo-remplace-notilus.md`
- Format : API externe officielle d'Odoo, documentée publiquement (pas de fichier OpenAPI : Odoo génère une documentation dynamique par instance)
- Lien vers la documentation officielle : https://www.odoo.com/documentation/19.0/developer/reference/external_api.html ; modèle : https://github.com/odoo/odoo/tree/master/addons/hr_expense (licence LGPL-3)
- Date de récupération : 2026-10-15
- Conditions d'utilisation vérifiées : oui, Odoo Community est sous LGPL-3 et s'auto-héberge gratuitement (l'accès à l'API sur Odoo Online, le SaaS, demande une offre payante : on ne l'utilise pas)
- Jetons et identifiants retirés de la collection : sans objet

## API (Odoo 19, « External JSON-2 API »)

- Requête : `POST /json/2/<modèle>/<méthode>` (exemple : `/json/2/hr.expense/search_read`).
- En-têtes : `Authorization: bearer <clé API>` (obligatoire), `Content-Type: application/json`, `X-Odoo-Database` (si plusieurs bases).
- Corps : objet JSON avec `ids`, `context` (optionnel) et les paramètres nommés de la méthode (`domain`, `fields`…). Pas d'arguments positionnels.
- Réponse : 200 et la valeur de retour en JSON ; erreur 4xx/5xx avec `name`, `message`, `arguments`, `context`, `debug` (exemple : 401 « Invalid apikey »).
- XML-RPC / JSON-RPC (`/xmlrpc`, `/xmlrpc/2`, `/jsonrpc`) : dépréciés, retirés dans Odoo 22 (automne 2028). On utilise JSON-2.

## Périmètre utile (flux M2 : notes de frais vers IFS)

Modèle `hr.expense` : `name`, `date`, `employee_id`, `product_id` (catégorie de dépense), `quantity`, `price_unit`, `total_amount`, `tax_amount`, `untaxed_amount`, `currency_id`, `payment_mode` (`own_account` / `company_account`), `attachment_ids`, `state` (`draft` → `submitted` → `approved` → `posted` → `paid`, ou `refused`). Plus `hr.employee` pour rattacher les collaborateurs.

## Mise en œuvre prévue

Odoo Community lancé en Docker à côté des autres mocks, avec des données fictives (règle 1) : le connecteur parle à un vrai Odoo, sans spec à reconstituer.
