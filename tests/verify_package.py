"""Validate package structure, references and executable helper; no model run."""
from pathlib import Path
import ast
import re

root = Path(__file__).resolve().parents[1]
skill = root / 'universal-orchestrator'
body = (skill / 'SKILL.md').read_text(encoding='utf-8')
assert body.startswith('---\n')
assert re.search(r'^name: universal-orchestrator$', body, re.M)
assert '[TODO' not in body
for ref in re.findall(r'\]\((references/[^)]+)\)', body):
    assert (skill / ref).is_file(), ref
    (skill / ref).read_text(encoding='utf-8')
ui = (skill / 'agents/openai.yaml').read_text(encoding='utf-8')
assert '$universal-orchestrator' in ui
helper = skill / 'scripts/resolve_models.py'
ast.parse(helper.read_text(encoding='utf-8'))
assert (root / 'install.ps1').is_file()
assert not (root / 'config-snippet.toml').exists(), 'Fixed global model config present'
assert not (root / 'codex-agents').exists(), 'Fixed agent profiles present'
print('OK: metadata, linked references, UTF-8 and helper syntax')
