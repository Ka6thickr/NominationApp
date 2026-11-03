"""Local structural checks only; not a Power Fx parser or Canvas runtime test."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'documentation2/manual-build'
rows = [
    ('IND_INNOVATION','II','IndividualInnovation',False),
    ('IND_CUSTOMER','IC','IndividualCustomer',False),
    ('IND_EXCELLENCE','IE','IndividualExcellence',False),
    ('TEAM_COLLAB','TC','TeamCollaboration',True),
    ('TEAM_IMPACT','TI','TeamImpact',True),
    ('TEAM_TRANSFORM','TT','TeamTransformation',True),
]

def balanced(source, context):
    stack = []
    i = 0
    while i < len(source):
        char = source[i]
        if source[i:i+2] == '//':
            end = source.find('\n', i)
            i = len(source) if end == -1 else end+1
            continue
        if char in ('"', "'"):
            quote = char
            i += 1
            while i < len(source):
                if source[i] == quote:
                    if i+1 < len(source) and source[i+1] == quote:
                        i += 2
                        continue
                    break
                i += 1
            assert i < len(source), f'{context}: unterminated quoted string/identifier'
        elif char in '({[':
            stack.append(char)
        elif char in ')}]':
            assert stack and stack.pop() == {')':'(', '}':'{', ']':'['}[char], f'{context}: unmatched {char}'
        i += 1
    assert not stack, f'{context}: unclosed {stack}'

checks = 0
files = list(OUT.glob('*.md')) + list(OUT.glob('*.fx'))
assert len(files) >= 20
for path in files:
    content = path.read_text(encoding='utf-8')
    assert not re.search(r'@(CODE|P|SUFFIX|DS|TYPE|ANSWERS|IDENTITY|INTENT)@', content), path.name
    if path.suffix == '.fx':
        balanced(content, path.name)
        checks += 1
    else:
        for index, block in enumerate(re.findall(r'```powerfx\s*\n(.*?)```', content, re.S)):
            balanced(block, f'{path.name} block {index+1}')
            checks += 1
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if not re.match(r'https?://|#', target):
                assert (path.parent / target).exists(), f'{path.name}: missing link {target}'

common = {'Title','Category','QuestionSetVersion','QuestionCount','NominatedBy','NominatorEmail',
          'EmployeeRole','EmployeeLevel','NominationStatus','DeclarationAccepted','SubmittedOn'}
qfields = {f'Q{n}{suffix}' for n in range(1,7) for suffix in ('PromptSnapshot','RequiredSnapshot','Response')}
source_names = {'IND_INNOVATION': 'MDAward', 'IND_CUSTOMER': 'TrendMarcherAward', 'IND_EXCELLENCE': 'BestInnovatorIndividual', 'TEAM_COLLAB': 'MDAwardTeam', 'TEAM_IMPACT': 'BestInnovatorTeam', 'TEAM_TRANSFORM': 'SpecialTeamAward'}
for code,p,s,team in rows:
    content = (OUT / f'Form-{code}.md').read_text(encoding='utf-8')
    actual = set(re.findall(r'^\| `([^`]+)` / `dc', content, re.M))
    expected = common | qfields | ({'TeamName','TeamPrimaryContact','TeamMembers'} if team else {'NominatedEmployee'})
    assert actual == expected, (code, actual ^ expected)
    assert f'Form DataSource = `{source_names[code]}`' in content
    assert f'SubmitForm(frm{s})' in content
    assert f'Patch({source_names[code]}, varRecord{p},' in content
    assert f'Set(varRecord{p}, frm{s}.LastSubmit)' in content
    for n in range(1,7):
        assert f'`txt{p}Q{n}.Default`' in content
        assert f'`dc{p}Q{n}Response.Visible`' in content
    assert f'`att{p}.Attachments`' in content
    assert f'ViewForm(frm{s})' in content

submit = (OUT / 'Review.Submit.OnSelect.fx').read_text(encoding='utf-8')
assert 'Patch(' not in submit, 'Final status Patch must stay in form OnSuccess'
for code,p,s,team in rows:
    assert submit.count(f'SubmitForm(frm{s})') == 1

admin = (OUT / 'Admin.Publish.OnSelect.fx').read_text(encoding='utf-8')
assert admin.index('ClearCollect(colAdminSaved') < admin.index('Patch(AwardCategories')
assert 'Remove(' not in admin and 'RemoveIf(' not in admin
assert 'Patch(AwardQuestions, Defaults(AwardQuestions)' in admin

onstart = (OUT / 'App.OnStart.fx').read_text(encoding='utf-8')
assert '00000000-0000-0000-0000-000000000000' in onstart
assert 'Char(9)' in (OUT / 'App.Formulas.fx').read_text(encoding='utf-8')
stepper = (ROOT / 'documentation2/Process-Stepper-Component.md').read_text(encoding='utf-8')
for index, block in enumerate(re.findall(r'```powerfx\s*\n(.*?)```', stepper, re.S)):
    balanced(block, f'stepper block {index+1}')
    checks += 1

print(f'PASS: {len(files)} manual files; {checks} formula blocks checked for balanced delimiters/quotes.')
print('PASS: local links, six typed source routes, complete fixed-schema Update maps, 36 question-control recipes.')
print('PASS: status Patch occurs after form success; admin pointer publication follows saved-set validation.')
print('NOT TESTED: Power Fx compilation/types, actual Canvas controls, connector calls, UI rendering or runtime behavior.')
