"""Structural validation, not a Power Fx compiler or runtime test."""
from pathlib import Path
import ast
import re

root=Path(__file__).resolve().parents[1]
# Reuse the existing delimiter scanner without executing unrelated guide tests.
tree=ast.parse((root/'tools/Test-ManualGuide.py').read_text(encoding='utf-8'))
function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='balanced')
scope={}
exec(compile(ast.Module(body=[function],type_ignores=[]),'<scanner>','exec'),scope)
text=(root/'Prod.md').read_text(encoding='utf-8')
blocks=re.findall(r'```powerfx\s*\n(.*?)```',text,re.S)
for i,block in enumerate(blocks): scope['balanced'](block,f'Prod block {i+1}')
for old in ['IndividualInnovation','IndividualCustomer','IndividualExcellence','TeamCollaboration','TeamImpact','TeamTransformation']:
    for prefix in ('Nom_','scr','frm'):
        assert prefix+old not in text,(prefix,old)
for name,p in [('BestInnovatorIndividual','II'),('MDAward','IC'),('TrendMarcherAward','IE'),('BestInnovatorTeam','TC'),('MDAwardTeam','TI'),('SpecialTeamAward','TT')]:
    assert f'Form DataSource = `{name}`; Item = `varRecord{p}`' in text
    assert f'Set(varRecord{p}, Defaults({name}))' in text
    assert f'Patch({name}, varRecord{p},' in text
    assert f'frm{name}.OnSuccess' in text and f'frm{name}.OnFailure' in text
    for slot in range(1,7):
        assert f'`txt{p}Q{slot}.Default`' in text
        assert f'`err{p}Q{slot}`' in text
assert 'varIsAdmin' not in text
assert 'three configured questions' in text
for p in ['II','IC','IE','TC','TI','TT','Home','Details','Category','Review','Confirmation','Mine','Admin']:
    for name in ['cntScroll','cntPage','cntHeader','cntNav','cntStepperStrip','cntActions','btnNavNew','btnNavMine','btnStartNew','btnGoMine','cntExitOverlay','btnExitCancel','btnExitDiscard','cntBusy']:
        assert name+p in text,(p,name)
    assert f'<a id="build-{p.lower()}"' in text
headings=re.findall(r'^#+ (.+)$',text,re.M)
slugs={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in headings}
slugs.update(re.findall(r'<a id="([^"]+)"',text))
for link in re.findall(r'\]\(([^)]+)\)',text):
    if link.startswith('#'): assert link[1:] in slugs,link
    elif not link.startswith(('https:','http:')): assert (root/link).exists(),link
print(f'PASS: {len(blocks)} fenced Power Fx blocks balanced; six typed mappings, 36 slot recipes, event coverage and links verified.')
print('NOT TESTED: Studio compilation, live connectors, rendered layout, permissions or runtime.')
