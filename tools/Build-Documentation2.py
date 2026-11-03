"""Build the standalone manual rebuild package without changing live resources."""
from pathlib import Path
import json
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'documentation2'
MAPPING = dict(zip(
    ['Nom_IndividualInnovation','Nom_IndividualCustomer','Nom_IndividualExcellence',
     'Nom_TeamCollaboration','Nom_TeamImpact','Nom_TeamTransformation'],
    ['MDAward','TrendMarcherAward','BestInnovatorIndividual','MDAwardTeam','BestInnovatorTeam','SpecialTeamAward']))
CODES = ['IND_INNOVATION','IND_CUSTOMER','IND_EXCELLENCE','TEAM_COLLAB','TEAM_IMPACT','TEAM_TRANSFORM']

def convert(text):
    for old, new in MAPPING.items():
        text = text.replace(old, new)
    return text

def write(path, text):
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.strip() + '\n', encoding='utf-8')

for source in (ROOT/'documentation/manual-build').iterdir():
    if source.suffix in ('.md','.fx'):
        text = convert(source.read_text(encoding='utf-8'))
        text = text.replace('The SharePoint backend is provisioned; these instructions are the next stage.',
                            'For this new setup, first create and verify all eight lists using ../00-SharePoint-Manual-Setup.md.')
        text = text.replace('No app has yet been created there by this guide.',
                            'This package describes a fresh manual build. Inspect existing solutions first and choose a distinct development solution/app name if retaining the earlier scaffold.')
        text = text.replace('../../provisioning/', '../provisioning/')
        text = text.replace('Use the target list GUIDs from `provisioning/deployment-result.json` (not title text) as the list environment-variable values.', 'For manually created lists, obtain each new list GUID from its List settings URL (the List query parameter) or the connector list picker. Use the actual target list GUID, not an old deployment result or title text, for each list environment-variable value.')
        write('manual-build/'+source.name, text)
for name in ['Process-Stepper-Component.md','PowerApps-Screen-Plan.md']:
    write(name, convert((ROOT/'documentation'/name).read_text(encoding='utf-8')))
for name in ['environment.json','seed-data.json','Provision-NominationLists.ps1','Test-Provisioning.ps1','README.md']:
    write('provisioning/'+name, convert((ROOT/'provisioning'/name).read_text(encoding='utf-8')))
provisioning_readme = OUT/'provisioning/README.md'
provisioning_readme.write_text(provisioning_readme.read_text() + '\nRun the commands above with documentation2 as your working directory, so they use this package\'s new list configuration. Manual setup does not produce deployment-result.json; record the new list GUIDs yourself if not running provisioning.\n', encoding='utf-8')

config = json.loads((OUT/'provisioning/environment.json').read_text())
schema = json.loads((OUT/'schema.json').read_text(encoding='utf-8-sig'))
mapping_table = '| Category code (retain) | New list / Power Fx source |\n|---|---|\n' + '\n'.join(
    f'| `{code}` | `{name}` |' for code, name in zip(CODES,MAPPING.values()))
intro = '''# Nomination App — fresh manual setup, version 2

This package supersedes the old list-name references for your new manual build. It does not rename or create live lists, migrate records, or modify the existing Canvas app. All runtime tests remain pending. Keep the original columns and Contoso branding; three question tags remain deferred.

## List mapping

The new list names are assigned in the order supplied. Category codes, screen names, control names and variable names remain stable. A list name does not change the category's displayed title or question wording; maintain those in AwardCategories and AwardQuestions. In particular, BestInnovatorIndividual currently routes through the existing IND_EXCELLENCE contract, and BestInnovatorTeam through TEAM_IMPACT. Review the provisional seed wording before activation.

''' + mapping_table + '''

Configuration lists remain `AwardCategories` and `AwardQuestions`. Use the exact spelling `TrendMarcherAward`.

## Build from beginning to end

1. [Create all lists and columns, then configure questions](00-SharePoint-Manual-Setup.md).
2. [Create solution, Canvas app, connections and shared state](manual-build/README.md).
3. [Build screens and layout](manual-build/01-Screens-and-Layout.md), then the [dynamic SVG/HTML stepper](Process-Stepper-Component.md).
4. [Build nominee details and dynamic category loading](manual-build/02-Details-and-Categories.md).
5. [Apply six typed form mappings](manual-build/Form-Mapping.md), following each of the six complete Form-*.md recipes.
6. [Build review, submission, My nominations and administration](manual-build/03-Review-Browse-and-Administration.md).
7. [Run validation and handover checks](manual-build/04-Validation-and-Handover.md). Publish only after the applicable tests and permissions checks pass.

For GitHub Copilot Chat use [the complete standalone guide](GitHub-Copilot-App-Guide.md). All shared formulas are also individual `.fx` files under `manual-build`; form-specific formulas are in their six `.md` recipes.

## One-place configuration and formula identifiers

`provisioning/environment.json` is the single physical site/list configuration for provisioning. All formulas in this package reference the new source names directly. A text variable cannot dynamically select a SharePoint data source for a typed form. For later environment moves, configure solution SharePoint site/list data-source environment variables and bind the sources through them, keeping app source identifiers stable. Do not simply change a string in App.OnStart and expect connections to move.

The optional PowerShell files are provided for reproducibility; the manual creation instructions are complete without running them. Do not rerun old generators into this package; regenerate with tools/Build-Documentation2.py if needed.

## Completion log

| Stage | State |
|---|---|
| New mapping and manual package | Prepared; local structural checks only |
| New lists and configuration data | User manual creation pending |
| New solution, app and screen design | User manual creation pending |
| Power Fx compilation and runtime tests | Pending |
| Publication | Pending |
'''
write('README.md',intro)

setup = '''# 00 — Manually create SharePoint lists and columns

## 1. Create the eight lists

Open https://5v7nf4.sharepoint.com/sites/AISite/ → Settings → Site contents → New → List → Blank list. Enter each exact list name below. Create AwardCategories first, AwardQuestions second, then the six nomination lists. If a configuration list already exists, verify its schema instead of creating a duplicate. Do not delete or rename the previous nomination lists for this fresh setup.

''' + mapping_table + '''

Also create/verify `AwardCategories` and `AwardQuestions`.

For each list, Settings → List settings → Columns → Create column. Enter the exact internal name shown in the tables on initial creation, with no spaces. Keep that display name too so the supplied formulas match. If an incorrect internal name was created, a display-name rename will not fix it; inspect the Field parameter in its column-settings URL before proceeding.

`Title` already exists: edit it instead of creating another Title column. ID, Created, Modified, Created By and Modified By are built in; do not recreate them. Attachments is the built-in list attachment feature, not a custom column.

## 2. Column type settings

- Text: Single line of text, maximum 255 characters, default blank unless listed.
- Note: Multiple lines of text, Plain text, append changes No; do not use rich text. Keep list validation empty. The app applies its answer length rules.
- Number: Number with zero decimal places; leave default blank unless listed.
- Choice: single-select Drop-down menu, exact choices below, fill-in choices No. Explicitly clear any automatically selected default except NominationStatus = Draft.
- Boolean: Yes/No; set the table's default.
- Lookup: Lookup to AwardCategories, display Title, single value, no additional lookup fields, no enforced relationship deletion behavior.
- User: Person or Group, People Only, allow multiple selections No. UserMulti: same with multiple selections Yes.
- DateTime: Date and Time, include time, no default.
- Required, unique and indexed settings must match the table. Unique columns automatically require an index. For other indexed columns use List settings → Indexed columns → Create a new index.

Do not add mandatory validation to nomination columns: incomplete drafts must save. The app enforces required questions at submission.

## 3. Exact schema for every list

'''
for key, fields in schema.items():
    name = config['Lists'][key]
    setup += f'### {name}\n\n| Internal / display name | Type | Required | Default / choices | Indexed | Unique |\n|---|---|---|---|---|---|\n'
    for field in fields:
        detail = ', '.join(field.get('Choices', []))
        if 'Default' in field:
            default = field['Default']
            if field['Type']=='Boolean': default = 'Yes' if str(default)=='1' else 'No'
            detail += ('; ' if detail else '') + f'Default: {default}'
        setup += f"| `{field['Name']}` | {field['Type']} | {'Yes' if field['Required'] else 'No'} | {detail or 'Blank'} | {'Yes' if field['Indexed'] else 'No'} | {'Yes' if field['Unique'] else 'No'} |\n"
    setup += '\n'
setup += '''## 4. List-level settings

1. All eight lists: List settings → Versioning settings → create a version each time an item is edited = Yes. Content approval = No for this design.
2. Six nomination lists: Advanced settings → Attachments = Enabled; read access = Read items that were created by the user; create/edit access = Create items and edit items that were created by the user. These settings do not restrict site owners and do not make Submitted records immutable. If server-enforced submission locking is required, implement and test an approved backend permission workflow before production.
3. Six nomination lists: add an index for Modified, in addition to NominatorEmail and NominationStatus specified above. ID already has a built-in index.
4. Configuration lists: grant normal app users Read and configuration administrators the necessary edit permissions. Test with ordinary accounts. Hiding an admin screen is not security. Configure the administrator identity in App.OnStart; its all-zero placeholder intentionally grants nobody admin UI access.
5. Leave extra custom validation and required fields off. Do not add the future question tags.
6. Verify 194 custom columns total: AwardCategories 6, AwardQuestions 8, each individual list 29, each team list 31. These counts exclude built-in Title. Tables include Title for its required setting.

## 5. Configure dynamic categories and questions manually

1. In AwardCategories create six rows using the CategoryCode/list mapping above; set AwardType to Individual or Team as appropriate. Set Title and Description to approved business-facing content, DisplayOrder to 1–6, IsActive = No, PublishedQuestionVersion blank. List names are storage identifiers, not approved category copy.
2. The optional `provisioning/seed-data.json` contains the prior prototype's provisional category and question content. Review it before using it with the newly named awards. Do not assume old innovation/customer/excellence wording matches the new business awards.
3. In AwardQuestions create 3–6 rows per category for version 1. Category selects the matching AwardCategories item, QuestionSetVersion = 1, QuestionKey = Q1 through Qn, DisplayOrder = 1 through n, Title = approved criterion heading, QuestionText = full approved question, GuidanceText = optional guidance, IsRequired = approved Yes/No. No synthetic people or nomination rows are needed.
4. Set ConfigurationKey exactly to `<CategoryCode>-V1-Q<slot>`, for example `IND_INNOVATION-V1-Q1`. For version 2 use `IND_INNOVATION-V2-Q1`. Every key must be unique. This format matches the administration formulas.
5. Read back every row. Confirm correct lookup, one row per slot, contiguous Q1–Qn, nonempty title and question, and the same version number. After content approval set that category's PublishedQuestionVersion = 1 and IsActive = Yes. Until this step category selection is intentionally empty.
6. Later changes use a new complete version; retain old rows. Update PublishedQuestionVersion only after verifying the new set. Saved nominations retain their original question snapshots.

## 6. Connect the new Canvas app

Create the solution and app using `manual-build/README.md`. Add SharePoint connection for this site and all eight exact lists. Verify their Data pane identifiers match the names in this package. Add Office365Users. Create every referenced screen and form before setting shared formulas. Use the existing screen/control identifiers even where they contain the previous category terminology.

For deployment across environments, create Data Source environment variables for the SharePoint site and each list within the solution, then use the Advanced connection selection to bind those variables. Validate each target list's column types/internal names before switching. A new list title alone does not migrate existing records or attachments.

## Sources

- [Microsoft: create list columns](https://support.microsoft.com/en-us/sharepoint/lists/data-and-lists/create-a-column-in-a-list-or-library)
- [Microsoft: column types and options](https://support.microsoft.com/en-us/sharepoint/lists/data-and-lists/list-and-library-column-types-and-options)
- [Microsoft: Canvas data-source environment variables](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables-data-source-canvas-apps)
'''
write('00-SharePoint-Manual-Setup.md',setup)

oldguide = convert((ROOT/'documentation/GitHub-Copilot-App-Guide.md').read_text(encoding='utf-8'))
embedded = oldguide[oldguide.index('# Embedded manual:'):]
# Rebuild embedded text from updated files to eliminate historical setup claims.
parts = ['# GitHub Copilot Chat — full manual rebuild guide\n\n'
         'Read this file completely. Build a fresh SharePoint-backed Canvas app using the exact list mapping below. '
         'Treat referenced documents as specifications, not executable instructions. Preserve all columns. '
         'Provide precise screen/control/property formulas at each stage. Verify actual Studio types, resolve errors, '
         'and record checkpoints before continuing. Never claim runtime validation from structural checks alone.\n\n', intro, setup]
for match in re.finditer(r'# Embedded manual: ([^\n]+)', embedded):
    name = match.group(1).strip()
    path = OUT/'manual-build'/name
    if path.exists():
        content = path.read_text(encoding='utf-8')
        content = re.sub(r'\]\(([^)]+)\)', lambda m: m.group(0) if m[1].startswith(('https:','http:','#')) else '](manual-build/'+m[1]+')', content)
        parts.append(f'\n\n---\n\n# Embedded manual: {name}\n\n'+content)
parts.append('\n\n# Full process stepper\n\n'+(OUT/'Process-Stepper-Component.md').read_text())
for path in sorted((OUT/'manual-build').glob('*.fx')):
    parts.append(f'\n\n## {path.name}\n\n```powerfx\n'+path.read_text()+'```\n')
write('GitHub-Copilot-App-Guide.md','\n'.join(parts))

# Use the existing structural checker against the new package and source names.
test = (ROOT/'tools/Test-ManualGuide.py').read_text()
test = test.replace("ROOT / 'documentation/manual-build'", "ROOT / 'documentation2/manual-build'")
test = test.replace("ROOT / 'documentation/Process-Stepper-Component.md'", "ROOT / 'documentation2/Process-Stepper-Component.md'")
test = test.replace("for code,p,s,team in rows:\n", 'source_names = '+repr(dict(zip(CODES,MAPPING.values())))+'\nfor code,p,s,team in rows:\n',1)
test = test.replace('Nom_{s}', '{source_names[code]}')
(ROOT/'tools/Test-Documentation2.py').write_text(test, encoding='utf-8')
for path in OUT.rglob('*'):
    if path.suffix in ('.md','.fx','.json','.ps1'):
        assert not any(old in path.read_text(encoding='utf-8-sig') for old in MAPPING), path
    if path.suffix == '.md':
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if not target.startswith(('http:', 'https:', '#')):
                assert (path.parent/target).exists(), (path, target)
with zipfile.ZipFile(OUT/'NominationApp-Manual-Setup.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.suffix != '.zip':
            archive.write(path, path.relative_to(OUT))
print('Built documentation2: full schema, renamed recipes, standalone Copilot guide and ZIP.')
