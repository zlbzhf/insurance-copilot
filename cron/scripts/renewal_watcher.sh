#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

WORKSPACE=""
AS_OF=""
MODE="alert-only"
FORMAT="markdown"
OUTPUT=""

usage() {
  cat >&2 <<'USAGE'
Usage: cron/scripts/renewal_watcher.sh --workspace PATH --as-of YYYY-MM-DD [--mode always|alert-only] [--format markdown|json] [--output PATH]

Script-only Hermes cron wrapper for local renewal watcher.
- stdout by default
- empty stdout in alert-only mode when there are no review-worthy rows
- non-zero exit for broken configuration
- never writes output inside the private workspace
USAGE
}

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

run_or_fail() {
  local label="$1"
  shift
  local log_file="$TMP_DIR/${label// /_}.log"
  if ! "$@" >"$log_file" 2>&1; then
    printf 'ERROR: %s failed\n' "$label" >&2
    sed 's/^/  /' "$log_file" >&2
    exit 1
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace)
      [[ $# -ge 2 ]] || fail "--workspace requires a path"
      WORKSPACE="$2"
      shift 2
      ;;
    --as-of)
      [[ $# -ge 2 ]] || fail "--as-of requires YYYY-MM-DD"
      AS_OF="$2"
      shift 2
      ;;
    --mode)
      [[ $# -ge 2 ]] || fail "--mode requires always or alert-only"
      MODE="$2"
      shift 2
      ;;
    --format)
      [[ $# -ge 2 ]] || fail "--format requires markdown or json"
      FORMAT="$2"
      shift 2
      ;;
    --output)
      [[ $# -ge 2 ]] || fail "--output requires a path"
      OUTPUT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "unknown argument: $1"
      ;;
  esac
done

[[ -n "$WORKSPACE" ]] || fail "workspace missing: pass --workspace PATH"
[[ -n "$AS_OF" ]] || fail "as-of date missing: pass --as-of YYYY-MM-DD"
[[ "$MODE" == "always" || "$MODE" == "alert-only" ]] || fail "invalid mode: $MODE"
[[ "$FORMAT" == "markdown" || "$FORMAT" == "json" ]] || fail "invalid format: $FORMAT"
[[ -d "$WORKSPACE" ]] || fail "workspace missing: $WORKSPACE"

WORKSPACE_ABS="$(python3 - "$WORKSPACE" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).expanduser().resolve())
PY
)"

TMP_ROOT="${TMPDIR:-/tmp}"
TMP_ROOT_ABS="$(python3 - "$TMP_ROOT" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).expanduser().resolve())
PY
)"
python3 - "$WORKSPACE_ABS" "$TMP_ROOT_ABS" <<'PY' || fail "TMPDIR must be outside workspace: $TMP_ROOT_ABS"
from pathlib import Path
import sys
workspace = Path(sys.argv[1])
tmp_root = Path(sys.argv[2])
try:
    tmp_root.relative_to(workspace)
except ValueError:
    raise SystemExit(0)
raise SystemExit(1)
PY

if [[ -n "$OUTPUT" ]]; then
  OUTPUT_ABS="$(python3 - "$OUTPUT" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).expanduser().resolve())
PY
)"
  python3 - "$WORKSPACE_ABS" "$OUTPUT_ABS" <<'PY' || fail "output path must be outside workspace: $OUTPUT_ABS"
from pathlib import Path
import sys
workspace = Path(sys.argv[1])
output = Path(sys.argv[2])
try:
    output.relative_to(workspace)
except ValueError:
    raise SystemExit(0)
raise SystemExit(1)
PY
fi

TMP_DIR="$(mktemp -d "$TMP_ROOT_ABS/insurance-renewal-cron.XXXXXX")"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

BUNDLE="$TMP_DIR/workbench-bundle.json"
ALERT_JSON="$TMP_DIR/renewal-alert.json"
ALERT_RENDERED="$TMP_DIR/renewal-alert.${FORMAT}"

run_or_fail "local file connector" \
  python3 "$ROOT/scripts/local_file_connectors.py" daily-workbench \
    --workspace "$WORKSPACE_ABS" \
    --format json \
    --output "$BUNDLE"

run_or_fail "renewal watcher" \
  python3 "$ROOT/scripts/renewal_watcher.py" \
    --bundle "$BUNDLE" \
    --workspace "$WORKSPACE_ABS" \
    --as-of "$AS_OF" \
    --format json \
    --output "$ALERT_JSON"

SHOULD_PRINT="1"
if [[ "$MODE" == "alert-only" ]]; then
  SHOULD_PRINT="$(python3 - "$ALERT_JSON" <<'PY'
import json, sys
from pathlib import Path
payload = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
actionable = [a for a in payload.get('alerts', []) if a.get('bucket') != 'monitor']
print('1' if actionable else '0')
PY
)"
fi

if [[ "$SHOULD_PRINT" != "1" ]]; then
  exit 0
fi

if [[ "$FORMAT" == "json" ]]; then
  if [[ -n "$OUTPUT" ]]; then
    cp "$ALERT_JSON" "$OUTPUT_ABS"
  else
    cat "$ALERT_JSON"
  fi
else
  run_or_fail "renewal watcher markdown render" \
    python3 "$ROOT/scripts/renewal_watcher.py" \
      --bundle "$BUNDLE" \
      --workspace "$WORKSPACE_ABS" \
      --as-of "$AS_OF" \
      --format markdown \
      --output "$ALERT_RENDERED"
  if [[ -n "$OUTPUT" ]]; then
    cp "$ALERT_RENDERED" "$OUTPUT_ABS"
  else
    cat "$ALERT_RENDERED"
  fi
fi
