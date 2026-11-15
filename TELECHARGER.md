# Télécharger EasyScanner Evolution

**Cette page regroupe toutes les versions Android. Garde ce lien dans tes favoris : elle restera à la même adresse.**

## Dernière version disponible

### EasyScanner Evolution — 0.3.1-evolution.3

**[TÉLÉCHARGER DIRECTEMENT L'APK — version 0.3.1-evolution.3](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/download/v0.3.1-evolution.3/EasyScanner-Evolution-v0.3.1-evolution.3.apk)**

- Interface française et bibliothèque de scans.
- Export DAO **XYZ / CSV** en millimètres, avec option de réduction spatiale sur grille de 1 mm.
- **Diagnostic caméra** : identifiant, focales et résolutions déclarées par Android ; affichage de la résolution réellement analysée et des images par seconde.
- Compilation et tests automatiques GitHub réussis le **15 novembre 2026**.
- Fichier APK d'environ **41 Mo**, **sans archive ZIP à décompresser**.

## Historique des versions

| Version Android | Modifications | Téléchargement direct |
|---|---|---|
| **0.3.1-evolution.3 — la plus récente** | Diagnostic caméra + exports DAO + français | **[Télécharger APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/download/v0.3.1-evolution.3/EasyScanner-Evolution-v0.3.1-evolution.3.apk)** |
| 0.3.1-evolution.2 | Exports XYZ / CSV, réduction sur grille de 1 mm, français | [Télécharger APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/download/v0.3.1-evolution.2/EasyScanner-Evolution-v0.3.1-evolution.2.apk) |
| 0.3.1-evolution.1 | Première traduction française, scanner original | [Télécharger APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases/download/v0.3.1-evolution.1/EasyScanner-Evolution-v0.3.1-evolution.1.apk) |

**[Toutes les versions sur GitHub Releases](https://github.com/vauthierced-pixel/EasyScanner-Evolution/releases)**

Les APK sont désormais publiés dans **Releases**, et non plus seulement dans les archives provisoires des compilations GitHub Actions. Les fichiers restent accessibles tant que les Releases correspondantes sont conservées sur le dépôt ; ils n'expirent pas après 30 jours.

## Installer sur Android

1. Sur ton téléphone, clique sur **Télécharger APK** dans le tableau.
2. Ouvre le fichier `.apk` téléchargé.
3. Autorise l'installation depuis ton navigateur ou gestionnaire de fichiers si Android le demande.
4. Lance **EasyScanner Evolution**.

**Attention aux mises à jour :** les APK actuels sont signés avec une clé de débogage créée lors de chaque compilation GitHub. Il se peut qu'Android **refuse d'installer une nouvelle version par-dessus l'ancienne**. Avant de désinstaller une version, sauvegarde tes nuages PLY, les photos et les sessions : la désinstallation peut effacer les fichiers internes de l'application. Une signature permanente et privée sera notre prochaine étape pour autoriser les mises à jour simples.

## Comment publier une nouvelle version permanente

Pour l'instant, la publication se fait depuis le workflow GitHub **[Publier un APK permanent (Releases)](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/workflows/publish-releases.yml)**.

1. L'APK doit d'abord être compilé avec succès par **[Android APK (Evolution)](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/workflows/android-apk.yml)**.
2. Ouvre le workflow **Publier un APK permanent**, puis **Run workflow**.
3. Indique la valeur exacte de `versionName` (exemple : `0.3.1-evolution.4`) et l'ID de la compilation Android réussie (nombre visible dans l'URL de l'exécution).
4. Après publication, ajoute son nouveau lien direct au tableau de cette page.

Le script refuse de publier une compilation échouée ou de remplacer une Release déjà existante. Les tags des Releases archivées se rapportent à la documentation sur la branche `main` ; les notes de chaque Release donnent le commit exact ayant produit l'APK sur la branche de développement.

## Autres téléchargements utiles

- [Support monobloc Redmi Note 14 Pro — STL / STEP (prototype)](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/runs/43707079746/artifacts/14159395277) : encore un fichier temporaire GitHub Actions.
- [Mires ChArUco A4, A3, A2 et autres formats](charuco/boards/)
- [Guide français des dossiers et fichiers](docs/COMPRENDRE_LES_FICHIERS.md)
- [Retour à l'accueil EasyScanner Evolution](README.md)

---

**EasyScanner Evolution est un prototype de scanner 3D, non un instrument topographique certifié.** La précision des mesures nécessite une validation indépendante avant tout usage en VRD.
