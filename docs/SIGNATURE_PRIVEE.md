# Signature permanente et privée d'EasyScanner Evolution

**But :** à partir de la version `0.3.1-evolution.5`, créer et réutiliser la **même signature Android privée** pour les versions APK publiées dans GitHub Releases.

**Coût : gratuit.** Pas besoin d'abonnement GitHub, ni de publication sur Google Play.

> **Règle de sécurité absolue :** ne jamais mettre le fichier de clé, son encodage Base64 ou ses mots de passe dans un dépôt public, un e-mail, une capture d'écran. Les saisir directement dans les secrets GitHub.

## 1. Créer la clé sur TON ordinateur Windows

Tu peux générer la clé avec l'outil `keytool`, fourni avec Java JDK 17. Si Windows répond que `keytool` est inconnu, installer un JDK 17 et rouvrir PowerShell.

1. Ouvre **PowerShell** sur Windows.
2. Copie le bloc suivant, puis appuie sur Entrée :

```powershell
$keyFile = Join-Path $HOME "Documents\EasyScanner-Evolution.jks"
keytool -genkeypair -v -keystore $keyFile -storetype JKS -alias easyscanner-evolution -keyalg RSA -keysize 3072 -validity 15000
```

3. Choisis un **mot de passe robuste** pour le fichier de clés (keystore). L'outil demandera quelques informations pour le certificat et, éventuellement, un mot de passe pour la clé elle-même. Tu peux utiliser le même mot de passe robuste pour les deux afin de simplifier la conservation.
4. Le fichier créé dans Documents est **`EasyScanner-Evolution.jks`**. **Ne l'envoie pas dans cette conversation.**

`15000` jours de validité représentent plus de 40 ans.

## 2. Faire deux sauvegardes privées

- Conserve le fichier `.jks` sur ton ordinateur et une **copie sécurisée sur un autre support** (clé USB chiffrée ou coffre-fort numérique).
- Conserve les mots de passe dans un gestionnaire de mots de passe, indépendamment du fichier si possible.
- Note l'alias exact : **`easyscanner-evolution`**.
- Si cette clé est perdue, **il sera normalement impossible de publier une mise à jour compatible** avec les applications déjà installées à l'aide de cette clé.

## 3. Ajouter quatre secrets dans GitHub

Ouvre directement [**les secrets du dépôt EasyScanner Evolution**](https://github.com/vauthierced-pixel/EasyScanner-Evolution/settings/secrets/actions).

Clique sur **New repository secret** pour chacun des quatre noms suivants. Les valeurs restent privées sur GitHub.

| Nom exact du secret | Valeur à saisir |
|---|---|
| `EASYSCANNER_KEYSTORE_BASE64` | Contenu encodé de `EasyScanner-Evolution.jks` (voir commande ci-dessous) |
| `EASYSCANNER_STORE_PASSWORD` | Mot de passe du keystore |
| `EASYSCANNER_KEY_ALIAS` | `easyscanner-evolution` |
| `EASYSCANNER_KEY_PASSWORD` | Mot de passe de la clé (identique au premier si tu l'as choisi ainsi) |

Pour préparer **le premier secret**, utilise cette commande PowerShell sur ton ordinateur :

```powershell
$keyFile = Join-Path $HOME "Documents\EasyScanner-Evolution.jks"
[Convert]::ToBase64String([IO.File]::ReadAllBytes($keyFile)) | Set-Clipboard
```

Cette commande **copie la valeur dans le presse-papiers**. Dans GitHub, crée `EASYSCANNER_KEYSTORE_BASE64`, colle la valeur dans le champ Secret, puis clique sur **Add secret**. Tu peux ensuite vider le presse-papiers depuis PowerShell avec `Set-Clipboard -Value ""`.

**Important :** Base64 n'est **pas du chiffrement**. Il sert seulement à transférer le fichier binaire dans un champ secret. La protection est celle des *secrets GitHub*, et celle de tes sauvegardes privées.

## 4. Lancer la compilation signée

Quand les quatre secrets existent :

1. Ouvre [**APK Android signé (permanent)**](https://github.com/vauthierced-pixel/EasyScanner-Evolution/actions/workflows/android-signed-release.yml).
2. Clique sur **Run workflow**.
3. Laisse la branche **main** sélectionnée et confirme.
4. GitHub récupère le code de `evolution-signature-stable`, construit et vérifie un APK signé, puis le publie dans une nouvelle Release si tout réussit.
5. Retrouve l'APK dans [**Télécharger EasyScanner Evolution**](https://github.com/vauthierced-pixel/EasyScanner-Evolution/blob/main/TELECHARGER.md) : le lien permanent « dernière version » pointera vers le nouvel APK.

Aucune nouvelle publication n'est effectuée tant que tu n'as pas configuré les secrets et lancé cette action.

## 5. Une transition unique entre les anciennes signatures et la nouvelle

Les versions **0.3.1-evolution.1 à .4** actuellement compilées en mode débogage sont signées avec des **clés de débogage générées sur les machines GitHub**. La nouvelle clé permanente sera **différente**.

Android refusera normalement de mettre directement à jour l'une des anciennes versions par une nouvelle signature. Il faudra donc, **une fois seulement** :

1. Exporter ou sauvegarder les scans `PLY`, photos, sessions et réglages utiles.
2. Vérifier les sauvegardes **avant de désinstaller**.
3. Désinstaller l'ancienne version si Android refuse l'installation.
4. Installer la première version utilisant la clé privée permanente, puis vérifier son fonctionnement.

Les mises à jour suivantes pourront s'installer par-dessus si **l'identifiant d'application reste identique**, si les APK utilisent **cette même clé**, et si le **versionCode augmente**.

## 6. Ce qui a été préparé dans le code

- La branche `evolution-signature-stable`, construite à partir de l’interface professionnelle française, porte la future version `0.3.1-evolution.5` / `versionCode 9`.
- Le fichier Gradle lit la clé et ses mots de passe uniquement à partir de variables d'environnement, sans rien inscrire dans le dépôt.
- Le workflow manuel `APK Android signé (permanent)` ne fonctionne que depuis la branche principale et ne publie un APK que **si les quatre secrets existent**, si la compilation réussit et si `apksigner` confirme une signature valide.
- Les trois anciennes Releases restent accessibles : aucune clé ni signature précédente n'est modifiée.

## Références officielles

- [Google Android : signer son application](https://developer.android.com/studio/publish/app-signing?hl=fr).
- [GitHub : utiliser les secrets dans Actions](https://docs.github.com/fr/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets).

**Ne partage jamais la clé privée ou les mots de passe ici.** Si tu es bloqué sur une étape, tu peux montrer uniquement la fenêtre GitHub **sans les valeurs des secrets**.
