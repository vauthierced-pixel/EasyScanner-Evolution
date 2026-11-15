# Comprendre les fichiers d'EasyScanner Evolution

Ce guide explique **ce que contient le dépôt**, ce qu'il faut ouvrir selon son objectif et les fichiers qu'il vaut mieux ne pas modifier sans préparation.

> Le dépôt est un *fork* (une copie indépendante) d'[EasyScanner de Raw Mechatronics](https://github.com/RawMechatronicsOrg/EasyScanner). Les explications ci-dessous sont adaptées à notre version Evolution.

## 1. S'orienter sur GitHub

| Ce que tu vois | Signification |
|---|---|
| **Code** | Liste des fichiers du projet |
| **main** | Branche principale, conservée proche du projet d'origine |
| **evolution-v0.3-fr-apk** | Branche où se trouvent nos améliorations Android et les exports XYZ/CSV |
| **Actions** | Ordinateur de compilation automatique de GitHub |
| **Android APK (Evolution)** | Procédure qui fabrique l'application Android |
| **Artifacts** | Archives ZIP produites par une compilation réussie ; elles contiennent l'APK |
| **Pull requests** | Modifications proposées, séparées de la branche principale |
| **README.md** | Page d'accueil affichée sous la liste des fichiers |

**Important :** changer de branche dans le menu au-dessus des fichiers change les versions affichées. Si tu regardes `main`, les dernières fonctions Evolution peuvent ne pas encore s'y trouver.

[Voir la branche Evolution](../tree/evolution-v0.3-fr-apk) · [Voir les compilations](../actions/workflows/android-apk.yml) · [Voir la proposition de modification](../pull/1)

Sur un navigateur, tu peux aussi utiliser « Traduire en français » pour les boutons de GitHub. Cela ne change pas le code.

## 2. Les grands dossiers

| Dossier ou fichier | Explication simple | À quoi il sert |
|---|---|---|
| `README.md` | Accueil en français | Comprendre le projet sans ouvrir le code |
| `README_EN.md` | Documentation anglaise du projet d'origine | Garder la référence technique complète |
| `android/` | Application Android | Caméra, affichage, calculs, galerie, export |
| `cad/` | Conception assistée par ordinateur | Pièces à imprimer en 3D et montage du scanner |
| `charuco/` | Mires ChArUco | PDF à imprimer pour repérer la position du téléphone |
| `docs/` | Documentation et images | Guides et illustrations |
| `.github/workflows/` | Automatisation GitHub | Compilation de l'APK |
| `LICENSE` | Licence du code | Conditions d'utilisation du logiciel |

## 3. Dans android/ : deux parties qui travaillent ensemble

### android/app/ — l'application visible sur le téléphone

C'est le code **Kotlin** (extension `.kt`). Il gère la caméra, les écrans, les menus, les sessions et les fichiers.

Chemin principal :
`android/app/src/main/java/com/rawmechatronics/easyscanner/`

| Fichier | Son rôle |
|---|---|
| `MainActivity.kt` | Écran principal et parcours de numérisation |
| `Wizard.kt` | Contrôle les étapes : mire, mise au point, caméra, laser, scan |
| `CameraController.kt` | Dialogue avec la caméra Android |
| `FrameProcessor.kt` | Transmet les images au moteur de calcul |
| `FrameResult.kt` | Structure des résultats renvoyés par le moteur |
| `OverlayView.kt` | Affiche les repères et informations sur l'image |
| `CloudView.kt` | Affichage 3D du nuage de points |
| `ResolutionGovernor.kt` | Ajustement automatique de la résolution |
| `AppSettings.kt` | Lecture et gestion des réglages |
| `SettingsActivity.kt` | Écran des paramètres |
| `LibraryActivity.kt` | Liste des numérisations enregistrées |
| `ScanLibrary.kt` | Recherche les scans et leurs photos |
| `ScanViewActivity.kt` | Vue détaillée d'un scan, photos et export DAO |
| `PlyCloud.kt` | Lecture du nuage PLY pour le visualiser |
| `PlyDaoExporter.kt` | **Evolution : export complet XYZ/CSV avec réduction optionnelle par grille** |
| `DaoDownloads.kt` | **Evolution : écrit les exports DAO dans Téléchargements** |
| `SessionExport.kt` | Copie les sessions dans Téléchargements |
| `Photos.kt`, `PhotoActivity.kt` | Gestion et affichage des photos |
| `NativeLib.kt` | Liaison entre le code Kotlin et le moteur Rust |
| `Insets.kt` | Ajustement de l'affichage aux barres Android |

Les deux fichiers **Evolution** ci-dessus sont présents sur la branche `evolution-v0.3-fr-apk`.

### android/app/src/main/res/ — textes et écrans

| Chemin | Utilité |
|---|---|
| `values/strings.xml` | Textes anglais, référence par défaut |
| `values-fr/strings.xml` | **Traduction française Evolution** |
| `xml/preferences.xml` | Définition des réglages (encore en partie en anglais) |
| `layout/` | Organisation des écrans Android |
| `AndroidManifest.xml` | Déclaration de l'application et de ses autorisations |

Pour traduire un texte à l'écran, il vaut généralement mieux utiliser un fichier `strings.xml` que remplacer directement les textes dans le programme. Certains réglages de `preferences.xml` doivent encore être externalisés pour être traduits proprement.

### android/core/ — le moteur de calcul 3D

C'est du code **Rust** (extension `.rs`), avec une liaison native Android et OpenCV.

Dans `core/algo/src/` :

| Fichier | Rôle principal |
|---|---|
| `laser.rs` | Détection de la réponse du laser |
| `stripe.rs` | Extraction de la bande lumineuse |
| `plane.rs` | Calcul du plan laser |
| `geom.rs` | Calculs géométriques |
| `cloud.rs` | Gestion du nuage de points |
| `volume.rs` | Limites du volume à scanner |
| `focus.rs` | Mise au point |
| `keyframe.rs` | Choix et synchronisation des vues photo |
| `photo_session.rs` | Données des sessions photo |
| `config.rs` | Paramètres et formats de configuration |
| `overlay.rs` | Géométrie des repères |
| `lib.rs` | Entrée de la bibliothèque Rust |

Dans `core/android/src/` :

| Fichier | Rôle principal |
|---|---|
| `board.rs` | Reconnaissance de la mire et calcul de position |
| `calib.rs` | Calibration de la caméra |
| `engine.rs` | Orchestration du calcul par image |
| `frame_out.rs` | Résultats transmis à l'application |
| `lib.rs` | Interface native Android |
| `e2e_tests.rs` | Tests du moteur de bout en bout |

**Ces fichiers pilotent les calculs 3D : mieux vaut les modifier par étapes, avec des tests.**

## 4. Les fichiers qui t'intéressent le plus

### Mires imprimables

Dossier : [`charuco/boards/`](../tree/main/charuco/boards)

| Feuille | Fichier | Carrés X × Y | Taille d'un carré |
|---|---|---|---|
| A4 | [`charuco_A4_4x6_45mm.pdf`](../blob/main/charuco/boards/charuco_A4_4x6_45mm.pdf) | 4 × 6 | 45 mm |
| A3 | [`charuco_A3_6x8_45mm.pdf`](../blob/main/charuco/boards/charuco_A3_6x8_45mm.pdf) | 6 × 8 | 45 mm |
| A2 | [`charuco_A2_8x10_45mm.pdf`](../blob/main/charuco/boards/charuco_A2_8x10_45mm.pdf) | 8 × 10 | 45 mm |

Imprimer à **100 %**, vérifier la règle de 100 mm, puis poser la feuille bien à plat. Le dictionnaire par défaut de ces mires est `DICT_5X5_100` (identifiant 5). Les dimensions exactes des A0 et A1 figurent dans `charuco/boards/boards.json`.

### Pièces mécaniques à imprimer

Dossier : [`cad/`](../tree/main/cad)

- `cad/export/*.stl` : pièces du support du laser, prêtes pour l'impression 3D.
- `cad/phone-clamp/export/*.stl` : pièces du support du téléphone.
- `cad/assembly/easy_scanner.step` : **assemblage mécanique 3D**, ouvrable dans un logiciel de CAO compatible STEP.
- `cad/assembly/EasyScanner.FCStd` : assemblage au format **FreeCAD**.
- `cad/assembly/easy_scanner.glb` : modèle 3D pour visualisation.
- `cad/models/*.py` : scripts de génération des pièces mécaniques.

La conception d'origine prévoit un **module laser linéaire cylindrique de diamètre 12 mm**, fixé près de la caméra sur un profilé aluminium en U de 16 × 13 mm. La fixation du téléphone est soumise à une licence spécifique, différente de celle du reste du support.

### Résultats des scans

| Extension | Qu'est-ce que c'est ? |
|---|---|
| `.ply` | Nuage de points d'origine, avec couleurs si disponibles |
| `.xyz` | Une ligne par point : `X Y Z`, séparés par des espaces, en millimètres |
| `.csv` | Tableau de coordonnées : `X_mm;Y_mm;Z_mm`, en millimètres |
| `.jpg` | Photos enregistrées pendant le scan |
| `.json` / `.jsonl` | Paramètres ou informations de session |

Notre export **XYZ/CSV** n'efface pas le PLY. L'option « grille 1 mm » garde un point par cellule cubique : ce n'est pas encore un filtrage des points isolés. Les coordonnées sont locales à la mire ; **il n'y a pas de géoréférencement de chantier**.

## 5. Comment retrouver l'APK

1. Ouvrir [Actions → Android APK (Evolution)](../actions/workflows/android-apk.yml).
2. Cliquer sur une exécution ayant une **coche verte**.
3. En bas de la page, trouver **Artifacts**.
4. Cliquer sur `EasyScanner-Evolution-APK` pour télécharger une archive ZIP.
5. Décompresser le ZIP pour obtenir `app-debug.apk`.

Un compte GitHub connecté peut être nécessaire pour télécharger l'archive. Les fichiers Artifacts sont temporaires (la configuration actuelle prévoit 30 jours).

La compilation prépare Java, Android SDK/NDK, Rust et OpenCV automatiquement. Pour nous, le fichier qui décrit ces opérations est :
[`.github/workflows/android-apk.yml`](../blob/evolution-v0.3-fr-apk/.github/workflows/android-apk.yml).

## 6. Que peut-on modifier sans tout casser ?

**Documentation et explications :** `README.md`, les guides dans `docs/`. C'est le plus simple.

**Textes affichés par l'application :** `strings.xml` et, avec précaution, `preferences.xml`.

**Boutons, menus, exports :** `android/app/`, en Kotlin, avec recompilation obligatoire.

**Précision 3D et traitement du laser :** `android/core/`, en Rust : tests et essais réels indispensables.

Il ne faut pas renommer arbitrairement les fichiers `.kt`, `.rs`, les dossiers de package ou les fichiers de compilation : d'autres morceaux du projet les utilisent sous leurs noms exacts.

## 7. Licences et prudence

- Code et scripts : [Apache-2.0](../LICENSE).
- Pièces mécaniques du scanner : [CERN-OHL-S-2.0](../cad/LICENSE).
- Support de téléphone et pièces dérivées : [CC BY-NC-SA 4.0](../cad/phone-clamp/LICENSE).

Le dépôt est **public**. Ne pas y ajouter de plans de chantier internes, de documents de collectivité ou de données personnelles.

---

[Retour à l'accueil](../README.md) · [Documentation originale anglaise](../README_EN.md) · [Projet d'origine](https://github.com/RawMechatronicsOrg/EasyScanner)
