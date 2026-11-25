# ADR-008 — LLM : OpenRouter remplace le Space Hugging Face

- **Statut :** adoptée (remplace l'ADR-006)
- **Date :** 2026-11-25
- **Auteur :** Youcef Addou

## Contexte

L'ADR-006 a retenu des modèles open source (Qwen) servis par un Space Hugging Face de l'organisation Ynov, sur ZeroGPU. Les tâches IA du M1 restent les mêmes : comprendre une demande en langage naturel, proposer les correspondances de champs et les transformations, répondre aux questions en SQL en lecture seule sur gold.

Ce qui a changé depuis :

- Le VPS retenu est un Hetzner CPX12 (2 vCPU, 2 Go de RAM, sans GPU). Il ne peut faire tourner aucun modèle : l'IA doit être appelée à distance.
- Le Space est un composant de plus à déployer et à maintenir (story prévue au Sprint 3), avec un quota par compte, une file d'attente et un démarrage à froid.
- Il reste 6 journées de production. Le temps passé sur l'infrastructure de l'IA est pris sur les connecteurs et les pipelines.

Contraintes :

- Budget : l'ADR-006 fixait 0 €. Cette ADR propose une seule dépense, d'environ 10 $.
- Données synthétiques uniquement (règle 1).
- Démos fiables aux oraux.
- Aucun secret dans le code ni dans la CI.

## Options étudiées

| Option | Coût | Effort sur 6 journées | Fiabilité en démo | Confidentialité |
| --- | --- | --- | --- | --- |
| 1. Garder le Space Hugging Face (ADR-006) | 0 € | Moyen : Space à développer, à déployer et à maintenir | Démarrage à froid et file d'attente, sauf avec le GPU dédié Ynov | Reste dans l'organisation Ynov |
| 2. OpenRouter, modèles gratuits uniquement | 0 € | Faible : une API compatible OpenAI, rien à héberger | Quota bas (environ 50 requêtes par jour, à vérifier) : risque de blocage en développement ou en démo | Certains fournisseurs gratuits peuvent conserver les requêtes |
| 3. OpenRouter, modèles gratuits + achat unique d'environ 10 $ de crédit | Environ 10 $, une seule fois | Faible : identique à l'option 2 | Quota relevé (environ 1 000 requêtes par jour, à vérifier), et un modèle payant peu cher possible en secours | Identique à l'option 2 |

**Option 1**
- Avantages : 0 €, chaîne 100 % open source, données qui restent dans l'organisation Ynov, et un même outil pour le fine-tuning du M2.
- Inconvénients : un composant de plus à construire alors qu'il reste peu de journées, un quota de 40 min/jour par compte, une file d'attente, et une dépendance à la licence Ynov.

**Option 2**
- Avantages : 0 €, rien à héberger, de nombreux modèles (dont les familles open source) accessibles avec une seule clé, et une API compatible OpenAI.
- Inconvénients : un quota quotidien trop bas pour une équipe de plusieurs membres, des modèles gratuits qui peuvent disparaître ou être saturés, et aucun recours le jour d'un oral.

**Option 3**
- Avantages : les mêmes que l'option 2, avec un quota suffisant pour l'équipe et un secours payant pour les oraux, pour un coût faible et borné.
- Inconvénients : on sort du « 0 € » de l'ADR-006, et le M2 dépend d'un service commercial. Les limites exactes des offres sont à confirmer sur le site d'OpenRouter au moment de l'achat.

## Décision

Option 3.

- **Fournisseur** : OpenRouter, appelé par son API compatible OpenAI.
- **Modèles** : les modèles gratuits (suffixe `:free`) par défaut, de préférence open source (par exemple de la famille Qwen) pour garder les prompts transposables en local. Le modèle utilisé pour chaque tâche se choisit par configuration et par mesure sur le jeu de référence (au moins 80 % de correspondances correctes), sans nouvelle ADR.
- **Secours** : un modèle payant peu cher, réservé aux oraux et aux cas où les modèles gratuits sont saturés.
- **Interface unique** : un seul client compatible OpenAI. On passe d'OpenRouter à un serveur local (Ollama ou llama.cpp, pour les postes équipés d'un GPU) en changeant seulement l'adresse et le modèle dans la configuration. Le client Gradio de l'ADR-006 n'est plus nécessaire.
- **Règles reprises de l'ADR-006** : chaque sortie est validée par un schéma Pydantic, une sortie invalide est retentée une fois puis signalée à l'humain, la température est fixée à 0, et la validation humaine (ADR-003) ne change pas.
- **Budget** : un achat unique d'environ 10 $. Toute autre dépense demande une nouvelle décision du chef de projet. Une limite de dépense est fixée sur la clé dans OpenRouter.
- **Économies de quota** : cache des réponses en développement, traitements par lots, aucun appel de modèle dans la CI (réponses enregistrées), réponses de démo enregistrées pour pouvoir rejouer la démo sans réseau.
- **Données et secrets** : uniquement des données synthétiques sont envoyées. La clé OpenRouter reste dans le `.env` (`OPENROUTER_API_KEY`) et dans les secrets du VPS. La CI n'en a pas besoin.

## Conséquences

Positives :

- Plus aucun composant d'IA à héberger : le VPS de 2 Go se contente d'appels HTTP.
- La story « déployer le Space » (Sprint 3) disparaît, et ce temps revient aux connecteurs et aux pipelines.
- Changer de modèle se fait en une ligne de configuration, avec un large choix de modèles.
- Démos plus fiables grâce au secours payant et aux réponses enregistrées.

Négatives :

- Une dépense d'environ 10 $, alors que l'ADR-006 fixait 0 €.
- Les requêtes passent par un service tiers, et certains fournisseurs gratuits peuvent les conserver. C'est acceptable seulement parce que les données sont synthétiques. Avant tout usage de données réelles, une nouvelle ADR est nécessaire.
- Les modèles gratuits peuvent changer, disparaître ou être saturés sans préavis.
- Le fine-tuning du M2 n'est pas couvert : OpenRouter ne sert pas nos propres modèles. Il faudra une ADR au M2 (GPU Ynov ou Hugging Face pour l'entraînement et le service).

À mettre en place :

- Passer l'ADR-006 au statut « remplacée par ADR-008 ».
- Créer un compte OpenRouter, acheter le crédit, créer une clé avec une limite de dépense.
- `.env.example` : `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, le modèle par tâche, l'adresse du serveur local. Retirer les variables Hugging Face.
- Mettre à jour `AGENTS.md` (stack), `docs/ARCHITECTURE.md`, `docs/ONBOARDING.md`, `docs/vulgarisation.md` et `docs/GLOSSARY.md`.
- Jira : supprimer ou adapter la story du Space. La tâche de veille sur les modèles devient « veille sur les modèles disponibles sur OpenRouter ».

À surveiller : le crédit restant, les limites de requêtes, les temps de réponse, et la disponibilité des modèles gratuits retenus.
