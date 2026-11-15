# Télécharger EasyScanner Evolution

**Cette page regroupe toutes les versions Android. Garde ce lien dans tes favoris : elle restera à la même adresse.**

## Télécharger la dernière version en un clic

**[TÉLÉCHARGER LA DERNIÈRE VERSION — EasyScanner-Evolution.apk](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/latest/download/EasyScanner-Evolution.apk)**

Ce lien est permanent : il pointe vers l'APK de la **dernière version publiée**. Tu peux le garder dans les favoris de ton téléphone. Aucun fichier ZIP à ouvrir et aucune recherche dans GitHub Actions.

**La signature privée permanente est maintenant en service** depuis la version `0.3.1-evolution.5`. Pour les prochaines mises à jour signées avec cette même clé : [guide de signature et de sauvegarde](docs/SIGNATURE_PRIVEE.md).

## Dernière version disponible

### EasyScanner Evolution — 0.3.1-evolution.5 (signature permanente)

**[TÉLÉCHARGER L'APK SIGNÉ — version 0.3.1-evolution.5](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/download/v0.3.1-evolution.5/EasyScanner-Evolution-v0.3.1-evolution.5.apk)**

- Interface professionnelle en français et diagnostic caméra.
- Export DAO en XYZ / CSV, avec réduction spatiale sur grille de 1 mm.
- **Signature Android permanente et privée** : cette version devient la référence pour les futures mises à jour.
- Compilation, tests et vérification de signature réussis le **15 novembre 2026**.
- APK d'environ **38,9 Mo**, téléchargeable directement sans ZIP.

## Historique des versions publiées

| Version Android | Principales nouveautés | Télécharger |
|---|---|---|
| **0.3.1-evolution.5 — recommandée** | Interface professionnelle française + signature privée permanente | **[APK signé](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/download/v0.3.1-evolution.5/EasyScanner-Evolution-v0.3.1-evolution.5.apk)** |
| 0.3.1-evolution.3 | Diagnostic caméra + export DAO + français ; ancienne signature de débogage | [APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/download/v0.3.1-evolution.3/EasyScanner-Evolution-v0.3.1-evolution.3.apk) |
| 0.3.1-evolution.2 | Export XYZ / CSV, réduction spatiale de 1 mm ; ancienne signature de débogage | [APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/download/v0.3.1-evolution.2/EasyScanner-Evolution-v0.3.1-evolution.2.apk) |
| 0.3.1-evolution.1 | Première version française ; ancienne signature de débogage | [APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/download/v0.3.1-evolution.1/EasyScanner-Evolution-v0.3.1-evolution.1.apk) |

**[Ouvrir toutes les versions GitHub Releases](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases)**

Ces téléchargements sont publiés dans **Releases** et ne sont pas soumis à l'expiration de 30 jours des archives GitHub Actions, tant que le dépôt et les Releases existent.

## Installation sur Android

1. Sur le téléphone, appuie sur **Télécharger la dernière version** en haut de cette page.
2. Ouvre directement le fichier `.apk`.
3. Autorise l'installation depuis la source choisie si Android le demande.
4. Lance **EasyScanner Evolution**.

**Important pour la première installation signée (.5) :** les APK .1 à .3 utilisaient des clés de débogage différentes. Il peut être nécessaire de désinstaller une ancienne version pour installer la .5. **Sauvegarde les fichiers PLY, les photos et les sessions avant toute désinstallation** : les données internes peuvent être perdues.

À partir de la .5, les mises à jour sont possibles sans désinstallation à condition de conserver **la même clé privée, le même identifiant d'application et un `versionCode` croissant**.

## Publier les futures versions signées

La procédure officielle est désormais le workflow manuel **[APK Android signé (permanent)](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/workflows/android-signed-release.yml)**.

1. Incrémenter `versionName` et `versionCode` sur la branche `evolution-signature-stable`.
2. Ouvrir le workflow, garder la branche **main** et choisir **Run workflow**.
3. Une fois la compilation et la vérification de signature réussies, GitHub publie le nouvel APK dans Releases.
4. Mettre à jour l'historique ci-dessus. Le lien « Télécharger la dernière version » continuera à pointer vers la bonne version.

Une Release existante n'est pas écrasée : une nouvelle publication nécessite un nouveau numéro de version. **Ne publie plus de nouveaux APK de débogage en tant que dernière version**, car leur signature ne permettrait pas une mise à jour transparente depuis la .5.

## Autres téléchargements utiles

- [Support monobloc Redmi Note 14 Pro — STL / STEP (prototype)](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/runs/43707079746/artifacts/14159395277) : encore un fichier temporaire GitHub Actions.
- [Mires ChArUco A4, A3, A2 et autres formats](charuco/boards/)
- [Guide français des dossiers et fichiers](docs/COMPRENDRE_LES_FICHIERS.md)
- [Retour à l'accueil EasyScanner Evolution](README.md)

---

**EasyScanner Evolution est un prototype de scanner 3D, non un instrument topographique certifié.** La précision des mesures nécessite une validation indépendante avant tout usage en VRD.
