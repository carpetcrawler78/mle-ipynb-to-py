# Install nbcommands if not already installed
if ! command -v nbgrep &> /dev/null; then
    echo "nbcommands is not installed. Installing..."
    pip install nbcommands
fi

# Path for the output Python file
mkdir -p ./.github/workflows/testing
touch ./.github/workflows/testing/test_import_libraries.py
PYTHON_FILE="./.github/workflows/testing/test_import_libraries.py"

# Remove the output file if it already exists
rm -f "$PYTHON_FILE"

# One improved regex used for BOTH notebooks and .py files
NB_REGEX='(?m)^\s*(?:from\s+[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*\s+import\s+\(?\s*(\*|[A-Za-z_]\w*(?:\s+as\s+[A-Za-z_]\w*)?(?:\s*,\s*[A-Za-z_]\w*(?:\s+as\s+[A-Za-z_]\w*)?)*)\s*\)?|import\s+[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*(?:\s+as\s+[A-Za-z_]\w*)?(?:\s*,\s*[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*(?:\s+as\s+[A-Za-z_]\w*)?)*)\s*(?:#.*)?$'

# Search for *.ipynb and *.py recursively, skipping common virtual-env folders
find . \
  -type d \( -name '.venv' -o -name 'venv' -o -name 'env' -o -name '.env' \) -prune -false \
  -o -type f \( -name '*.ipynb' -o -name '*.py' \) -print0 |
while IFS= read -r -d '' file; do
  if [[ "$file" == *.ipynb ]]; then
    nbgrep "$NB_REGEX" "$file" \
      | grep -v 'nbgrep:' \
      | awk -F ':' '{sub(/^[^:]*:[^:]*:line [0-9]+:/, " ", $0)}1' \
      | sed 's/^[[:space:]]*//' \
      | grep -E '^(from|import)\b'
  else
    python - "$file" "$NB_REGEX" <<'PY'
import re, sys, pathlib
path = pathlib.Path(sys.argv[1])
pattern = sys.argv[2]
try:
    text = path.read_text(encoding="utf-8", errors="ignore")
except Exception:
    sys.exit(0)
rx = re.compile(pattern, re.MULTILINE | re.DOTALL)
for m in rx.finditer(text):
    line = m.group(0).strip()
    line = re.sub(r"[ \t]*\n[ \t]*", " ", line)  # flatten (...) blocks
    if line.startswith(("import ", "from ")):
        print(line)
PY
  fi
done \
| sed -E 's/[[:space:]]+/ /g' \
| sed -E '/^[[:space:]]*#/d' \
| sed -E '/^[[:space:]]*$/d' \
| sort -u > "$PYTHON_FILE"

echo "<<<<<<< All extracted import statements from notebooks and Python scripts >>>>>>"
cat "$PYTHON_FILE"

# Generate test function
echo "" >> "$PYTHON_FILE.tmp"

# >>> Add this preamble so 'src' (a directory) can be imported as a top-level package
echo "import os, sys" >> "$PYTHON_FILE.tmp"
echo "THIS_DIR = os.path.dirname(__file__)" >> "$PYTHON_FILE.tmp"
echo "REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, os.pardir, os.pardir, os.pardir))" >> "$PYTHON_FILE.tmp"
echo "if REPO_ROOT not in sys.path: sys.path.insert(0, REPO_ROOT)" >> "$PYTHON_FILE.tmp"
echo "" >> "$PYTHON_FILE.tmp"
# <<<

echo "def test_import_libraries():" >> "$PYTHON_FILE.tmp"
echo "    try:" >> "$PYTHON_FILE.tmp"
grep "import" "$PYTHON_FILE" | sed 's/^/        /' >> "$PYTHON_FILE.tmp"
echo "    except ImportError as e:" >> "$PYTHON_FILE.tmp"
echo "        assert False, f\"Failed to import library: {e}\"" >> "$PYTHON_FILE.tmp"
echo "" >> "$PYTHON_FILE.tmp"
echo "    assert True" >> "$PYTHON_FILE.tmp"

mv "$PYTHON_FILE.tmp" "$PYTHON_FILE"
cat "$PYTHON_FILE"
