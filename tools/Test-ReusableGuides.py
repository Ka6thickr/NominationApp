"""Validate current manual package; does not compile Power Fx."""
from pathlib import Path
import ast,re
root=Path(__file__).resolve().parents[1]
tree=ast.parse((root/'tools/Test-ManualGuide.py').read_text(encoding='utf-8'))
scope={}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='balanced'],type_ignores=[]),'<scanner>','exec'),scope)
files=list((root/'production-guide/fx').glob('*.fx'))
for path in files:
    text=path.read_text(encoding='utf-8')
    scope['balanced'](text,str(path))
    assert not re.search(r'(?<!\w)Theme\.',text),path
for path in [root/'Prod.md']+list((root/'production-guide').glob('*.md')):
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
        if not target.startswith(('https:','http:','#')):
            assert (path.parent/target.split('#')[0]).exists(),(path,target)
guides=list((root/'production-guide').glob('scr*.md'))
assert len(guides)==13
for path in guides:
    text=path.read_text(encoding='utf-8')
    assert '## 1. Complete Tree view' in text and 'cmpAppNav' in text
assert '#E20074' in (root/'production-guide/fx/Theme.Initialize.fx').read_text()
assert 'Theme =' not in (root/'production-guide/fx/App.Formulas.fx').read_text()
print(f'PASS: 13 screen trees, component bindings, links and {len(files)} FX delimiter checks. Studio/runtime not tested.')
