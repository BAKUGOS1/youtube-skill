#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATOR="${SKILL_VALIDATOR:-/root/.codex/skills/.system/skill-creator/scripts/quick_validate.py}"

for skill in "$ROOT"/skills/*; do
  python "$VALIDATOR" "$skill"
done

python -m compileall -q "$ROOT/skills"
