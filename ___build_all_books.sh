#!/usr/bin/env bash
set -euo pipefail

# Usage examples:
#   ./build_all_books.sh
#   ./build_all_books.sh --clean
#   ./build_all_books.sh --gen-md-toc             # calls __generate_md_toc.py
#   ./build_all_books.sh --skip=BookA,BookB
#   ./build_all_books.sh --only=BookA,BookB
#   ./build_all_books.sh --prompt                 # ask before each build
#   ./build_all_books.sh --preprompt              # ask up front, then build selected
#   ./build_all_books.sh --clean --preprompt
#   ./build_all_books.sh --build-root             # also build a book in ROOT_DIR (if it looks like a book)
#   ./build_all_books.sh --build-root-only        # build only the root book (skip books/)

DO_CLEAN=0
DO_GEN_MD_TOC=0
DO_PROMPT=0       # prompt right before each build
DO_PREPROMPT=0    # prompt once up front to select list
DO_BUILD_ROOT=1   # also build the book in ROOT_DIR (current folder)
DO_ROOT_ONLY=0    # build only ROOT_DIR (ignore books/)
ONLY_LIST=""
SKIP_LIST=""

DO_BUNDLE_SITES=0 # copy all builds to the root build.


for arg in "$@"; do
  case "$arg" in
    --clean) DO_CLEAN=1 ;;
    --gen-md-toc) DO_GEN_MD_TOC=1 ;;
    --prompt) DO_PROMPT=1 ;;
    --preprompt) DO_PREPROMPT=1 ;;
    --build-root) DO_BUILD_ROOT=1 ;;
    --build-root-only) DO_BUILD_ROOT=1; DO_ROOT_ONLY=1 ;;
    --only=*) ONLY_LIST="${arg#*=}" ;;
    --skip=*) SKIP_LIST="${arg#*=}" ;;
    --bundle-sites) DO_BUNDLE_SITES=1 ;;
    *)
      echo "Unknown option: $arg"
      exit 1
      ;;
  esac
done

if [[ $DO_PROMPT -eq 1 && $DO_PREPROMPT -eq 1 ]]; then
  echo "ERROR: Use only one of --prompt or --preprompt."
  exit 1
fi

if [[ $DO_ROOT_ONLY -eq 1 && ( -n "$ONLY_LIST" || -n "$SKIP_LIST" ) ]]; then
  echo "ERROR: --build-root-only cannot be combined with --only= or --skip=."
  exit 1
fi

# Ensure user-installed scripts are visible (DesignSafe)
export PATH="$HOME/.local/bin:$PATH"

# Install classic Jupyter Book only if jb is missing
if ! command -v jb >/dev/null 2>&1; then
  echo "=== Installing classic Jupyter Book (jb) ==="
  python -m pip install --user -U "jupyter-book<1"
fi

# Optional extension (only install if import fails)
python -c "import sphinx_last_updated_by_git" 2>/dev/null || \
  python -m pip install --user -U sphinx-last-updated-by-git
python -c "import sphinx_last_updated_by_git; print('sphinx-last-updated-by-git: ok')"

# ---------- Paths ----------
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

BASE_CFG="shared/_config.base.yml"
BOOKS_DIR="books"
TOC_GEN="__generate_md_toc.py"

SHARED_STATIC_DIR="shared/_static"

# ---------- Repo/Pages settings (edit once, or set in env e.g. CI) ----------
REPO_URL="${REPO_URL:-https://github.com/<YOURUSER>/<YOURREPO>}"
BASE_PAGES_URL="${BASE_PAGES_URL:-https://<YOURUSER>.github.io/<YOURREPO>}"

# ---------- Per-book titles (edit as needed) ----------
declare -A TITLES=(
  # ["OpenSees-on-DesignSafe"]="OpenSees on DesignSafe"
  # ["ROOT"]="My Root Book Title"
)

# ---------- Helpers ----------
csv_contains() { local csv="$1" item="$2"; [[ ",$csv," == *",$item,"* ]]; }

should_consider_book() {
  local bookname="$1"
  if [[ -n "$ONLY_LIST" ]]; then
    csv_contains "$ONLY_LIST" "$bookname" || return 1
  fi
  if [[ -n "$SKIP_LIST" ]]; then
    csv_contains "$SKIP_LIST" "$bookname" && return 1
  fi
  return 0
}

is_book_dir() {
  local d="$1"
  [[ -f "$d/_toc.yml" || -f "$d/myst.yml" ]]
}

sync_shared_static_into_book() {
  local bookdir="$1"

  # Only proceed if the shared static directory exists
  [[ -d "$SHARED_STATIC_DIR" ]] || return 0

  # Ensure the book has a local _static folder (classic JB uses this)
  mkdir -p "$bookdir/_static"

  # Copy only JS and CSS (and keep them updated)
  if command -v rsync >/dev/null 2>&1; then
    rsync -av --delete \
      --include="*/" \
      --include="*.js" \
      --include="*.css" \
      --exclude="*" \
      "$SHARED_STATIC_DIR/" "$bookdir/_static/"
  else
    cp -f "$SHARED_STATIC_DIR/"*.js "$bookdir/_static/" 2>/dev/null || true
    cp -f "$SHARED_STATIC_DIR/"*.css "$bookdir/_static/" 2>/dev/null || true
  fi
}

prepare_and_build_book() {
  local bookdir="$1"
  local bookname="$2"
  local baseurl="$3"

  if [[ $DO_CLEAN -eq 1 ]]; then
    echo "---- Cleaning: ${bookname} ----"
    rm -rf "$bookdir/_build" "$bookdir/.jupyter_cache" 2>/dev/null || true
  fi

  echo "---- Preparing config for: ${bookname} ----"
  cp "$BASE_CFG" "$bookdir/_config.yml"
  local title="${TITLES[$bookname]:-$bookname}"
  sed -i "s|__TITLE__|${title}|g" "$bookdir/_config.yml"
  sed -i "s|__BASEURL__|${baseurl}|g" "$bookdir/_config.yml"
  sed -i "s|__REPOURL__|${REPO_URL}|g" "$bookdir/_config.yml"

    if [[ "$bookname" == "ROOT" ]]; then
      shared_path="./shared"
    else
      shared_path="../../shared"
    fi
    
    sed -i "s|__SHARED__|${shared_path}|g" "$bookdir/_config.yml"
  

  


  

  echo "---- Syncing shared static assets into: ${bookname} ----"
  sync_shared_static_into_book "$bookdir"

  echo "---- Building: ${bookname} ----"
  jb build "$bookdir"
}

# ---------- Optional TOC generation ----------
if [[ $DO_GEN_MD_TOC -eq 1 ]]; then
  echo "=== Step 0: Generate markdown TOCs (optional) ==="
  [[ -f "$TOC_GEN" ]] || { echo "ERROR: $TOC_GEN not found in $ROOT_DIR"; exit 1; }
  python "$TOC_GEN"
  echo "=== TOC generator changes (if any) ==="
  git status --porcelain || true
else
  echo "=== Step 0: Skipping markdown TOC generation (use --gen-md-toc to enable) ==="
fi

# ---------- Build root (optional) ----------
if [[ $DO_BUILD_ROOT -eq 1 ]]; then
  if is_book_dir "$ROOT_DIR"; then
    echo "=== Step 0.5: Root book detected; will build ROOT_DIR ==="
  else
    echo "=== Step 0.5: --build-root set, but ROOT_DIR is not a Jupyter Book (missing _toc.yml or myst.yml). Skipping root build. ==="
    DO_BUILD_ROOT=0
  fi
fi

# If root-only, skip discovery and just build root (if enabled)
if [[ $DO_ROOT_ONLY -eq 1 ]]; then
  if [[ $DO_BUILD_ROOT -eq 1 ]]; then
    if [[ $DO_PROMPT -eq 1 || $DO_PREPROMPT -eq 1 ]]; then
      read -r -p "Build 'ROOT' now? [y/N] " ans
      case "${ans:-}" in
        y|Y|yes|YES) ;;
        *) echo "---- Skipping (by prompt): ROOT ----"; exit 0 ;;
      esac
    fi
    # Root baseurl (choose what you want your Pages root to be)
    ROOT_BASEURL="${BASE_PAGES_URL}/"
    prepare_and_build_book "$ROOT_DIR" "ROOT" "$ROOT_BASEURL"
    echo "=== Done ==="
    exit 0
  else
    echo "ERROR: --build-root-only requires ROOT_DIR to be a valid book."
    exit 1
  fi
fi

# ---------- Discover books (books/) ----------
BOOK_PATHS=()
BOOK_NAMES=()

for book in "${BOOKS_DIR}"/*; do
  [[ -d "$book" ]] || continue
  [[ -f "$book/_toc.yml" || -f "$book/myst.yml" ]] || continue

  bookname="$(basename "$book")"
  if should_consider_book "$bookname"; then
    BOOK_PATHS+=("$book")
    BOOK_NAMES+=("$bookname")
  fi
done

# Root book is treated like an additional selectable "book" when enabled
if [[ $DO_BUILD_ROOT -eq 1 ]]; then
  BOOK_PATHS+=("$ROOT_DIR")
  BOOK_NAMES+=("ROOT")
fi

if [[ ${#BOOK_PATHS[@]} -eq 0 ]]; then
  echo "No books found to build (after filters)."
  exit 0
fi

# ---------- Preprompt selection (optional) ----------
SELECTED=()

if [[ $DO_PREPROMPT -eq 1 ]]; then
  echo "=== Preprompt: select books to build ==="
  echo "Enter y to include, anything else to skip."
  echo

  for i in "${!BOOK_NAMES[@]}"; do
    bn="${BOOK_NAMES[$i]}"
    read -r -p "Build '${bn}'? [y/N] " ans
    case "${ans:-}" in
      y|Y|yes|YES) SELECTED+=("${BOOK_PATHS[$i]}") ;;
      *) ;;
    esac
  done

  echo
  echo "Selected ${#SELECTED[@]} book(s):"
  for b in "${SELECTED[@]}"; do
    # ROOT_DIR prints as basename of repo; show ROOT instead
    if [[ "$b" == "$ROOT_DIR" ]]; then echo "  - ROOT"; else echo "  - $(basename "$b")"; fi
  done
  echo

else
  SELECTED=("${BOOK_PATHS[@]}")
fi

if [[ ${#SELECTED[@]} -eq 0 ]]; then
  echo "No books selected. Exiting."
  exit 0
fi

# ---------- Ensure ROOT builds first ----------
if [[ ${#SELECTED[@]} -gt 1 ]]; then
  NEW_SELECTED=()
  # Add ROOT first (if present)
  for b in "${SELECTED[@]}"; do
    if [[ "$b" == "$ROOT_DIR" ]]; then
      NEW_SELECTED+=("$b")
      break
    fi
  done
  # Then add everything else, in original order
  for b in "${SELECTED[@]}"; do
    [[ "$b" == "$ROOT_DIR" ]] && continue
    NEW_SELECTED+=("$b")
  done
  SELECTED=("${NEW_SELECTED[@]}")
fi



# ---------- Build ----------
echo "=== Step 1: Build books ==="
for book in "${SELECTED[@]}"; do
  bookname="$(basename "$book")"
  if [[ "$book" == "$ROOT_DIR" ]]; then
    bookname="ROOT"
  fi

  if [[ $DO_PROMPT -eq 1 ]]; then
    read -r -p "Build '${bookname}' now? [y/N] " ans
    case "${ans:-}" in
      y|Y|yes|YES) ;;
      *) echo "---- Skipping (by prompt): ${bookname} ----"; continue ;;
    esac
  fi

  if [[ "$bookname" == "ROOT" ]]; then
    baseurl="${BASE_PAGES_URL}/"
  else
    baseurl="${BASE_PAGES_URL}/${bookname}/"
  fi

  prepare_and_build_book "$book" "$bookname" "$baseurl"
done

echo " -- done part 1 --"

# ---------- Step 2: Bundle non-root book HTML into ROOT site (optional) ----------
if [[ $DO_BUNDLE_SITES -eq 1 ]]; then
  ROOT_SITE="${ROOT_DIR}/_build/html"

  if [[ ! -d "$ROOT_SITE" ]]; then
    echo "=== Step 2: Skipping bundling (ROOT site not found at $ROOT_SITE). Did you build ROOT? ==="
  else
    echo "=== Step 2: Bundling book sites into ROOT site: $ROOT_SITE ==="

    for book in "${SELECTED[@]}"; do
      # Skip ROOT
      if [[ "$book" == "$ROOT_DIR" ]]; then
        continue
      fi

      bookname="$(basename "$book")"
      src="${book}/_build/html"
      dst="${ROOT_SITE}/${bookname}"

      if [[ ! -d "$src" ]]; then
        echo "---- Skipping ${bookname}: no build at $src ----"
        continue
      fi

      echo "---- Copying ${bookname} site into ROOT: /${bookname}/ ----"
      if command -v rsync >/dev/null 2>&1; then
        mkdir -p "$dst"
        rsync -a --delete "${src}/" "${dst}/"
      else
        rm -rf "$dst"
        mkdir -p "$dst"
        cp -a "${src}/." "$dst/"
      fi
    done
  fi
else
  echo "=== Step 2: Skipping bundling (use --bundle-sites to enable) ==="
fi






echo "=== Done ==="
