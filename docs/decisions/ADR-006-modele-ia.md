# ADR-006 — Modèle IA : open source sur un Space Hugging Face, budget 0 €

- **Statut :** remplacée par ADR-008
- **Date :** 2026-10-14
- **Auteur :** Youcef Addou

## Contexte

Tâches IA du M1 :

- comprendre une demande en langage naturel et produire une définition de flux ;
- proposer les correspondances de champs avec un score de confiance, et les expliquer ;
- proposer les transformations (formats, dates, codes) ;
- répondre aux questions transverses, en SQL en lecture seule sur gold (ADR-005).

En M2 s'ajoutent un modèle de correspondance spécialisé (fine-tuning) et des agents.

Contraintes :

- budget : 0 € ;
- données synthétiques uniquement (règle 1) ;
- démos fiables aux oraux ;
- 6 journées de production : pas d'infrastructure lourde à maintenir ;
- VPS sans GPU.

Ressources disponibles :

- licence Academia Hub de chaque membre via l'organisation Ynov sur Hugging Face : ZeroGPU 40 min/jour par compte (GPU de 48 Go par appel), Spaces et dépôts privés ;
- GPU dédiés de l'organisation Ynov (L40, A100, H200), dont l'usage pour ce projet est accordé ;
- un poste avec un GPU de 8 Go peut faire tourner un modèle d'environ 9 milliards de paramètres quantifié en 4 bits.

À noter : les abonnements Claude ou Google AI couvrent l'usage des assistants, pas l'API. Une API commerciale serait donc facturée à part.

Cette ADR traite le ticket « ADR : modèle IA (API ou local) et budget ».

## Options étudiées

| Option | Modèles | Coût | Confidentialité | Effort sur 6 journées |
| --- | --- | --- | --- | --- |
| 1. API Claude | Modèles de pointe | Payant à l'usage : incompatible avec 0 € | Données chez Anthropic | Faible |
| 2. API Gemini, offre gratuite | Modèles Flash | Gratuit, débit limité | Données réutilisables par Google | Faible |
| 3. Modèle local seul (postes ou VPS) | 9 milliards de paramètres au plus sur un GPU de 8 Go, lent sur CPU | 0 €, ou VPS plus cher | Aucune sortie | Élevé : postes hétérogènes, pas de GPU sur le VPS |
| 4. Open source sur un Space Hugging Face, local en développement | 27 à 36 milliards de paramètres | 0 € (licence Ynov) | Reste dans l'organisation Ynov | Moyen |

## Décision

Option 4.

**Modèles candidats.** Classements officiels Hugging Face, octobre 2026. Le choix final se fait par mesure sur le jeu de référence.

| Modèle | Taille | Licence | Points forts | Usage |
| --- | --- | --- | --- | --- |
| `Qwen/Qwen3.6-35B-A3B` | 36 Md, dont 3 Md actifs | Apache 2.0 | Extraction structurée (ExtractBench 88,1). Rapide, donc peu de quota consommé par appel | Space, par défaut (version FP8) |
| `Qwen/Qwen3.8-27B` | 28 Md | Apache 2.0 | Meilleurs scores (ExtractBench 89,8, GPQA 89,2), plus lent | Space, à comparer (version FP8) |
| `Qwen/Qwen3.5-9B` | 10 Md | Apache 2.0 | Environ 6 Go en 4 bits : tient dans un GPU de 8 Go | Poste local, développement |

**Rôles.**

- **Space Hugging Face** : Space privé dans l'organisation Ynov, sur ZeroGPU. C'est le moteur principal. DataLift (sur le VPS) et chaque membre l'appellent avec leur propre jeton, sur le quota de 40 min/jour par compte.
- **Poste local avec GPU** : développement et tests sans consommer le quota, avec un serveur local compatible OpenAI (Ollama ou llama.cpp). On garde la même famille de modèles (Qwen) que sur le Space, pour que les prompts se transposent.
- **Embeddings** (similarité entre champs) : petit modèle open source multilingue, sur CPU ou GPU local.
- **Oraux** : le Space passe sur un GPU dédié de l'organisation Ynov (pas de quota, pas de file d'attente). Les réponses de démo sont enregistrées pour pouvoir la rejouer sans réseau.
- **Entraînement (M2)** : fine-tuning du modèle de correspondance sur les GPU dédiés de l'organisation Ynov, avec Colab ou Kaggle en secours. Le modèle et les jeux de données sont stockés dans des dépôts privés de l'organisation, puis le modèle est servi par le Space.

**Interface unique.** Le code de l'agent IA appelle une seule interface. Deux implémentations : le Space (client Gradio) et le serveur local (API compatible OpenAI). Le moteur se choisit par configuration. Chaque sortie est validée par un schéma Pydantic. Une sortie invalide est retentée une fois, puis signalée à l'humain. La température est fixée à 0. La validation humaine (ADR-003) ne change pas.

**Mesure.** Le jeu de référence (au moins 80 % de correspondances correctes) compare les modèles candidats : précision, temps de réponse, secondes de GPU par appel. Changer de modèle se fait par configuration, sans nouvelle ADR.

**Veille sur les modèles open source.** Les modèles open source évoluent en quelques semaines. Objectif : disposer en permanence des meilleurs et des plus récents.

- Fréquence : une fois par sprint, avec une tâche Jira dédiée.
- Sources : classements officiels Hugging Face (extraction structurée, respect des consignes, raisonnement, agents), fiches des modèles, annonces des éditeurs.
- Critères pour qu'un modèle soit testé : licence open source permissive (Apache 2.0, MIT…). Tient sur le GPU du Space (48 Go, en FP8 si besoin). Pour le local, une version de la même famille qui tient dans 8 Go en 4 bits.
- Adoption : le modèle est mesuré sur le jeu de référence. Il remplace le modèle en place seulement s'il fait mieux à vitesse comparable. Le changement passe par une PR de configuration qui indique les mesures, et le résultat de la veille est noté dans le ticket Jira.
- La recherche peut être automatisée : un script interroge l'API des classements officiels de Hugging Face et liste les modèles qui respectent les critères.

**Budget.**

- Plafond : 0 €. Toute dépense demande une nouvelle décision du chef de projet.
- Économies de quota : cache des réponses en développement, traitements par lots, aucun appel de modèle dans la CI (réponses enregistrées), appel de préchauffage avant une démo.

**Données et secrets.**

- Seules des données synthétiques sont envoyées aux modèles.
- Sur Hugging Face, tout reste privé dans l'organisation Ynov : ce qui est publié y est public par défaut.
- Le jeton Hugging Face de chaque membre reste dans son `.env`. La CI n'a besoin d'aucun jeton.

## Conséquences

Positives :

- Coût nul, et une chaîne 100 % open source, des modèles jusqu'à l'hébergement.
- Chaque membre est autonome, avec son propre quota.
- Même famille de modèles en local et sur le Space.
- Le M2 est préparé : entraînement, stockage et service du modèle spécialisé au même endroit.
- Grâce à la veille, le projet suit les derniers modèles open source sans changer d'architecture.

Négatives :

- Qualité inférieure aux meilleures API sur les tâches les plus difficiles. C'est limité par l'ontologie (l'IA choisit parmi des objets et des actions connus), la validation Pydantic et la validation humaine.
- Quota par compte, file d'attente et démarrage à froid du Space : d'où le préchauffage, le GPU dédié pour les oraux et les réponses de démo enregistrées.
- Un composant de plus à maintenir : le Space.
- Dépendance à la licence Ynov, dont la durée est à vérifier pour le M2 (2027-2028).

À mettre en place :

- Onboarding : chaque membre rejoint l'organisation Ynov sur Hugging Face et crée un jeton personnel.
- Variables d'environnement à ajouter : jeton Hugging Face, identifiant du Space, adresse du serveur local, modèle par tâche.
- Story à créer : déployer le Space dans l'organisation Ynov (Sprint 3, avec le socle de l'agent IA).
- Tâche Jira récurrente : veille sur les modèles open source, une par sprint.

À surveiller : la consommation de quota, les temps de réponse, la durée de la licence. Avant tout usage de données réelles, une nouvelle ADR est nécessaire.
