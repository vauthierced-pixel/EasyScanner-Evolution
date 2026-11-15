#!/usr/bin/env bash
# Publish a verified Android APK from GitHub Actions as a permanent Release.
set -euo pipefail

: "${GH_TOKEN:?GitHub token required}"
: "${GITHUB_REPOSITORY:?GitHub repository required}"
: "${VERSION:?Android version required}"
: "${RUN_ID:?Successful Android workflow run required}"

if [[ "$GITHUB_REPOSITORY" != "vauthierced-pixel/EasyScanner-Evolution" ]]; then
  echo "Unexpected repository: $GITHUB_REPOSITORY" >&2
  exit 1
fi
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+-evolution\.[0-9]+$ ]]; then
  echo "Unexpected version name: $VERSION" >&2
  exit 1
fi
if [[ ! "$RUN_ID" =~ ^[0-9]+$ ]]; then
  echo "Invalid workflow run ID" >&2
  exit 1
fi

tag="v${VERSION}"
if gh release view "$tag" --repo "$GITHUB_REPOSITORY" >/dev/null 2>&1; then
  echo "Release $tag already exists; preserving existing APK."
  exit 0
fi

run_json="$(gh api "repos/${GITHUB_REPOSITORY}/actions/runs/${RUN_ID}")"
run_status="$(jq -r '.status' <<< "$run_json")"
run_result="$(jq -r '.conclusion' <<< "$run_json")"
run_name="$(jq -r '.name' <<< "$run_json")"
run_origin="$(jq -r '.head_repository.full_name' <<< "$run_json")"
source_sha="$(jq -r '.head_sha' <<< "$run_json")"

if [[ "$run_status" != "completed" || "$run_result" != "success" ||
      "$run_name" != "Android APK (Evolution)" ||
      "$run_origin" != "$GITHUB_REPOSITORY" ||
      ! "$source_sha" =~ ^[0-9a-f]{40}$ ]]; then
  echo "Run #$RUN_ID is not a successful EasyScanner Evolution Android build" >&2
  exit 1
fi

gradle_file="$(gh api "repos/${GITHUB_REPOSITORY}/contents/android/app/build.gradle.kts?ref=${source_sha}" \
  --jq .content | tr -d '\n' | base64 --decode)"
if ! grep -Fq "versionName = \"$VERSION\"" <<< "$gradle_file"; then
  echo "The source for run #$RUN_ID does not declare versionName = $VERSION" >&2
  exit 1
fi

outdir="$(mktemp -d)"
trap 'rm -rf "$outdir"' EXIT
mkdir -p "$outdir/from-actions" "$outdir/release"
gh run download "$RUN_ID" --repo "$GITHUB_REPOSITORY" \
  --name "EasyScanner-Evolution-APK" --dir "$outdir/from-actions"

mapfile -d '' apk_files < <(find "$outdir/from-actions" -type f -name '*.apk' -print0)
if [[ "${#apk_files[@]}" -ne 1 ]]; then
  echo "Expected one APK, found ${#apk_files[@]}" >&2
  exit 1
fi

asset="EasyScanner-Evolution-${tag}.apk"
cp "${apk_files[0]}" "$outdir/release/$asset"
unzip -tqq "$outdir/release/$asset"
(
  cd "$outdir/release"
  sha256sum "$asset" > "${asset}.sha256"
)

cat > "$outdir/notes.md" <<EOF
## EasyScanner Evolution ${VERSION}

Application Android expérimentale en français, dérivée du projet libre EasyScanner.

**Installation :** télécharger le fichier **${asset}** dans les fichiers ci-dessous (sans archive ZIP intermédiaire).

**Attention aux mises à jour Android :** cet APK est signé avec une clé de débogage générée pendant la compilation. Une ancienne version peut avoir une signature différente et refuser la mise à jour. Sauvegarder les scans et les sessions avant de désinstaller quoi que ce soit. Pour des mises à jour fiables, il faudra configurer une clé de signature persistante et privée.

**Précision 3D :** prototype expérimental, non adapté à des mesures VRD sans contrôle indépendant.

- [Compilation GitHub #${RUN_ID}](https://github.com/${GITHUB_REPOSITORY}/actions/runs/${RUN_ID})
- Code source de l\'application : ${source_sha}
- Le tag GitHub de la Release pointe vers la documentation principale (`main`), tandis que le code exact de l\'APK est disponible via le commit ci-dessus.\n- Un fichier SHA-256 permet de vérifier l'intégrité de l'APK.
EOF

latest_flag="--latest=false"
if [[ "${MARK_LATEST:-false}" == "true" ]]; then
  latest_flag="--latest"
fi

gh release create "$tag" \
  "$outdir/release/$asset" "$outdir/release/${asset}.sha256" \
  --repo "$GITHUB_REPOSITORY" \
  --target "main" \
  --title "EasyScanner Evolution ${VERSION}" \
  --notes-file "$outdir/notes.md" \
  "$latest_flag"

echo "Published: https://github.com/${GITHUB_REPOSITORY}/releases/tag/$tag"
