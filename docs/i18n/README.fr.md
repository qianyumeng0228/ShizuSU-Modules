# ShizuSU-Modules

[![État du build](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml/badge.svg)](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml)
[![Site web](https://img.shields.io/website?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules&label=Pages)](https://qianyumeng0228.github.io/ShizuSU-Modules)
[![Modules](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules%2Fmodules.json&query=length&label=Modules&color=blue)](https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json)
[![Licence](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

**Langues :** [中文](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/README.md) · [English](README.en.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · Français · [Italiano](README.it.md) · [Español](README.es.md)

Une source de référentiel de modules open source pour l'écosystème **KernelSU / Magisk / APatch** : une configuration, deux formats de sortie compatibles — **ShizuSU / SukiSU-Ultra (voie A)** et **MMRL / BakaSU (voie B)** — en remplacement de la source officielle abandonnée `modules.kernelsu.org`.

Elle collecte des modules open source filtrés à partir d'une **liste mondiale de 1 532 entrées** ; les versions et les liens de téléchargement sont automatiquement reconstruits chaque jour.

## Fonctionnalités

- **Sortie double format** : `modules.json` (schéma natif du gestionnaire) + `json/modules.json` (protocole MMRL) — un seul référentiel fonctionne avec ShizuSU, KernelSU, SukiSU-Ultra, MMRL et BakaSU
- **Maintenance entièrement automatique** : GitHub Actions met à jour chaque jour à 00:30 UTC les métadonnées, les dernières versions et les liens directs de téléchargement, avec re-signature
- **Audit de seuil open source** : `tools/validate.py` vérifie chaque module selon « source accessible + licence + version téléchargeable » ; les résultats sont écrits dans `audit.json` pour traçabilité
- **Mécanisme de signature** : l'index et les ZIP des modules privés sont signés Ed25519 ; la clé publique est fournie avec le référentiel pour vérification hors ligne
- **Collecte manuelle + automatique** : trois voies de soumission — via Issue, découverte automatique par topics GitHub, et envoi depuis le téléphone avec approbation
- **Collecte approuvée par l'administrateur** : les modules à licence peu claire sont collectés après examen par l'administrateur (`adminApproved`), marqués de façon transparente, risques évalués par l'utilisateur

## Démarrage rapide

### Gestionnaire ShizuSU / SukiSU-Ultra

Le gestionnaire prend en charge le remplacement de la source à l'exécution : écrire la clé `module_repo_base_url` dans la préférence « settings » avec l'URL Pages de ce référentiel :

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

### Gestionnaire officiel KernelSU (voie A)

Pour les gestionnaires prenant en charge le format de liste `modules.json`, ajouter la source :

```
https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json
```

### MMRL

Ajouter le référentiel dans MMRL ; l'URL peut comporter ou non un `/` final :

```
https://qianyumeng0228.github.io/ShizuSU-Modules/
```

MMRL lit `json/config.json` et `json/modules.json` ; les modules collectés peuvent être consultés et installés directement.

### BakaSU

Dans BakaSU « Paramètres du référentiel → + Ajouter un référentiel » :

- **Format d'API : choisir obligatoirement `MMRL`**
- **URL du serveur** (sans le suffixe `/json/modules.json`) :

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

> **Ne pas** choisir `KernelSU Modules API` : c'est le protocole Registry. Ce référentiel ne fournit pas de point de terminaison `api/v1`, et BakaSU impose une vérification SHA-256 réelle pour les sources Registry, ce qui entraînerait des erreurs 404/installation.

## Structure du référentiel

```
modules.json                  # Voie A : catalogue de modules (liste, conforme au schéma officiel)
module/<moduleId>.json        # Voie A : détails de chaque module (versions / README / liens de téléchargement)
json/config.json              # Voie B : description du référentiel MMRL
json/modules.json             # Voie B : index des modules MMRL
modules/<id>/track.json       # Voie B : définition de track MMRL
modules/<id>/update.json      # Voie B : MagiskUpdateJson (version/téléchargement)
signatures/public.pem         # Clé publique Ed25519
signatures/modules.sig        # Signature de modules.json
signatures/<moduleId>.sig     # Signature des ZIP de modules privés
audit.json                    # Résultats de l'audit de seuil open source
catalog/candidates.json       # Candidats de la découverte automatique par topics
private/*.zip                 # Modules privés (approuvés par l'administrateur)
compat/                       # Modules de compatibilité
```

Les données sont générées par `build.py` (voie A) + `tools/build_mmrl.py` (voie B) + `tools/validate.py` (audit) + `tools/sign.py` (signature) ; le schéma de la voie A est aligné champ par champ avec le code d'analyse du gestionnaire SukiSU-Ultra / ShizuSU.

## Contenu collecté

- **871 modules** dans l'index de la voie A ; **804** installables directement via MMRL/BakaSU
- **19 catégories** couvertes : masquage Root / Play Integrity, méta-modules (moteurs de montage), implémentations Zygisk, optimisation des performances, proxys réseau, blocage de publicité, audio, polices/affichage, sauvegarde et récupération, Xposed/LSPosed, WebUI, etc.
- **324 approuvés par l'administrateur** (`adminApproved`) : licence en amont non déclarée ou peu claire — collectés après examen par l'administrateur, chaque entrée porte une `note` ; évaluez les risques vous-même
- Source des données : synthèse mondiale des modules KernelSU (liste dédupliquée de 1 532 entrées)

## Critères de collecte

Les modules doivent satisfaire les conditions suivantes pour entrer dans l'index (voir [CONTRIBUTING.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/CONTRIBUTING.md)) :

1. **Source accessible** : un référentiel GitHub public
2. **Licence** : une licence open source standard détectable (SPDX) ; les licences peu claires passent par l'approbation de l'administrateur
3. **Téléchargeable** : la dernière version contient un ZIP téléchargeable
4. **Pas de builds noyau** : les référentiels de sources du noyau / builds LKM ne sont pas acceptés (le référentiel ne collecte que des modules installables)

Les modules non conformes sont marqués `unverified` (toujours affichés avec l'état « en attente de révision ») ; les modules privés sans référentiel public sont approuvés par l'administrateur et marqués `origin=manual`.

## Soumettre un module

Choisissez l'une des trois voies :

1. **Soumission via Issue (recommandée)** : ouvrir une Issue avec le [modèle de soumission de module](.github/ISSUE_TEMPLATE/module_submission.md) et indiquer le référentiel source et l'URL de la version
2. **Découverte automatique** : `discover-modules.yml` analyse GitHub chaque jour par topic (`shizusu-module` / `kernelsu-module` / `magisk-module` / `apatch-module`) ; les candidats arrivent dans `catalog/candidates.json`
3. **Envoi depuis le téléphone** : entrée « Envoi de module » du gestionnaire ShizuSU → file de révision → approbation de l'administrateur → inclusion automatique

## Mécanisme de mise à jour

- **Build quotidien** : à 00:30 UTC (08:30 heure de Pékin), mise à jour automatique des versions, liens de téléchargement et statistiques
- **Déclenchement manuel** : exécuter le workflow `Update module repo` depuis la page Actions du référentiel
- Chaîne de build : génération voie A → audit de seuil open source → sortie MMRL → signature → vérification du schéma → synchronisation GitHub Pages

## Citation et intégration (bienvenue)

Tout gestionnaire, outil ou site est invité à utiliser les données de ce référentiel. Méthodes recommandées :

- **Lire le JSON directement** : `https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json` (liste) et `module/<id>.json` (détails)
- **Badge dynamique** : le badge du nombre de modules est déjà dynamique (shields.io le lit en direct ; voir le début de ce fichier)
- **Spécification d'intégration** : définitions des champs dans [API.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/API.md) ; les liens de téléchargement pointent vers les versions GitHub en amont et peuvent être enregistrés directement
- **Attribution** : veuillez mentionner « Source des données : ShizuSU-Modules » avec un lien vers ce référentiel ; pour réduire la charge en amont, un cache du JSON est recommandé (les données se mettent à jour chaque jour vers 08:30)

## Licence et clause de non-responsabilité

- Le **code et l'index** de ce référentiel sont sous [licence MIT](LICENSE)
- Les modules tiers collectés **restent la propriété de leurs auteurs d'origine** : ce référentiel ne fait qu'indexer/relier ; « collecter » ne signifie pas accorder une autorisation d'utilisation — vérifiez la licence en amont de chaque module avant utilisation ; les modules approuvés par l'administrateur (`adminApproved`) ont des licences peu claires, évaluez les risques vous-même
- Si un auteur en amont revendique ses droits, ouvrez une Issue et l'entrée sera supprimée sous 24 heures
