# Télécharger EasyScanner Evolution

> **C'est la page à conserver dans tes favoris.** Elle regroupe les versions de l'application Android, de la plus récente à la plus ancienne.
>
> **Version à installer actuellement : 0.3.1-evolution.3.**

## La dernière version

### EasyScanner Evolution 0.3.1-evolution.3 — Diagnostic caméra

**[TÉLÉCHARGER LA VERSION 0.3.1-evolution.3 (ZIP contenant l'APK)](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/runs/43723209578/artifacts/14165571728)**

- Interface principale en français.
- Diagnostic caméra (identifiant, focale, résolutions accessibles).
- Résolution analysée et images par seconde affichées dans le scanner.
- Export des scans en XYZ et CSV pour la DAO, avec option de réduction sur une grille de 1 mm.
- Compilation GitHub réussie le **15 novembre 2026**.
- **[Voir la fiche de compilation](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/runs/43723209578)**.

## Historique des versions Android

| Version | Nouveautés principales | Télécharger | Date de compilation |
|---|---|---|---|
| **0.3.1-evolution.3** — recommandée | Diagnostic caméra + export DAO + français | **[ZIP / APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/runs/43723209578/artifacts/14165571728)** | 15/11/2026 |
| 0.3.1-evolution.2 | Export XYZ/CSV + réduction spatiale 1 mm + français | [ZIP / APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/runs/43701549566/artifacts/14156542368) | 15/11/2026 |
| 0.3.1-evolution.1 | Première application française + compilation automatisée | [ZIP / APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/runs/43697031317/artifacts/14154693064) | 15/11/2026 |

Les trois versions ci-dessus ont une compilation GitHub réussie. Cela ne remplace pas une validation de la précision 3D sur un scan réel.

## Installer en quatre étapes

1. **Clique sur le lien ZIP / APK** de la version choisie. Connecte-toi à GitHub si nécessaire.
2. Dans le dossier **Téléchargements** du téléphone ou de l'ordinateur, ouvre le ZIP téléchargé.
3. **Extrais le fichier `app-debug.apk`** : c'est lui qui installe l'application Android.
4. Ouvre ce fichier APK sur le téléphone, puis autorise son installation si Android le demande.

Tu peux installer une nouvelle version Evolution par-dessus l'ancienne tant que la signature de test reste compatible. En cas d'échec, **ne désinstalle pas l'ancienne application avant d'avoir sauvegardé les scans et les sessions**.

## Un lien ne fonctionne plus ?

Les ZIP des compilations **GitHub Actions expirent**. Les archives ci-dessus sont prévues pour rester disponibles jusqu'au **15 décembre 2026**. Cette page, elle, reste accessible à la même adresse.

Si un lien a expiré, ouvre la page **[Toutes les compilations APK](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/workflows/android-apk.yml)**. Choisis une compilation avec une **coche verte**, puis descends à la rubrique **Artifacts** et clique sur **EasyScanner-Evolution-APK**. Les futures versions pourront aussi être publiées dans des *Releases* pour conserver durablement les APK.

## Autres fichiers utiles

- **[Support monobloc Redmi Note 14 Pro — fichiers STL et STEP](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/runs/43707079746/artifacts/14159395277)** (prototype à vérifier avant fabrication).
- **[Mires ChArUco prêtes à imprimer](charuco/boards/)** (A4, A3, A2, A1, A0).
- **[Guide français des fichiers](docs/COMPRENDRE_LES_FICHIERS.md)**.
- **[Accueil du projet](README.md)**.

---

**Important :** EasyScanner Evolution est un scanner 3D expérimental. La précision des mesures n'est pas certifiée. N'utilise pas ces mesures pour des travaux VRD sans contrôle indépendant.
