"""Review supplied source snapshots and assemble the current production build recipe."""
from pathlib import Path
import re
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT/'production-review'
CHANGES = (INPUT/'Changes.md').read_text(encoding='utf-8-sig')
ROWS = [
    ('IND_INNOVATION','II','IndividualInnovation','BestInnovatorIndividual'),
    ('IND_CUSTOMER','IC','IndividualCustomer','MDAward'),
    ('IND_EXCELLENCE','IE','IndividualExcellence','TrendMarcherAward'),
    ('TEAM_COLLAB','TC','TeamCollaboration','BestInnovatorTeam'),
    ('TEAM_IMPACT','TI','TeamImpact','MDAwardTeam'),
    ('TEAM_TRANSFORM','TT','TeamTransformation','SpecialTeamAward')]

def remap(text):
    for code,prefix,old,new in ROWS:
        for start in ('Nom_','scr','frm'):
            text = text.replace(start+old, new if start=='Nom_' else start+new)
    return text

def controls(text):
    """Read only serialized control/property blocks; not a general YAML parser."""
    lines = text.splitlines()
    result = {}
    for i,line in enumerate(lines):
        match = re.match(r'^(\s*)- (\w+):\s*$',line)
        if not match: continue
        indent = len(match[1]); name = match[2]
        props = {}; j=i+1
        while j<len(lines) and (not lines[j].strip() or len(lines[j])-len(lines[j].lstrip())>indent):
            if lines[j].strip()=='Children:': break
            prop = re.match(r'^\s+(\w+): (.*)$',lines[j])
            if prop:
                value=prop[2]; k=j+1
                if value in ('|-','|','>-','>'):
                    base=len(lines[j])-len(lines[j].lstrip())
                    values=[]
                    while k<len(lines) and (not lines[k].strip() or len(lines[k])-len(lines[k].lstrip())>base):
                        values.append(lines[k].strip()); k+=1
                    value='\n'.join(values); j=k-1
                props[prop[1]]=value
            j+=1
        result[name]={'line':i+1,'props':props}
    return result

def norm(value):
    return re.sub(r'\s+','',re.sub(r'//[^\n]*','',value)).lstrip('=')

audit=['## Independent review of supplied screen exports\n',
       'Source evidence is retained under production-review. Line references below identify the supplied snapshots, not the target recipes. Missing serialization is reported as unverified; defaults and live behavior were not inspected. Both supplied files contain a Screens root and OnVisible = Set(varCurrentStep, 3). The Changes.md statement that the II file is form-only is outdated.\n']
for code,p,old,new in ROWS[:2]:
    filename='scr'+new+'.txt'; text=(INPUT/filename).read_text(encoding='utf-8-sig')
    items=controls(text); form=items['frm'+new]['props']
    cards={n:v for n,v in items.items() if v['props'].get('Control','').startswith('TypedDataCard')}
    fields={v['props']['DataField'].lstrip('=').strip('"') for v in cards.values()}
    expected={'Title','Category','QuestionSetVersion','QuestionCount','NominatedBy','NominatorEmail','EmployeeRole','EmployeeLevel','NominationStatus','DeclarationAccepted','SubmittedOn','NominatedEmployee','{Attachments}'}|{f'Q{i}{s}' for i in range(1,7) for s in ('PromptSnapshot','RequiredSnapshot','Response')}
    assert fields==expected,(new,fields^expected)
    assert norm(form['DataSource'])==new and norm(form['Item'])=='varRecord'+p
    start=CHANGES.index('### '+new+':')
    end=CHANGES.find('\n### ',start+5)
    recipe=CHANGES[start:end if end!=-1 else None]
    updates=re.findall(r'^\| `[^`]+` / `(dc\w+)` \| `([^`]+)` \|',recipe,re.M)
    for name,value in updates:
        assert norm(items[name]['props']['Update'])==norm(value),(name,'Update mismatch')
    assert norm(items['dc'+p+'Attachments']['props']['Update'])=='att'+p+'.Attachments'
    audit.append(f'### {new}\n\nVerified {len(items)} controls, {len(cards)} cards, exact expected DataField set and {len(updates)} field Update mappings against the supplied target recipe. Native attachment Update also matches.\n\n| Control / property | Observed export | Required correction / verification |\n|---|---|---|')
    def finding(name,prop,fix):
        item=items[name]; value=item['props'].get(prop,'Not serialized')
        value=value.replace('|','\\|').replace('\n',' ')
        audit.append(f'| `{name}.{prop}` (line {item["line"]}) | `{value}` | {fix} |')
    for prop in ('OnSuccess','OnFailure'):
        finding('frm'+new,prop,'Apply the complete event recipe below before enabling save/submit.')
    finding('frm'+new,'Width','Bind to the original responsive page/sidebar layout below.')
    for i in range(1,7):
        txt=f'txt{p}Q{i}'; heading=f'lbl{p}Q{i}Heading'; counter=f'lbl{p}Q{i}Counter'
        if p=='II':
            finding(txt,'Y',f'Use lbl{p}Q{i}Prompt.Y + lbl{p}Q{i}Prompt.Height + 18.')
            finding(txt,'Height','Use If(App.Width <= 760, 180, 142).')
        else:
            finding(heading,'Text','Use this slot for both dynamic title and required marker; see exact recipe.')
            if i>1: finding(counter,'Y',f'Use {txt}.Y + {txt}.Height + 6.')
        finding(txt,'DelayOutput','Explicitly verify false in Studio; omission alone is not a defect.')
    for prop in ('OnAddFile','OnRemoveFile','OnUndoRemoveFile'):
        finding('att'+p,prop,'Set varHasChanges=true; varDeclarationAccepted=false; varResponsesComplete=false.')
    hidden=[v for n,v in cards.items() if not re.match(f'dc{p}Q[1-6]Response$',n) and n!='dc'+p+'Attachments']
    audit.append(f'\nHidden metadata: {sum(norm(v["props"].get("Visible",""))=="false" for v in hidden)}/{len(hidden)} explicitly hidden; {sum(norm(v["props"].get("Height",""))=="0" for v in hidden)}/{len(hidden)} explicitly Height=0. Apply Height=0 to every hidden card.\n')
    audit.append('Also apply the complete question typography, input X=22/Width=Parent.Width-44, border radius/padding, generated-heading visibility, error-label position and card-order corrections below. Open Sans and default navy styling in the exports differ from the planned Segoe UI/theme styling. Preserve native metadata and attachment binding.\n')

mapping='| Category code | Data source | Screen | Form | Record |\n|---|---|---|---|---|\n'+'\n'.join(f'| `{c}` | `{n}` | `scr{n}` | `frm{n}` | `varRecord{p}` |' for c,p,o,n in ROWS)
intro='''# Prod — current environment build and correction guide

Prepared 9 November 2026. This is the current manual implementation specification, not a deployed app or proof of production readiness. Use it instead of documentation2 for the new environment's mappings. Existing historical guides are retained unchanged.

## Review conclusion and precedence

The two exports preserve the fixed SharePoint form schema, dynamic answer slots, typed sources and separate saved-record variables. Their design is incomplete: neither supplied screen contains the full header/navigation/stepper, summary, responsive sidebar, page scrolling or Save/Review actions. Both contain their form directly under the screen. The screenshots confirm the 13 screen names and new list mapping, but do not show rendered screen layouts. Pixel-level visual parity cannot be verified from tree view screenshots.

Use the user's current mapping table first, the original core process/layout second, and the corrected formula recipes below third. Treat Changes.md as evidence and proposed recipes, not as an instruction to change the core design. Its claims about earlier provisioning or tests are historical, not independently verified here. Only the two supplied screen exports were inspected; four remaining forms and shared screen implementations were not supplied.

### Accepted mapping — replaces the earlier order-based mapping

'''+mapping+'''

AwardCategories and AwardQuestions retain their names. Category codes and II/IC/IE/TC/TI/TT prefixes remain unchanged. This mapping agrees with both the supplied table image and Changes.md. In particular IND_INNOVATION now maps to BestInnovatorIndividual, not the earlier documentation2 assignment. Do not mix formula packages.

The target environment ID and real site URL were not supplied. Select your actual new environment/site and bind its eight lists; do not use the fictional Contoso URLs in Changes.md or an old AISite connection. If current configuration records already exist, verify their CategoryCode values against this table before testing. No list rename, data migration or live publication is performed by this guide.

### Corrections required before continuing

1. Keep the original page shell: Contoso header, navigation, four-step display, one scroll viewport below it, summary and desktop progress sidebar. Changes.md's full-screen minimal scrolling layout is a fallback, not the final design. Use the restored shell below.
2. Apply II input positioning/sizing, IC per-slot title/required flags and counter positioning, and common theme/error-label/metadata fixes described in the independent review. Reorder response cards Q1–Q6, then Attachments, then hidden metadata.
3. Wire every form's full OnSuccess/OnFailure and all attachment dirty-state events. Keep final status Patch inside the successful save lifecycle. Do not enable buttons before those events exist.
4. Team categories have three configured questions: publish only Q1–Q3 rows for the active version. Retain all Q1–Q6 columns and controls. The recipes allow 3–6 generally and hide unused slots; they do not enforce a new exactly-three business constraint. Existing saved nominations retain their original count and snapshots.
5. Keep category names, descriptions and questions data-driven. A renamed award does not approve the old prototype's wording. Review category/question content before activation.

## Build sequence for all 13 screens

| Order | Screen / stage | Build and verify |
|---|---|---|
| 1 | App + connections | Verify new solution/environment, eight typed sources, Office365Users; create all named screens/forms; then apply App.Formulas and App.OnStart below. |
| 2 | scrHome | Original shell without stepper; New nomination action initializes state; My nominations opens browsing; admin entry is gated. |
| 3 | scrNomineeDetails | Step 1; individual/team fields, directory pickers, role/level; all changes invalidate review/declaration; Continue validates and opens categories. |
| 4 | scrCategorySelection | Step 2; filter active categories by award type; selection loads only published version after discard handling; snapshot 3–6 slots. |
| 5 | scrBestInnovatorIndividual | First complete draft/save/reopen/evidence slice using II and BestInnovatorIndividual. Apply export corrections before copying layout. |
| 6 | scrMDAward | IC and MDAward; apply its distinct heading/counter corrections. |
| 7 | scrTrendMarcherAward | IE and TrendMarcherAward; fresh bound form, complete IE recipe. |
| 8 | scrBestInnovatorTeam | TC and BestInnovatorTeam; team fields and three configured questions. |
| 9 | scrMDAwardTeam | TI and MDAwardTeam; team fields and three configured questions. |
| 10 | scrSpecialTeamAward | TT and SpecialTeamAward; team fields and three configured questions. |
| 11 | scrReview | Step 4; current in-memory answers and queued filenames; declaration; routed Submit only after validation; return without reset. |
| 12 | scrConfirmation | Reference after verified submitted success; no duplicate submission; new nomination uses reset action. |
| 13 | scrMyNominations | Selected typed source, own-email/status filter; open exact source/ID; Draft edit or Submitted ViewForm; restore snapshots. |
| 14 | scrQuestionAdministration | Approved admin identities; clone/load version, validate new rows, read back, update category pointer last. |

The sequence includes App setup plus 13 screens. Do not reset forms in routine OnVisible events. Complete the acceptance checklist at the end before app publication.

## Evidence limitations and verification

The source text checks verify field coverage and Update mappings, not connector types or Power Fx compilation. Export-omitted defaults must be confirmed in Studio. A screen tree proves screen existence, not layout completion. Runtime tests, new-site permissions and environment-variable binding remain manual acceptance gates.

Microsoft references: [form save lifecycle](https://learn.microsoft.com/power-platform/power-fx/reference/function-form) and [native attachment events and form binding](https://learn.microsoft.com/en-us/powerapps/maker/canvas-apps/controls/control-attachments).
'''

onboarding=remap((ROOT/'documentation/manual-build/README.md').read_text(encoding='utf-8'))
onboarding=onboarding[onboarding.index('## 1. Create the solution'):]
onboarding=onboarding.replace('**Ka6thickMSFT**','**your actual new target environment**').replace('No app has yet been created there by this guide.','Inspect and continue your existing destination app; the screenshot already shows its named screens.')
onboarding=onboarding.replace('Connect these existing AISite lists','Connect these destination-site lists')
onboarding=onboarding.replace('Use the target list GUIDs from `provisioning/deployment-result.json` (not title text) as the list environment-variable values.', 'Use the actual new target list GUIDs from List settings or the connection picker, not the old deployment report, as environment-variable values.')
layout=remap((ROOT/'documentation/manual-build/01-Screens-and-Layout.md').read_text(encoding='utf-8'))
stepper=(ROOT/'documentation/Process-Stepper-Component.md').read_text(encoding='utf-8')
dimensions=['# Exact final form placement for all six screens\n',
    'These values complete the original shell and override any minimal-shell/full-width placement in older notes. First create the header/nav/stepper/scroll controls from the visual guide. Name each centered manual page container, heading, summary and progress container as below. All of these are siblings inside the page container; the form remains a native form. Copy the original heading/subtitle/summary text and styling. Keep the form error label after the form and the action row after that error.\n']
for c,p,o,n in ROWS:
    dimensions.append(f'''## scr{n} — placement

| Control / property | Formula / value |
|---|---|
| `cntPage{p}.Width` | `Min(1180, Parent.Width)` |
| `lblHeading{p}.X` | `If(App.Width<=760,16,24)` |
| `lblHeading{p}.Width` | `cntPage{p}.Width-2*Self.X` |
| `lblHeading{p}.Y` | `If(App.Width<=760,27,39)` |
| `lblHeading{p}.Text` | `If(varReadOnly,"View nomination","Criteria & evidence")` |
| `lblSubtitle{p}.Y` | `lblHeading{p}.Y+lblHeading{p}.Height+8` |
| `lblSubtitle{p}.Text` | `varCategory.Title` |
| `cntSummary{p}.X / Width` | `lblHeading{p}.X` / `lblHeading{p}.Width` |
| `cntSummary{p}.Y` | `lblSubtitle{p}.Y+lblSubtitle{p}.Height+18` |
| `cntSummary{p}.Height` | `If(App.Width<=760,112,72)` |
| `cntProgress{p}.X` | `If(App.Width<=760,lblHeading{p}.X,lblHeading{p}.X+lblHeading{p}.Width-260)` |
| `cntProgress{p}.Y` | `cntSummary{p}.Y+cntSummary{p}.Height+22` |
| `cntProgress{p}.Width / Height` | `If(App.Width<=760,lblHeading{p}.Width,260)` / `If(App.Width<=760,100,260)` |
| `frm{n}.X` | `lblHeading{p}.X` |
| `frm{n}.Y` | `If(App.Width<=760,cntProgress{p}.Y+cntProgress{p}.Height+22,cntProgress{p}.Y)` |
| `frm{n}.Width` | `If(App.Width<=760,lblHeading{p}.Width,lblHeading{p}.Width-282)` |
| `lblSaveError{p}.Y` | `frm{n}.Y+frm{n}.Height+8` |
| `lblSaveError{p}.X / Width` | `frm{n}.X` / `frm{n}.Width` |
| `lblSaveError{p}.AutoHeight / Visible / Text` | `true` / `!IsBlank(frm{n}.Error)` / `frm{n}.Error` |
| `cntActions{p}.X / Width` | `lblHeading{p}.X` / `lblHeading{p}.Width` |
| `cntActions{p}.Y` | `Max(frm{n}.Y+frm{n}.Height,If(lblSaveError{p}.Visible,lblSaveError{p}.Y+lblSaveError{p}.Height,0),cntProgress{p}.Y+cntProgress{p}.Height)+20` |
| `cntActions{p}.Height` | `If(App.Width<=760,96,48)` |
| `cntPage{p}.Height` | `cntActions{p}.Y+cntActions{p}.Height+If(App.Width<=760,40,56)` |

Use the explicit sum of error-aware response card heights plus attachment card height +24 from the {n} recipe below. Set subtitle X/Width to the heading X/Width, heading/subtitle AutoHeight=true, and use the common theme typography. Place Save/Review/Back buttons inside cntActions{p} using the shared action-row coordinates. The Details edit button uses the same capture-before-navigation action as btn{p}Back. Do not set cntPage{p}.Height to the viewport height.
''')
home='''# scrHome — explicit starting screen

Use the shared header/navigation and scrolling page shell, with the stepper strip hidden and Height=0. Set App.StartScreen=scrHome. Use a centered content container with maximum width 1030. Create lblHeadingHome (Text="Employee & Team Recognition Awards", AutoHeight=true, Segoe UI, Theme.Heading, Size=If(App.Width<=760,18.75,22.5)), X=If(App.Width<=760,16,24), Width=Parent.Width-2*Self.X, Y=If(App.Width<=760,27,39).

Add btnHomeNew (Text="New nomination", X=lblHeadingHome.X, Y=lblHeadingHome.Y+lblHeadingHome.Height+26, Width=220, Height=44). Its OnSelect is the complete New nomination action below, invoked only after the documented discard confirmation if there is an active nomination. Add btnHomeMine below it (Y=btnHomeNew.Y+btnHomeNew.Height+16, same X/Width/Height, Text="My nominations", OnSelect=Navigate(scrMyNominations,ScreenTransition.None)). Add btnHomeAdmin below that (same spacing, Text="Question administration", Visible=varCanManageQuestions, OnSelect=Navigate(scrQuestionAdministration,ScreenTransition.None)). Verify App.OnStart defines varCanManageQuestions before use. Apply the shared button styles. Set page Height from the last visible button plus 56. Home entry must not reset an active form in OnVisible.

These native entry controls complete a functional Home screen; no supplied rendered Home screenshot verifies its final spacing. The original theme and shared header remain the visual reference.
'''
# Retain full expanded recipes, replacing the minimal-shell instructions with original design authority.
recipes=CHANGES[CHANGES.index('## Six explicit form recipes'):]
recipes=recipes.replace('Use the common form-building and scrolling rules above.', 'Use the restored original shell and card-building rules in this document. The minimal full-screen shell is not the target layout.')
common=CHANGES[CHANGES.index('## Common form-building and scrolling rules'):CHANGES.index('### Scrolling layout')]
body='\n\n'.join([intro,'\n'.join(audit),'# Solution, state and navigation setup\n'+onboarding,
    '# Original visual design — retained\n'+layout,
    home, '\n'.join(dimensions),
    '# Reusable process stepper — complete formulas\n'+stepper,
    common, '# Complete current form and shared-screen recipes\n'+recipes])
# Old relative recipe links become local anchors; every named formula is embedded below.
def link(m):
    target=m[1]
    if target.startswith(('http:','https:','#')): return m[0]
    anchors={'App.Formulas.fx':'appformulas','App.OnStart.fx':'apponstart',
      'NewNomination.OnSelect.fx':'new-nomination-action-after-any-required-discard-confirmation',
      'Details.Continue.OnSelect.fx':'details-continue-button-onselect',
      'Category.Load.OnSelect.fx':'category-load-action-after-selectiondiscard-checks',
      'Review.Submit.OnSelect.fx':'review-screen-submit-button-onselect',
      'Admin.LoadCopy.OnSelect.fx':'question-administration-copyload-button-onselect',
      'Admin.Publish.OnSelect.fx':'question-administration-publish-button-onselect',
      'Navigate-Active-Form.fx':'return-to-the-existing-active-form-without-resetting-it'}
    return '](#'+anchors.get(target,'build-sequence-for-all-13-screens')+')'
body=re.sub(r'\]\(([^)]+)\)',link,body)
(ROOT/'Prod.md').write_text(body,encoding='utf-8')
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in INPUT.iterdir() if p.is_file() and p.name!='manifest.json'}
(INPUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built Prod.md; independently checked both source field sets and Update mappings.')
