"""Build screen-specific manuals with reusable header/navigation and real FX files."""
from pathlib import Path
import re, runpy, ast

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'production-guide'
OUT.mkdir(exist_ok=True)
(OUT/'fx').mkdir(exist_ok=True)
source=(ROOT/'production-review/Changes.md').read_text(encoding='utf-8-sig')
old=runpy.run_path(str(ROOT/'tools/Prod-Screen-Chapters.py'))
screens=old['SCREENS']
legacy=old['chapters']()

def section(text,heading):
    start=text.index(heading)
    level=len(heading)-len(heading.lstrip('#'))
    match=re.search(r'^#{1,'+str(level)+r'} ',text[start+len(heading):],re.M)
    return text[start:start+len(heading)+match.start()] if match else text[start:]

def blocks(text): return re.findall(r'```powerfx\s*\n(.*?)```',text,re.S)
def fx(name,value):
    (OUT/'fx'/name).write_text(value.strip()+'\n',encoding='utf-8')
    return f'[Copy full formula](fx/{name})'
def table(rows):
    return '| Control / property | Value or formula |\n|---|---|\n'+'\n'.join('| '+a+' | '+b.replace('|','\\|').replace('\n','<br>')+' |' for a,b in rows)+'\n'
def inline(v):return '`'+v+'`'
def expand_fx(text,stem):
    i=0
    def replace(m):
        nonlocal i
        i+=1
        return fx(f'{stem}.{i:02}.fx',m[1])+' — paste into the property identified immediately above.\n'
    text=re.sub(r'```powerfx\s*\n(.*?)```',replace,text,flags=re.S)
    # Preserve references to the separate full formula reference, never old source names.
    text=re.sub(r'\]\(documentation/manual-build/([^)]*)\)',lambda m:'](Reference.md)',text)
    return text

shared={
 'App.Formulas':'### App.Formulas','App.OnStart':'### App.OnStart',
 'NewNomination.OnSelect':'### New nomination action after any required discard confirmation',
 'Details.Continue.OnSelect':'### Details Continue button OnSelect',
 'Category.Load.OnSelect':'### Category load action after selection/discard checks',
 'NavigateActiveForm':'### Return to the existing active form without resetting it',
 'Review.Submit.OnSelect':'### Review screen Submit button OnSelect',
 'Admin.LoadCopy.OnSelect':'### Question administration copy/load button OnSelect',
 'Admin.Publish.OnSelect':'### Question administration Publish button OnSelect'}
for name,heading in shared.items():fx(name+'.fx',blocks(section(source,heading))[0])

component='''# Build reusable components once

## What changes in your half-built screen

| Keep | Replace after verification | New reusable definition |
|---|---|---|
| frmBestInnovatorIndividual and all corrected cards/events | cntHeaderII and its copied labels/logo | cmpAppHeader |
| cntScrollII and cntPageII | cntNavII and its copied navigation buttons | cmpAppNav |
| Summary, progress, action row and form controls | cntStepperStripII, if only used to host the stepper | cmpStepper directly on the screen |

1. Save a development checkpoint. Create the three components below in the **Components** tab of Tree view.
2. Insert instances on scrBestInnovatorIndividual. Initially hide the old header/nav/strip (Visible=false) rather than deleting them.
3. Update cntScrollII.Y to the formula in its new screen guide. Verify navigation, discard handling and stepper states.
4. Once verified, remove the redundant hidden visual containers if desired. Keep the original form and its controls. Do not copy component children into every screen.

## Property types and terminology

| Term | What to select |
|---|---|
| Manual-layout container | Insert → Layout → plain Container; you set child X/Y |
| Scroll viewport | Insert → Vertical container; set vertical overflow to Scroll |
| Component definition | Create once in Tree view → Components |
| Component instance | Insert a custom component on a screen; set its input/event properties |
| Data input | Custom property: Data, Input, specified data type |
| Event input | Custom property: Event, no parameters; the hosting screen supplies behavior |

For existing apps check Settings → Updates → Enhanced component properties if Event is not offered. Keep **Access app scope off** in all three components. Event properties are required for this recipe; do not substitute a Text/Boolean input for an Event. The host handles state, navigation, forms and SharePoint. See [Microsoft's component property instructions](https://learn.microsoft.com/en-gb/power-apps/maker/canvas-apps/component-properties).

## 1. cmpAppHeader

Create a component named cmpAppHeader. Default Width=1366, Height=64, Fill=Color.White.

```text
cmpAppHeader
  imgHeaderLogo (Image)
  lblHeaderBrand (classic Label)
  lblHeaderTitle (classic Label)
  lblHeaderUser (classic Label)
```

Create these custom properties before setting child formulas:

| Name | Kind / data type | Preview default |
|---|---|---|
| BrandText | Data Input / Text | "Contoso" |
| TitleText | Data Input / Text | "Employee & Team Recognition Awards" |
| UserText | Data Input / Text | "" |
| LogoImage | Data Input / Image | Blank() |
| HeadingColor | Data Input / Color | ColorValue("#17253f") |
| SmallLayout | Data Input / Boolean | false |

| Control | Property | Formula |
|---|---|---|
| imgHeaderLogo | X / Y / Width / Height | 16 / (cmpAppHeader.Height-28)/2 / 28 / 28 |
| imgHeaderLogo | Image / ImagePosition | cmpAppHeader.LogoImage / ImagePosition.Fit |
| imgHeaderLogo | AccessibleLabel | cmpAppHeader.BrandText & " awards" |
| lblHeaderBrand | X / Y / Width / Height | 54 / (cmpAppHeader.Height-28)/2 / 76 / 28 |
| lblHeaderBrand | Text | cmpAppHeader.BrandText |
| lblHeaderTitle | X / Y / Width / Height | 144 / (cmpAppHeader.Height-28)/2 / Max(0,cmpAppHeader.Width-374) / 28 |
| lblHeaderTitle | Text / Visible | cmpAppHeader.TitleText / !cmpAppHeader.SmallLayout |
| lblHeaderUser | X / Y / Width / Height | Max(140,cmpAppHeader.Width-210) / (cmpAppHeader.Height-28)/2 / 190 / 28 |
| lblHeaderUser | Text / Visible | cmpAppHeader.UserText / !cmpAppHeader.SmallLayout |
| All three labels | Font / Color | Font.'Segoe UI' / cmpAppHeader.HeadingColor |
| lblHeaderBrand | Size / FontWeight | 11.25 / FontWeight.Semibold |
| lblHeaderTitle, lblHeaderUser | Size | 9.75 |

## 2. cmpAppNav

Create cmpAppNav, default Width=1366, Height=48, Fill=Color.White.

```text
cmpAppNav
  btnComponentNew (classic Button)
  btnComponentMine (classic Button)
  rectNavSelected (Rectangle)
```

| Custom property | Kind / type | Preview default |
|---|---|---|
| Busy | Data Input / Boolean | false |
| ActiveTab | Data Input / Text | "New" |
| AccentColor | Data Input / Color | ColorValue("#0f6cbd") |
| OnNew | Event, no parameters | Leave behavior empty until instance binding |
| OnMine | Event, no parameters | Leave behavior empty until instance binding |

| Control | Property | Formula |
|---|---|---|
| btnComponentNew | X / Y / Width / Height | 16 / 5 / Min(150,(cmpAppNav.Width-40)/2) / 38 |
| btnComponentMine | X / Y / Width / Height | btnComponentNew.X+btnComponentNew.Width+8 / 5 / btnComponentNew.Width / 38 |
| btnComponentNew | Text / OnSelect | "New nomination" / cmpAppNav.OnNew() |
| btnComponentMine | Text / OnSelect | "My nominations" / cmpAppNav.OnMine() |
| Both buttons | DisplayMode | If(cmpAppNav.Busy,DisplayMode.Disabled,DisplayMode.Edit) |
| Both buttons | Fill / Color / Font / Size | Color.Transparent / cmpAppNav.AccentColor / Font.'Segoe UI' / 9.75 |
| Both buttons | BorderThickness / FocusedBorderThickness | 0 / 2 |
| rectNavSelected | X | If(cmpAppNav.ActiveTab="Mine",btnComponentMine.X,btnComponentNew.X) |
| rectNavSelected | Y / Width / Height / Fill | 46 / btnComponentNew.Width / 2 / cmpAppNav.AccentColor |
| rectNavSelected | Visible | cmpAppNav.ActiveTab="New" Or cmpAppNav.ActiveTab="Mine" |

The component calls its Event properties. Paste the screen-specific event FX files into **the instance's OnNew/OnMine properties**, not into the component's buttons. No hidden helper from another screen is called.

## 3. cmpStepper

Use [the complete stepper component guide](01-Stepper.md). It contains the input-property schema, Image control and SVG formula. Keep the display-only component and existing completion-state logic. Insert its instance directly below cmpAppNav on screens that need the stepper. No cntStepperStrip container is needed in this revised design.

## Verification before duplicating instances

| Check | Expected |
|---|---|
| Change BrandText on one instance | Its header changes without changing the definition |
| Edit a label style in the definition | All instances receive the visual update |
| OnNew while unsaved | Host opens its discard dialog |
| Cancel discard | Existing form data and queued files stay intact |
| Busy=true | Navigation buttons disabled |
| Steps change | Only progress appearance changes; no save/navigation occurs |

Component recipes have not been compiled in your Studio session. Resolve property/schema errors before reusing instances.
'''
(OUT/'00-Reusable-Components.md').write_text(component,encoding='utf-8')
stepper=(ROOT/'documentation/Process-Stepper-Component.md').read_text(encoding='utf-8')
stepper=stepper.replace('Target environment: Ka6thickMSFT.', 'Target environment: your current destination environment.')
(OUT/'01-Stepper.md').write_text(expand_fx(stepper,'cmpStepper'),encoding='utf-8')

# Preserve the prior full reference, but remove the superseded screen-shell instructions.
reference=(ROOT/'Prod.md').read_text(encoding='utf-8')
if '# Reference appendix — mappings, complete formulas and historical audit' in reference:
    reference=reference.split('# Reference appendix — mappings, complete formulas and historical audit',1)[1]
if len(reference)<50000 and (OUT/'Reference.md').exists():
    reference=(OUT/'Reference.md').read_text(encoding='utf-8')
(OUT/'Reference.md').write_text('# Formula reference — historical shell is superseded\n\nUse the individual screen guides for current component/container construction. This appendix retains detailed field recipes and the historical audit.\n\n'+reference,encoding='utf-8')

shared_sections={'Details':'#### 2. scrNomineeDetails','Category':'#### 3. scrCategorySelection',
 'Review':'#### 1. scrReview','Confirmation':'#### 2. scrConfirmation','Mine':'#### 3. scrMyNominations',
 'Admin':'#### 4. scrQuestionAdministration'}

def content_tree(p,n):
    if n:
        tree=[('lblHeading'+p,'Label'),('lblSubtitle'+p,'Label'),('cntSummary'+p,'Container'),
         ('  lblSummary'+p,'Label'),('  btnEditDetails'+p,'Button'),('cntProgress'+p,'Container'),
         ('  lblProgress'+p,'Label'),('  lblProgressHelp'+p,'Label'),('frm'+n,'Existing Edit form' if p in ('II','IC') else 'Edit form')]
        if p not in ('II','IC'):
            for i in range(1,7):
                tree += [(f'  dc{p}Q{i}Response','Data card'),(f'    cnt{p}Q{i}','Container'),(f'      lbl{p}Q{i}Heading','Label'),(f'      lbl{p}Q{i}Prompt','Label'),(f'      txt{p}Q{i}','Text input'),(f'      lbl{p}Q{i}Counter','Label'),(f'    err{p}Q{i}','Label')]
            tree += [(f'  dc{p}Attachments','Native attachment card'),(f'    att{p}','Native Attachments')]
            names=['Title','Category','QuestionSetVersion','QuestionCount','NominatedBy','NominatorEmail','EmployeeRole','EmployeeLevel','NominationStatus','DeclarationAccepted','SubmittedOn']+(['NominatedEmployee'] if p=='IE' else ['TeamName','TeamPrimaryContact','TeamMembers'])
            names += [f'Q{i}{s}' for i in range(1,7) for s in ['PromptSnapshot','RequiredSnapshot']]
            tree += [('  dc'+p+x,'Hidden native card; retain generated child editors') for x in names]
        return tree+[(f'lblSaveError{p}','Label'),('cntActions'+p,'Container'),('  btn'+p+'Back','Button'),('  btn'+p+'SaveDraft','Button'),('  btn'+p+'Review','Button'),('  btn'+p+'BackToMine','Button')]
    mapping={
      'Home':['lblHeadingHome','lblSubtitleHome','cntActionsHome','  btnHomeNew','  btnHomeMine','  btnHomeAdmin'],
      'Details':['lblHeadingDetails','lblSubtitleDetails','cntDetailsCard','  lblType','  btnIndividualType','  btnTeamType','  lblNominator','  lblNominatorValue','  lblNominee','  cmbNominee','  cntTeamDetails','    lblTeamName','    txtTeamName','    lblPrimaryContact','    cmbPrimaryContact','    lblTeamMembers','    cmbTeamMemberToAdd','    btnAddTeamMember','    galTeamMembers','      lblMemberName','      btnRemoveTeamMember','  cntRoleLevel','    lblRole','    txtRole','    lblLevel','    cmbLevel','  lblDetailsHelp','cntActionsDetails','  btnDetailsContinue'],
      'Category':['lblHeadingCategory','lblSubtitleCategory','cntCategorySummary','  lblCategorySummary','galCategories','  cntCategoryTile','    lblCategoryTitle','    lblCategoryDescription','    lblCategorySelected','  btnSelectCategory','lblCategoryState','cntActionsCategory','  btnCategoryBack','  btnCategoryContinue','btnLoadCategory','btnRefreshCategories'],
      'Review':['lblHeadingReview','lblSubtitleReview','cntReviewDetails','  lblReviewDetails','  btnReviewEditDetails']+[x for i in range(1,7) for x in [f'cntReviewQ{i}',f'  lblReviewHeading{i}',f'  lblReviewPrompt{i}',f'  lblReviewAnswer{i}']]+['cntReviewEvidence','  lblEvidenceHeading','  lblReviewFiles','  btnReviewEditEvidence','cntDeclaration','  chkDeclaration','  lblDeclarationHelp','cntActionsReview','  btnReviewBack','  btnReviewSubmit'],
      'Confirmation':['lblHeadingConfirmation','lblSubtitleConfirmation','cntConfirmationCard','  lblConfirmationReference','  lblConfirmationCategory','  lblConfirmationNominee','  lblConfirmationTime','cntActionsConfirmation','  btnConfirmationView','  btnConfirmationMine','  btnConfirmationNew'],
      'Mine':['lblHeadingMine','lblSubtitleMine','cntMineFilters','  btnBrowseIndividual','  btnBrowseTeam','  cmbBrowseCategory','  ddBrowseStatus','  txtBrowseId','  btnBrowseRefresh','lblBrowseError','cntMineResults']+[x for q in ['II','IC','IE','TC','TI','TT'] for x in ['  galMine'+q,'    lblMineReference'+q,'    lblMineNominee'+q,'    lblMineModified'+q,'    lblMineStatus'+q,'    btnMineOpen'+q]]+['cntActionsMine','  btnMineNew'],
      'Admin':['lblHeadingAdmin','lblSubtitleAdmin','lblAdminDenied','cntAdminEditor','  cmbAdminCategory','  lblAdminVersion','  btnAdminCopyVersion','  galAdminQuestions','    lblAdminSlot','    txtAdminTitle','    txtAdminQuestion','    txtAdminGuidance','    chkAdminRequired','  btnAdminAddQuestion','  btnAdminRemoveQuestion','  galAdminPreview','    lblAdminPreview','  galAdminErrors','    lblAdminError','cntActionsAdmin','  btnAdminPublish','  btnAdminFreshVersion','btnAdminLoadCopy']}
    def kind(x):
        x=x.strip()
        for a,b in [('cnt','Container'),('lbl','Label'),('btn','Button'),('cmb','Classic Combo box'),('txt','Classic Text input'),('gal','Gallery'),('chk','Classic Checkbox'),('dd','Classic Dropdown')]:
            if x.startswith(a):return b
    return [(x,kind(x)) for x in mapping[p]]

def screen_guide(s,p,w,step,n):
    heading=f'# {s} — build sheet\n\n'
    heading+='[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)\n\n'
    heading+='**Keep the existing form and corrected cards. Build only the surrounding page controls.**\n\n' if p in ('II','IC') else 'Build controls in Tree view order. Insert children under the parent shown.\n\n'
    tree=[s,f'  cmpHeader{p} [instance of cmpAppHeader]',f'  cmpNav{p} [instance of cmpAppNav]']
    if step:tree += [f'  cmpStepper{p} [instance of cmpStepper]']
    tree += [f'  cntScroll{p} [Vertical container]',f'    cntPage{p} [plain Container]']
    tree += ['      '+name+' ['+kind+']' for name,kind in content_tree(p,n)]
    tree += [f'  btnStartNew{p} [hidden Button]',f'  btnGoMine{p} [hidden Button]',f'  cntExitOverlay{p} [plain Container]',f'    cntExitDialog{p} [plain Container]',f'      lblExitMessage{p} [Label]',f'      btnExitCancel{p} [Button]',f'      btnExitDiscard{p} [Button]',f'  cntBusy{p} [plain Container]',f'    lblBusy{p} [Label]']
    if p in ('Category','Admin'):
        tag='CategoryChange' if p=='Category' else 'AdminDiscard'
        tree += [f'  cnt{tag}Overlay [Container]',f'    cnt{tag}Dialog [Container]',f'      lbl{tag}Message [Label]',f'      btn{tag}Cancel [Button]',f'      btn{tag}Confirm [Button]']
    text=heading+'## 1. Complete Tree view\n\n```text\n'+'\n'.join(tree)+'\n```\n\n'
    text+='Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.\n\n'
    rows=[(s+'.Fill','Theme.Page'),(f'cmpHeader{p}.X / Y','0 / 0'),(f'cmpHeader{p}.Width / Height','Parent.Width / If(App.Width<=760,58,64)'),
      (f'cmpHeader{p}.BrandText / TitleText','Theme.Brand / Theme.AppTitle'),(f'cmpHeader{p}.UserText','User().FullName'),(f'cmpHeader{p}.HeadingColor / SmallLayout','Theme.Heading / App.Width<=760'),
      (f'cmpNav{p}.X / Y',f'0 / cmpHeader{p}.Y+cmpHeader{p}.Height'),(f'cmpNav{p}.Width / Height','Parent.Width / 48'),(f'cmpNav{p}.Busy / AccentColor','varIsBusy / Theme.Primary'),(f'cmpNav{p}.ActiveTab','"Mine"' if p=='Mine' else '""' if p in ('Admin','Home','Confirmation') else '"New"'),
      (f'cntScroll{p}.X','0'),(f'cntScroll{p}.Y',f'cmpStepper{p}.Y+cmpStepper{p}.Height' if step else f'cmpNav{p}.Y+cmpNav{p}.Height'),(f'cntScroll{p}.Width / Height','Parent.Width / Max(0,Parent.Height-Self.Y)'),
      (f'cntScroll{p}.LayoutDirection','LayoutDirection.Vertical'),(f'cntScroll{p}.LayoutOverflowY / LayoutOverflowX','LayoutOverflow.Scroll / LayoutOverflow.Hide'),(f'cntScroll{p}.LayoutGap / all paddings','0'),
      (f'cntPage{p}.Width',f'Min({w},Parent.Width)'),(f'cntPage{p}.AlignInContainer','AlignInContainer.Center'),(f'cntPage{p}.FillPortions / LayoutMinWidth / LayoutMinHeight','0 / 0 / 0'),
      (f'cntPage{p}.Height',f'cntActions{p}.Y+cntActions{p}.Height+If(App.Width<=760,40,56)'),
      (f'lblHeading{p}.X / Y', 'If(App.Width<=760,16,24) / If(App.Width<=760,27,39)'),(f'lblHeading{p}.Width / AutoHeight','Parent.Width-2*Self.X / true'),(f'lblHeading{p}.Font / Size',"Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)"),(f'lblHeading{p}.Color / FontWeight','Theme.Heading / FontWeight.Semibold'),
      (f'lblSubtitle{p}.X / Y',f'lblHeading{p}.X / lblHeading{p}.Y+lblHeading{p}.Height+8'),(f'lblSubtitle{p}.Width / AutoHeight',f'lblHeading{p}.Width / true'),(f'lblSubtitle{p}.Font / Size / Color',"Font.'Segoe UI' / 11.25 / Theme.Muted")]
    if step:
        rows += [(f'cmpStepper{p}.X / Y',f'(Parent.Width-Self.Width)/2 / cmpNav{p}.Y+cmpNav{p}.Height'),(f'cmpStepper{p}.Width / Height','Min(1060,Parent.Width) / 94'),(f'cmpStepper{p}.CurrentStep','varCurrentStep')]
        for prop,val in [('CurrentHex','PrimaryHex'),('CompleteHex','SuccessHex'),('PendingHex','BorderHex'),('MutedHex','MutedHex'),('HaloHex','PaleHex')]:rows.append((f'cmpStepper{p}.{prop}','Theme.'+val))
    text+='## 2. Components and scrolling — property table\n\nUse temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.\n\n'+table([(a,inline(b)) for a,b in rows])
    if step:
        steps='Table({StepNo:1,Label:"Nominee details",IsComplete:varDetailsComplete},{StepNo:2,Label:"Award category",IsComplete:varCategoryComplete},{StepNo:3,Label:"Criteria & evidence",IsComplete:varResponsesComplete},{StepNo:4,Label:"Review & submit",IsComplete:varSubmissionComplete})'
        text+=table([(f'cmpStepper{p}.Steps',fx(f'cmpStepper{p}.Steps.fx',steps))])
    text+='\n## 3. Navigation events and hidden helpers\n\n'
    nav=[]
    for event,action,target in [('OnNew','New','btnStartNew'),('OnMine','Mine','btnGoMine')]:
        code=f'If((varHasChanges && !varReadOnly)'+(' || varAdminDirty' if p=='Admin' else '')+f', Set(varExitAction,"{action}"); Set(varShowExitDialog,true), Select({target}{p}))'
        nav.append((f'cmpNav{p}.{event}',fx(f'cmpNav{p}.{event}.fx',code)))
    nav += [(f'btnStartNew{p}.OnSelect','[Copy full New nomination formula](fx/NewNomination.OnSelect.fx)'),(f'btnGoMine{p}.OnSelect',inline('Navigate(scrMyNominations,ScreenTransition.None)')),(f'btnStartNew{p} and btnGoMine{p}: Visible / DisplayMode',inline('false / DisplayMode.Edit'))]
    text+=table(nav)+'\nPaste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.\n\n'
    modal=[(f'cntExitOverlay{p}.X / Y / Width / Height','0 / 0 / Parent.Width / Parent.Height'),(f'cntExitOverlay{p}.Visible / Fill','varShowExitDialog / RGBA(0,0,0,0.35)'),(f'cntExitDialog{p}.Width / Height','Min(440,Parent.Width-32) / 220'),(f'cntExitDialog{p}.X / Y','(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)'),(f'cntExitDialog{p}.Fill','Theme.Surface'),(f'lblExitMessage{p}.X / Y / Width / Height','20 / 20 / Parent.Width-40 / 112'),(f'lblExitMessage{p}.Text','"Leave this page? Unsaved changes and selected files will be discarded."'),(f'btnExitCancel{p}.X / Y / Width / Height','20 / 160 / 110 / 38'),(f'btnExitCancel{p}.Text / OnSelect','"Cancel" / Set(varShowExitDialog,false)'),(f'btnExitDiscard{p}.X / Y / Width / Height','Parent.Width-140 / 160 / 120 / 38'),(f'btnExitDiscard{p}.Text','"Discard"'),(f'cntBusy{p}.X / Y / Width / Height','0 / 0 / Parent.Width / Parent.Height'),(f'cntBusy{p}.Visible / Fill','varIsBusy / RGBA(255,255,255,0.65)'),(f'lblBusy{p}.Text / Align','"Saving or loading…" / Align.Center'),(f'lblBusy{p}.X / Y / Width / Height','0 / (Parent.Height-40)/2 / Parent.Width / 40')]
    text+='## 4. Dialog and busy controls — property table\n\n'+table([(a,inline(b)) for a,b in modal])
    discard='Set(varShowExitDialog,false); Set(varHasChanges,false);'+('Set(varAdminDirty,false);' if p=='Admin' else '')+f'If(varExitAction="New",Select(btnStartNew{p}),Select(btnGoMine{p}))'
    text+=table([(f'btnExitDiscard{p}.OnSelect',fx(f'btnExitDiscard{p}.OnSelect.fx',discard))])
    text+='\n## 5. Screen content, buttons and formulas\n\n'
    # Retain the exact screen-specific content/action recipes, without the copied header/nav shell.
    oldchapter=section(legacy,f'## {s} — exact controls and build order')
    detail=oldchapter.split('### 6. Screen content and action container',1)[1].split('### 7.',1)[0].split('### Checkpoint',1)[0]
    detail=detail.replace('Select(btnNavNew'+p+')',f'cmpNav{p}.OnNew()').replace('Select(btnNavMine'+p+')',f'cmpNav{p}.OnMine()')
    # Direct callers use the event logic itself: events are dispatched by the component buttons.
    detail=detail.replace(f'cmpNav{p}.OnNew()',f'Select(btnStartNew{p})').replace(f'cmpNav{p}.OnMine()',f'Select(btnGoMine{p})')
    detail=re.sub(r'\]\(#[^)]+\)','](Reference.md)',detail)
    text+=detail
    if n:
        placement=section(reference,f'## scr{n} — placement')
        text+='\n### Exact content placement\n\n'+placement
        recipe=section(source,f'### {n}:')
        # Metadata layouts and complete handlers remain explicit; convert every block to a real file.
        text+='\n### '+('Existing form reference — verify only when needed' if p in ('II','IC') else 'Build this form and every card')+'\n\n'+expand_fx(recipe,s)
    elif p in shared_sections:
        text+='\n### Detailed content/control recipe\n\n'+expand_fx(section(source,shared_sections[p]),s)
        if p=='Review':text+=expand_fx(section(source,'### Six expanding review question blocks'),'ReviewQuestions')
    else:
        text+='\nSet btnHomeAdmin.Visible=varCanManageQuestions. Home has no form reset in OnVisible. Apply the full New nomination formula only after unsaved-change checks.\n'
    # New/mine actions outside nav must retain same-screen discard behavior; reference exact FX files.
    text+='\n### Event file assignments — paste into these exact properties\n\n'
    assignments=[]
    if p=='Home':assignments=[('btnHomeNew.OnSelect',f'cmpNav{p}.OnNew.fx'),('btnHomeMine.OnSelect',f'cmpNav{p}.OnMine.fx')]
    if p=='Details':assignments=[('btnDetailsContinue.OnSelect','Details.Continue.OnSelect.fx')]
    if p=='Category':assignments=[('btnLoadCategory.OnSelect','Category.Load.OnSelect.fx')]
    if p=='Review':
        fx('Review.Back.fx','Set(varDeclarationAccepted,false);\n'+(OUT/'fx/NavigateActiveForm.fx').read_text(encoding='utf-8'))
        assignments=[('btnReviewSubmit.OnSelect','Review.Submit.OnSelect.fx'),('btnReviewBack.OnSelect','Review.Back.fx'),('btnReviewEditEvidence.OnSelect','Review.Back.fx')]
    if p=='Confirmation':assignments=[('btnConfirmationView.OnSelect','NavigateActiveForm.fx'),('btnConfirmationMine.OnSelect',f'cmpNav{p}.OnMine.fx'),('btnConfirmationNew.OnSelect',f'cmpNav{p}.OnNew.fx')]
    if p=='Mine':assignments=[('btnMineNew.OnSelect',f'cmpNav{p}.OnNew.fx')]
    if p=='Admin':assignments=[('btnAdminLoadCopy.OnSelect','Admin.LoadCopy.OnSelect.fx'),('btnAdminPublish.OnSelect','Admin.Publish.OnSelect.fx')]
    text+=table([(control,f'[Copy full formula](fx/{file})') for control,file in assignments]) if assignments else 'Form button and event formulas are linked beside their exact headings above.\n'
    text+='\n## 6. Verify before the next screen\n\n| Check | Expected |\n|---|---|\n| Tree view | Matches the listed parents; no duplicate existing form |\n| Components | Header/nav built once; instances have values/events |\n| Scroll | Last input, error and action reachable at desktop/mobile widths |\n| Cancel | Unsaved answers and queued files retained |\n| Formulas | No unresolved names; English separators or locale equivalent |\n| Runtime | Test synthetic draft/save/reopen before submission |\n'
    # Crosslinks in imported references point to the retained reference or real FX files.
    text=re.sub(r'\]\(#[^)]+\)','](Reference.md)',text)
    return text

for s,p,w,step,n in screens:(OUT/(s+'.md')).write_text(screen_guide(s,p,w,step,n),encoding='utf-8')
index='''# Prod — reusable components and screen build guides

Updated 10 November 2026. Build the shared components once, then follow one screen guide at a time. Each screen has its own Tree view, parent/control types, property tables and linked `.fx` files. The two existing forms are retained.

## Start here

1. [Build reusable header, navigation and stepper](production-guide/00-Reusable-Components.md). This includes migration steps for your half-built first screen.
2. [Finish scrBestInnovatorIndividual](production-guide/scrBestInnovatorIndividual.md).
3. [Finish scrMDAward](production-guide/scrMDAward.md).
4. Build the remaining screens from the table below.

## Screen guides

| Screen | Guide | Main work |
|---|---|---|
'''
for s,p,w,step,n in screens:index+=f'| `{s}` | [Open guide](production-guide/{s}.md) | '+('Keep existing form; finish shell/actions' if p in ('II','IC') else 'Build controls, properties and behavior')+' |\n'
index+='''
## Shared App properties

| Property | Formula file |
|---|---|
| App.StartScreen | `scrHome` |
| App.Formulas | [App.Formulas.fx](production-guide/fx/App.Formulas.fx) |
| App.OnStart | [App.OnStart.fx](production-guide/fx/App.OnStart.fx) |

Create all required source/form/control names before running OnStart. Do not run it during unsaved editing. Component inputs receive Theme/state values from the host app; Access app scope stays off.

## Configuration contract

| Category | Source | Screen | Form |
|---|---|---|---|
'''
for (s,p,w,step,n),c in zip(screens[:6],['IND_INNOVATION','IND_CUSTOMER','IND_EXCELLENCE','TEAM_COLLAB','TEAM_IMPACT','TEAM_TRANSFORM']):index+=f'| {c} | {n} | {s} | frm{n} |\n'
index+='''
AwardCategories and AwardQuestions retain their names. Keep all fixed columns and Q1–Q6 slots. Team categories have three configured active question rows; unused slots stay hidden. Questions, categories and snapshots remain data-driven. Keep native attachments inside the matching form and the final status update inside form OnSuccess.

## Reference and validation

- [Full field/formula reference and earlier audit](production-guide/Reference.md). Its old copied-header layout is superseded by the component/screen guides above.
- [Stepper implementation](production-guide/01-Stepper.md).
- `.fx` files are formulas for properties, not importable applications. Copy the entire file into the named property.
- Source checks do not prove Studio compilation, rendering, permissions or runtime success. Finish the acceptance checklist in the reference before publication.

**Rebuild documentation:** run `tools/Build-ReusableGuides.py`. Do not run the older guide generators alone; they recreate the superseded single-file guide.
'''
(ROOT/'Prod.md').write_text(index,encoding='utf-8')
print('Built reusable components, 13 screen guides, index and extracted FX files.')

# Apply the chosen global palette consistently after extracting the original recipes.
colors={'#0f6cbd':'#E20074','#0b5a9e':'#B5005D','#eff6fc':'#FDE6F1'}
formula_path=OUT/'fx/App.Formulas.fx'
formulas=formula_path.read_text(encoding='utf-8')
match=re.match(r'Theme\s*=\s*(\{.*?\});\s*',formulas,re.S)
assert match,'Expected original theme record'
palette='Set(varAppTheme, '+match[1]+');\n'
for a,b in colors.items():palette=palette.replace(a,b)
formula_path.write_text(formulas[match.end():],encoding='utf-8')
fx('Theme.Initialize.fx',palette)
onstart=OUT/'fx/App.OnStart.fx'
onstart.write_text(palette+'\n'+onstart.read_text(encoding='utf-8'),encoding='utf-8')
logo='"data:image/svg+xml;utf8," & EncodeUrl("<svg xmlns=\"\"http://www.w3.org/2000/svg\"\" viewBox=\"\"0 0 28 28\"\"><rect width=\"\"28\"\" height=\"\"28\"\" rx=\"\"6\"\" fill=\"\"" & varAppTheme.PrimaryHex & "\"\"/><circle cx=\"\"14\"\" cy=\"\"11\"\" r=\"\"5\"\" fill=\"\"none\"\" stroke=\"\"white\"\"/><path d=\"\"M11 15 L10 23 L14 20 L18 23 L17 15\"\" fill=\"\"none\"\" stroke=\"\"white\"\"/></svg>")'
fx('Header.LogoImage.fx',logo)
for path in list(OUT.rglob('*.md'))+list(OUT.rglob('*.fx')):
    text=path.read_text(encoding='utf-8')
    text=re.sub(r'(?<![\w])Theme\.', 'varAppTheme.',text)
    for a,b in colors.items():text=text.replace(a,b)
    # Embedded reference must not offer a competing named theme definition.
    text=re.sub(r'Theme\s*=\s*\{.*?\};\s*', '',text,flags=re.S)
    if path.name.startswith('scr') and path.suffix=='.md':
        p=next(p for s,p,w,st,n in screens if s==path.stem)
        text+='\n## Header image and theme initialization\n\n'+table([(f'cmpHeader{p}.LogoImage','[Copy Image formula](fx/Header.LogoImage.fx)')])
        text+='\nBefore preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.\n'
    path.write_text(text,encoding='utf-8')
(OUT/'02-Theme.md').write_text('''# Theme setup — #E20074

The new guides use **varAppTheme**, a global record initialized with Set in App.OnStart. This does not automatically restyle controls: each Fill/Color/BorderColor must use the values below. The failure of the previous Theme reference has not been diagnosed in your Studio session; this is an explicit replacement strategy, not a claim that named formulas are unsupported.

## Apply once

| Step | Action |
|---|---|
| 1 | Remove the old `Theme = {...};` definition from App.Formulas. Use the updated [App.Formulas.fx](fx/App.Formulas.fx), retaining LevelOptions and validation formulas. |
| 2 | Use the updated [App.OnStart.fx](fx/App.OnStart.fx); its first block initializes varAppTheme. If you already customized OnStart, merge only [Theme.Initialize.fx](fx/Theme.Initialize.fx) at its beginning. |
| 3 | Save unsaved nomination work before running full OnStart, because it resets working state. To refresh colours alone, temporarily paste Theme.Initialize.fx into a temporary button OnSelect and click it; that block changes only the palette. |
| 4 | Replace old control references such as Theme.Primary with varAppTheme.Primary. Check all screens and component instance input properties. |
| 5 | Component definitions use their own input properties; leave Access app scope off. Preview defaults may use literal colours. |

## Control styling and manual fallback

| Control/property | Preferred formula | Manual formula |
|---|---|---|
| Primary button Fill / active accent | varAppTheme.Primary | ColorValue("#E20074") |
| Primary button HoverFill | varAppTheme.PrimaryHover | ColorValue("#B5005D") |
| Primary button Color | Color.White | ColorValue("#FFFFFF") |
| Selected card / halo Fill | varAppTheme.Pale | ColorValue("#FDE6F1") |
| Screen Fill | varAppTheme.Page | ColorValue("#F4F6F8") |
| Card Fill | varAppTheme.Surface | ColorValue("#FFFFFF") |
| Heading Color | varAppTheme.Heading | ColorValue("#17253F") |
| Body Color | varAppTheme.Body | ColorValue("#27364F") |
| Muted label Color | varAppTheme.Muted | ColorValue("#667085") |
| BorderColor | varAppTheme.Border | ColorValue("#D8DEE7") |
| Error label Color | varAppTheme.Error | ColorValue("#C50F1F") |
| Completed step colour | varAppTheme.Success | ColorValue("#107C10") |
| SVG primary hex text | varAppTheme.PrimaryHex | "#E20074" |

Classic controls do not use BasePaletteColor: set their Fill, Color, HoverFill and border properties. If a modern control exposes BasePaletteColor, use ColorValue("#E20074") there, but keep the classic form/control types used by these recipes. A manual colour is a fallback and will not update when the global record changes.

## Verify

Check a primary button is magenta, a selected card is pale pink, completed steps remain green, error text remains red, and header/nav instances receive the palette. Run App Checker for unresolved Theme references. The global variable must be initialized before expecting colours in preview.

The global-variable approach follows the [requested theming article](https://www.matthewdevaney.com/power-apps-coding-standards-for-canvas-apps/power-apps-app-theming-guidelines/). Its later comments also discuss named formulas; global variables are chosen here for explicit manual initialization.
''',encoding='utf-8')
index_path=ROOT/'Prod.md'
index=index_path.read_text(encoding='utf-8').replace('1. [Build reusable','1. [Set up the #E20074 global theme](production-guide/02-Theme.md), then [build reusable')
index_path.write_text(index,encoding='utf-8')
