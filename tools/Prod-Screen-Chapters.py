"""Expand screen-specific containers, navigation, dialogs and action placement."""
import re

SCREENS = [
 ('scrBestInnovatorIndividual','II',1180,3,'BestInnovatorIndividual'),
 ('scrMDAward','IC',1180,3,'MDAward'),
 ('scrTrendMarcherAward','IE',1180,3,'TrendMarcherAward'),
 ('scrBestInnovatorTeam','TC',1180,3,'BestInnovatorTeam'),
 ('scrMDAwardTeam','TI',1180,3,'MDAwardTeam'),
 ('scrSpecialTeamAward','TT',1180,3,'SpecialTeamAward'),
 ('scrHome','Home',1030,0,''), ('scrNomineeDetails','Details',1030,1,''),
 ('scrCategorySelection','Category',1030,2,''), ('scrReview','Review',960,4,''),
 ('scrConfirmation','Confirmation',1030,0,''), ('scrMyNominations','Mine',1030,0,''),
 ('scrQuestionAdministration','Admin',1030,0,'')]

def chapters():
    out=['''# Screen-by-screen construction — start here

This section fills the naming, parent/container and button-placement gaps in the original reference. These are new controls to create unless they already exist in your app. Keep the corrected II/IC forms. All names below are app-wide unique. Screen-specific instructions take precedence over generic `cntScroll`, `cntPage`, `hdr`, `innerX`, `innerWidth` and `lastControl` examples in the reference appendix. Those generic terms are explanations, not controls or variables to create.

The latest II/IC corrections are user-confirmed; the older export audit later in this file is historical evidence, not a request to repeat completed changes. Actual rendering/runtime still needs verification. The exact MD screen is scrMDAward.

**Work order:** construct the first award shell, finish the other five award shells, then Home → Details → Category → My nominations → Review → Confirmation → Administration. Create all referenced form/control dependencies before running App.OnStart. The shared App/formula and component sections remain complete below.

## Screen index

''']
    out += [f'- [{s} — exact controls and build order](#build-{p.lower()})' for s,p,w,step,n in SCREENS]
    for screen,p,width,step,destination in SCREENS:
        show='true' if step else 'false'
        end=f'cntActions{p}.Y+cntActions{p}.Height+If(App.Width<=760,40,56)'
        out.append(f'''
<a id="build-{p.lower()}"></a>
## {screen} — exact controls and build order

### 1. Tree structure and creation order

Select {screen}. Create the following manual containers directly on the screen, except cntScroll{p}, which is a **vertical auto-layout container**. Create cntPage{p} as a **manual container inside cntScroll{p}**. Do not place the header, navigation or modal overlay inside the scroll viewport.

```text
{screen}
  cntHeader{p}
    lblBrand{p}, lblAppTitle{p}, lblUser{p}
  cntNav{p}
    btnNavNew{p}, btnNavMine{p}
  cntStepperStrip{p}
    {'cmpStepper'+p if step else '(no component needed; strip hidden)'}
  cntScroll{p}
    cntPage{p}
      lblHeading{p}, lblSubtitle{p}
      (screen content specified below)
      cntActions{p}
  btnStartNew{p}, btnGoMine{p} (hidden action helpers)
  cntExitOverlay{p}
    cntExitDialog{p}
      lblExitMessage{p}, btnExitCancel{p}, btnExitDiscard{p}
  cntBusy{p}
    lblBusy{p}
```

### 2. Container properties — use these exact names

Set Screen.Fill=`Theme.Page`. Set header/nav/stepper Fill=`Theme.Surface`.

| Control | X | Y | Width | Height |
|---|---|---|---|---|
| cntHeader{p} | `0` | `0` | `Parent.Width` | `If(App.Width<=760,58,64)` |
| cntNav{p} | `0` | `cntHeader{p}.Y+cntHeader{p}.Height` | `Parent.Width` | `48` |
| cntStepperStrip{p} | `0` | `cntNav{p}.Y+cntNav{p}.Height` | `Parent.Width` | `{'94' if step else '0'}` |
| cntScroll{p} | `0` | `cntStepperStrip{p}.Y+cntStepperStrip{p}.Height` | `Parent.Width` | `Max(0,Parent.Height-Self.Y)` |
| cntPage{p} | Auto-layout parent controls position | Auto-layout parent controls position | `Min({width},Parent.Width)` | `{end}` |
| cntActions{p} | `lblHeading{p}.X` | Screen-specific formula below | `lblHeading{p}.Width` | `If(App.Width<=760,96,48)` |

cntStepperStrip{p}.Visible=`{show}`. For cntScroll{p}, set LayoutDirection=`LayoutDirection.Vertical`, LayoutOverflowY=`LayoutOverflow.Scroll`, LayoutOverflowX=`LayoutOverflow.Hide`, LayoutGap=0 and all paddings=0. For cntPage{p}, set AlignInContainer=`AlignInContainer.Center`, FillPortions=0, LayoutMinWidth=0, LayoutMinHeight=0; disable Flexible height. Temporarily use Height=800 until cntActions{p} exists, then apply the final Height above. Do not set the page Height to Parent.Height.

### 3. Heading and top navigation

Create classic labels. lblHeading{p}: X=`If(App.Width<=760,16,24)`, Y=`If(App.Width<=760,27,39)`, Width=`Parent.Width-2*Self.X`, AutoHeight=true, Size=`If(App.Width<=760,18.75,22.5)`, Font=`Font.'Segoe UI'`, FontWeight=FontWeight.Semibold, Color=Theme.Heading. lblSubtitle{p}: same X/Width, Y=`lblHeading{p}.Y+lblHeading{p}.Height+8`, AutoHeight=true, Size=11.25, Color=Theme.Muted.

Inside cntHeader{p}: lblBrand{p} Text=Theme.Brand, X=54, Y=16, Width=76, Height=28; lblAppTitle{p} Text=Theme.AppTitle, X=144, Y=18, Width=`Max(0,Parent.Width-374)`, Height=28, Visible=`App.Width>760`; lblUser{p} Text=User().FullName, X=`Max(140,Parent.Width-210)`, Y=18, Width=190, Height=28, Visible=`App.Width>760`. Use Segoe UI and Theme.Heading. Add the award logo from the shared SVG reference as imgLogo{p}, X=16, Y=`(Parent.Height-28)/2`, Width/Height=28, AccessibleLabel=`Theme.Brand & " awards"`. Do not use prototype user names.

Inside cntNav{p}: btnNavNew{p}, Text="New nomination", X=16, Y=5, Width=150, Height=38; btnNavMine{p}, Text="My nominations", X=174, Y=5, Width=150, Height=38. Both DisplayMode=`If(varIsBusy,DisplayMode.Disabled,DisplayMode.Edit)`. For widths below 340 reduce both button widths proportionally. Use transparent Fill, Theme.Primary text, and visible keyboard focus borders.

### 4. Navigation actions and discard dialog

Create hidden native btnStartNew{p} and btnGoMine{p} **on this screen**, Visible=false, DisplayMode=DisplayMode.Edit. btnStartNew{p}.OnSelect is the complete [New nomination action](#new-nomination-action-after-any-required-discard-confirmation) below. btnGoMine{p}.OnSelect=`Navigate(scrMyNominations,ScreenTransition.None)`. Select must not target a helper on another screen.

btnNavNew{p}.OnSelect:

```powerfx
If(varHasChanges && !varReadOnly{' || varAdminDirty' if p=='Admin' else ''},
    Set(varExitAction,"New"); Set(varShowExitDialog,true),
    Select(btnStartNew{p})
)
```

btnNavMine{p}.OnSelect:

```powerfx
If(varHasChanges && !varReadOnly{' || varAdminDirty' if p=='Admin' else ''},
    Set(varExitAction,"Mine"); Set(varShowExitDialog,true),
    Select(btnGoMine{p})
)
```

cntExitOverlay{p}: X/Y=0, Width/Height=Parent.Width/Parent.Height, Fill=`RGBA(0,0,0,0.35)`, Visible=varShowExitDialog. cntExitDialog{p} inside it: Width=`Min(440,Parent.Width-32)`, Height=220, X=`(Parent.Width-Self.Width)/2`, Y=`Max(16,(Parent.Height-Self.Height)/2)`, Fill=Theme.Surface. lblExitMessage{p}: X/Y=20, Width=Parent.Width-40, Height=112, Text="Leave this page? Unsaved changes and selected files will be discarded."; Wrap=true. btnExitCancel{p}: X=20,Y=160,Width=110,Height=38,Text="Cancel",OnSelect=`Set(varShowExitDialog,false)`. btnExitDiscard{p}: X=`Parent.Width-140`,Y=160,Width=120,Height=38,Text="Discard", OnSelect:

```powerfx
Set(varShowExitDialog,false);
Set(varHasChanges,false);
{'Set(varAdminDirty,false);' if p=='Admin' else ''}
If(varExitAction="New",Select(btnStartNew{p}),Select(btnGoMine{p}))
```

### 5. Busy layer and button style

Create cntBusy{p} last at screen root: X/Y=0, Width/Height=Parent.Width/Parent.Height, Fill=`RGBA(255,255,255,0.65)`, Visible=varIsBusy. lblBusy{p}: Text="Saving or loading…", X=0, Y=`(Parent.Height-40)/2`, Width=Parent.Width, Height=40, Align=Align.Center. Keep buttons disabled while busy; the overlay alone is not the validation guard.

For action buttons use Height=38, Font=`Font.'Segoe UI'`, Size=10.5, radius=4, FocusedBorderThickness=2. Primary actions Fill=Theme.Primary, Color=Color.White; secondary actions Fill=Theme.Surface, Color=Theme.Primary, BorderColor=Theme.Border, BorderThickness=1. Keep each handler's validation conditions below.

### 6. Screen content and action container
''')
        if destination:
            out.append(f'''Keep frm{destination} inside cntPage{p}. Also create lblSaveError{p}, cntSummary{p}, cntProgress{p} and cntActions{p} inside that page. Use [the exact placement table](#scr{destination.lower()}--placement) below for each coordinate; it expands every reference for this screen.

cntActions{p}.Y=`Max(frm{destination}.Y+frm{destination}.Height,If(lblSaveError{p}.Visible,lblSaveError{p}.Y+lblSaveError{p}.Height,0),cntProgress{p}.Y+cntProgress{p}.Height)+20`.

Inside cntSummary{p}, create lblSummary{p}: X=20,Y=16,Width=`Max(0,Parent.Width-160)`,AutoHeight=true,Text=`Coalesce(NomineeDisplay,"Details incomplete") & "  •  " & varAwardType & " award" & Char(10) & NominationReference`. Create btnEditDetails{p}: Text="Edit details", X=`Parent.Width-130`,Y=16,Width=110,Height=38,Visible=`!varReadOnly`,OnSelect=`Select(btn{p}Back)`.

Inside cntProgress{p}, create lblProgress{p}: X/Y=16,Width=Parent.Width-32,AutoHeight=true,Text=`Text(CountIf(colAnswers,Slot<=varQuestionCount && !IsBlank(Trim(Response)))) & " of " & Text(varQuestionCount) & " responses entered"`. Add lblProgressHelp{p}: X=16,Y=`lblProgress{p}.Y+lblProgress{p}.Height+10`,Width=Parent.Width-32,AutoHeight=true,Text="Required responses must be completed before review. You can save an incomplete draft.",Visible=`!varReadOnly`. Grow the progress container if long text exceeds its planned height; the action-row Max formula prevents overlap.

| Button in cntActions{p} | X | Y | Width | Text / action |
|---|---|---|---|---|
| btn{p}Back | `0` | `0` | `80` | Back / full Back to details block in this form's recipe |
| btn{p}SaveDraft | `If(App.Width<=760,92,Parent.Width-278)` | `0` | `120` | Save draft / full btn{p}SaveDraft.OnSelect |
| btn{p}Review | `If(App.Width<=760,0,Parent.Width-146)` | `If(App.Width<=760,50,0)` | `If(App.Width<=760,Parent.Width,146)` | Review / full btn{p}Review.OnSelect |
| btn{p}BackToMine | `0` | `0` | `180` | My nominations / `Select(btnNavMine{p})` |

First three buttons Visible=`!varReadOnly`; btn{p}BackToMine.Visible=varReadOnly. Back DisplayMode disables while busy; Save disables while busy/read-only/no category; Review disables while busy/read-only. Copy the complete actions from [this form's recipe](#form-{p.lower()}); do not replace capture/preflight/save handlers with a simple Navigate. Set screen OnVisible=`Set(varCurrentStep,3)`.
''')
        else:
            configs={
             'Home':('"Employee & Team Recognition Awards"','"Recognize a colleague or team."','lblSubtitleHome.Y+lblSubtitleHome.Height+26', [('btnHomeNew','New nomination','Select(btnNavNewHome)'),('btnHomeMine','My nominations','Select(btnNavMineHome)'),('btnHomeAdmin','Manage questions','Navigate(scrQuestionAdministration,ScreenTransition.None)')]),
             'Details':('"Nominee details"','"Choose the nomination type and tell us who you are recognizing."','cntDetailsCard.Y+cntDetailsCard.Height+24',[('btnDetailsContinue','Continue','complete Details Continue button OnSelect block')]),
             'Category':('"Award category"','"Choose the category that best matches the nomination."','Max(galCategories.Y+galCategories.Height,lblCategoryState.Y+lblCategoryState.Height)+24',[('btnCategoryBack','Back','Navigate(scrNomineeDetails,ScreenTransition.None)'),('btnCategoryContinue','Continue','guarded category selection handler in scrCategorySelection recipe')]),
             'Review':('"Review & submit"','"Check the nomination and supporting evidence before submitting."','cntDeclaration.Y+cntDeclaration.Height+24',[('btnReviewBack','Back','Set(varDeclarationAccepted,false); then complete Return to the existing active form block'),('btnReviewSubmit','Submit nomination','complete Review screen Submit button OnSelect block')]),
             'Confirmation':('"Nomination submitted"','NominationReference','cntConfirmationCard.Y+cntConfirmationCard.Height+24',[('btnConfirmationView','View nomination','complete Return to the existing active form block'),('btnConfirmationMine','My nominations','Select(btnNavMineConfirmation)'),('btnConfirmationNew','New nomination','Select(btnNavNewConfirmation)')]),
             'Mine':('"My nominations"','"View submitted nominations or continue a draft."','cntMineResults.Y+cntMineResults.Height+24',[('btnMineNew','New nomination','Select(btnNavNewMine)')]),
             'Admin':('"Manage award questions"','"Create a new question version and publish after checking it."','cntAdminEditor.Y+cntAdminEditor.Height+24',[('btnAdminPublish','Publish new version','complete Question administration Publish button OnSelect block'),('btnAdminFreshVersion','Use fresh version','complete Use a fresh version number action in admin recipe')])}
            title,subtitle,y,buttons=configs[p]
            out.append(f'lblHeading{p}.Text=`{title}`; lblSubtitle{p}.Text=`{subtitle}`. cntActions{p}.Y=`{y}`.\n\n')
            out.append(f'Inside cntActions{p}, place these classic buttons. For this screen set cntActions{p}.Height=`If(App.Width<=760,{len(buttons)*50},48)`. Each button Width=`If(App.Width<=760,Parent.Width,Min(240,(Parent.Width-{(len(buttons)-1)*12})/{len(buttons)}))`, Height=38; X=`If(App.Width<=760,0,index*(Self.Width+12))`, Y=`If(App.Width<=760,index*50,0)`. Replace index with the literal number in the table; do not create an index variable.\n\n| Index | Exact name | Text | OnSelect / exact block to copy |\n|---|---|---|---|\n')
            out += [f'| {i} | {b} | {t} | `{a}` |' for i,(b,t,a) in enumerate(buttons)]
            out.append('\n'+shared_content(p))
        if p=='Review':
            out.append('''
**Review container completion:** cntReviewQ1.Y=`cntReviewDetails.Y+cntReviewDetails.Height+18`; subsequent question Y/Height/Visible use the six expanded review blocks. cntReviewEvidence.Y=`cntReviewQ6.Y+cntReviewQ6.Height+18`. Name the declaration container **cntDeclaration**; X=lblHeadingReview.X,Width=lblHeadingReview.Width,Y=`cntReviewEvidence.Y+cntReviewEvidence.Height+18`. Place chkDeclaration inside it as documented. Add lblDeclarationHelp inside, X=20,Width=Parent.Width-40,Y=`chkDeclaration.Y+chkDeclaration.Height+12`,AutoHeight=true,Text="Submitting saves this nomination. Submitted nominations are read-only in this app." Set cntDeclaration.Height=`lblDeclarationHelp.Y+lblDeclarationHelp.Height+28`. These exact names complete the cntActionsReview.Y dependency.
''')
        if p=='Admin':
            out.append('''
**Admin editor placement:** cmbAdminCategory X=20,Y=20,Width=`Parent.Width-40`,Height=40. btnAdminCopyVersion X=20,Y=`cmbAdminCategory.Y+cmbAdminCategory.Height+12`,Width=220,Height=38. galAdminQuestions X=20,Y=`btnAdminCopyVersion.Y+btnAdminCopyVersion.Height+20`,Width=`Parent.Width-40`,TemplateSize=`If(App.Width<=760,520,440)`,Height=`Min(1000,CountRows(colAdminQuestions)*Self.TemplateSize)`. Keep the gallery scrolling. galAdminPreview X=20,Y=`galAdminQuestions.Y+galAdminQuestions.Height+20`,Width=Parent.Width-40,TemplateSize=180,Height=`Min(540,CountRows(colAdminQuestions)*180)`,Items=`Sort(colAdminQuestions,Slot,SortOrder.Ascending)`. Its label Text=`ThisItem.Title & Char(10) & ThisItem.QuestionText & Char(10) & ThisItem.GuidanceText`,X/Y=12,Width=Parent.TemplateWidth-24,AutoHeight=true; increase TemplateSize if actual approved content wraps beyond 156 units. galAdminErrors X=20,Y=`galAdminPreview.Y+galAdminPreview.Height+20`,Width=Parent.Width-40; template label X/Y=8,Width=Parent.TemplateWidth-16,AutoHeight=true,Text=`Text(ThisItem.Slot) & ": " & ThisItem.Message`. Increase error TemplateSize if text does not fit. These properties complete cntAdminEditor.Height and cntActionsAdmin.Y dependencies.
''')
        if p=='Mine':
            out.append('''
**Filter placement:** preserve the existing filter-control names and OnChange formulas in the browse recipe. Place the Individual/Team selector first, cmbBrowseCategory second, status selector third and txtBrowseId fourth. Give each control a 20-unit label and 40-unit editor. On desktop allocate four equal columns with 12-unit gaps and X=`16+index*((Parent.Width-68)/4+12)`,Width=`(Parent.Width-68)/4`, label Y=8/editor Y=32. On mobile stack four rows with label Y=`12+index*76`, editor Y=label.Y+22, X=16,Width=Parent.Width-32; override cntMineFilters.Height=`If(App.Width<=760,332,100)`. Here index is the literal 0,1,2,3 for the controls in that order. Keep all result galleries at the same origin so only the selected one occupies the viewport.
''')
        if step:
            out.append(f'''### 7. Stepper instance for {screen}

Create component definition cmpStepper once from the full component section. Insert instance **cmpStepper{p}** into cntStepperStrip{p}. Set Width=`Min(1060,Parent.Width)`, X=`(Parent.Width-Self.Width)/2`,Y=0,Height=94,CurrentStep=varCurrentStep. Bind CurrentHex=Theme.PrimaryHex,CompleteHex=Theme.SuccessHex,PendingHex=Theme.BorderHex,MutedHex=Theme.MutedHex,HaloHex=Theme.PaleHex. Steps:

```powerfx
Table(
 {{StepNo:1,Label:"Nominee details",IsComplete:varDetailsComplete}},
 {{StepNo:2,Label:"Award category",IsComplete:varCategoryComplete}},
 {{StepNo:3,Label:"Criteria & evidence",IsComplete:varResponsesComplete}},
 {{StepNo:4,Label:"Review & submit",IsComplete:varSubmissionComplete}}
)
```
''')
        out.append(f'''### Checkpoint — {screen}

- [ ] Each named control exists under the parent stated above; no duplicate form was created.
- [ ] No formula contains unexplained example tokens such as innerX or lastControl.
- [ ] At desktop and mobile widths, scroll to the final action and all error text.
- [ ] Busy state prevents duplicate actions; discard Cancel preserves inputs/files.
- [ ] Configure the content handlers from the screen's full recipe; resolve App Checker errors before runtime tests.
''')
    return '\n'.join(out)

def shared_content(p):
    return {
      'Home':'btnHomeAdmin.Visible=varCanManageQuestions. Keep Home OnVisible free of form resets. The New action resets all six form contexts only after discard handling. No stepper instance is required.',
      'Details':'''Create cntDetailsCard inside cntPageDetails: X=lblHeadingDetails.X,Width=lblHeadingDetails.Width,Y=lblSubtitleDetails.Y+lblSubtitleDetails.Height+26,Fill=Theme.Surface. Build the type/person/team/role/level controls from **2. scrNomineeDetails** below inside this card, keeping their exact names for the shared formulas. Name the final helper label lblDetailsHelp; place it after the last level input, AutoHeight=true; cntDetailsCard.Height=`lblDetailsHelp.Y+lblDetailsHelp.Height+30`. btnDetailsContinue.DisplayMode=`If(varIsBusy,DisplayMode.Disabled,DisplayMode.Edit)`; incomplete details may proceed for draft saving. Screen OnVisible=`Set(varCurrentStep,1)`.''',
      'Category':'''Create cntCategorySummary inside cntPageCategory: X/Width match heading,Y=lblSubtitleCategory.Y+lblSubtitleCategory.Height+18,Height=72. Add lblCategorySummary inside, X/Y=16,Width=Parent.Width-32,AutoHeight=true,Text=NomineeDisplay. Create galCategories inside cntPageCategory below summary+22; use the full gallery/template recipe below. Create lblCategoryState below gallery+12, X/Width match heading,AutoHeight=true,Text=`If(varCategoryLoadError,"Categories could not be loaded.",If(IsEmpty(colCategoryOptions),"No categories are currently published for this nomination type.",""))`.

Create hidden btnLoadCategory on this screen, DisplayMode.Edit; its OnSelect uses the complete Category load action. btnCategoryContinue uses the guarded Continue handler in **3. scrCategorySelection**, including varShowCategoryChangeDialog. Add cntCategoryChangeOverlay at screen root, matching the dimensions of cntExitOverlayCategory, Visible=varShowCategoryChangeDialog. Inside add a centered dialog, message, Cancel (`Set(varShowCategoryChangeDialog,false)`) and Confirm (`Select(btnLoadCategory)`) buttons; use the discard-dialog sizes above and unique names lblCategoryChangeMessage, btnCategoryChangeCancel and btnCategoryChangeConfirm. The load handler handles closing/reset only after successful validation. Keep this separate from the top navigation exit dialog. Apply the complete category OnVisible block; do not use only Set(varCurrentStep,2).''',
      'Review':'''Create cntReviewDetails, cntReviewQ1 through cntReviewQ6, cntReviewEvidence and cntDeclaration inside cntPageReview. Their full content and expanding height formulas are in **1. scrReview** and **Six expanding review question blocks** below. X/Width match lblHeadingReview for all these blocks. cntReviewDetails.Y=lblSubtitleReview.Y+lblSubtitleReview.Height+26. Keep the review inputs in memory; do not refresh saved answers into this page. btnReviewSubmit.DisplayMode is the full declaration/DetailsValid/ResponsesValid/category/read-only guard in the review recipe. btnReviewBack clears declaration and uses the full active-form route without resets. Set screen OnVisible=`Set(varCurrentStep,4)`.''',
      'Confirmation':'''Create cntConfirmationCard inside cntPageConfirmation: Width=`Min(640,Parent.Width-32)`,X=`(Parent.Width-Self.Width)/2`,Y=lblSubtitleConfirmation.Y+lblSubtitleConfirmation.Height+26,Height=300,Fill=Theme.Surface. Add labels lblConfirmationReference, lblConfirmationCategory, lblConfirmationNominee and lblConfirmationTime inside at X=24,Width=Parent.Width-48,AutoHeight=true. First Y=24, subsequent Y=previous label.Y+previous label.Height+16. Text values are NominationReference,varCategory.Title,NomineeDisplay,Text(varSubmittedOn,"dd mmm yyyy, hh:mm"). Set card Height=lblConfirmationTime.Y+lblConfirmationTime.Height+24. Only form submission success navigates here. View nomination uses the active form already in View mode. No reset in OnVisible.''',
      'Mine':'''Create cntMineFilters inside cntPageMine: X/Width match heading,Y=lblSubtitleMine.Y+lblSubtitleMine.Height+26,Height=If(App.Width<=760,240,100). Place the filter controls named in **3. scrMyNominations** inside, stacked on mobile. Create cntMineResults below filters+20, X/Width match heading,Height=600. Place galMineII,galMineIC,galMineIE,galMineTC,galMineTI,galMineTT inside it with X/Y=0,Width/Height=Parent.Width/Parent.Height. Only the selected category gallery is Visible. This is a deliberately bounded scrolling results gallery so delegated records can load; it is not an unbounded collection. Apply the six typed Items/OnSelect recipes from their form sections. Apply the complete My nominations OnVisible refresh block. Keep content height fixed to allow gallery virtualization; page scroll still reaches the action row.''',
      'Admin':'''Create cntAdminEditor inside cntPageAdmin, X/Width match heading,Y=lblSubtitleAdmin.Y+lblSubtitleAdmin.Height+26,Visible=varCanManageQuestions. Place cmbAdminCategory and btnAdminCopyVersion at top; copy button Text="Copy to new version". Add same-screen hidden btnAdminLoadCopy with the complete load/copy action. btnAdminCopyVersion uses the guarded varAdminDirty action from the admin recipe.

Create galAdminQuestions inside cntAdminEditor using the exact input/control names and slot updates from **4. scrQuestionAdministration**. Add galAdminPreview below the editor gallery and galAdminErrors below the preview, Items=colPublishErrors, TemplateSize=60,Height=`CountRows(colPublishErrors)*60`; set editor Height=galAdminErrors.Y+galAdminErrors.Height+24. Grow editor/preview gallery row heights to fit all fields; retain their documented local collection binding. Set cntActionsAdmin.Visible=varCanManageQuestions; apply the full Publish button DisplayMode guard from the recipe. Add lblAdminDenied at page root, same X/Width as heading,Y=lblSubtitleAdmin.Y+lblSubtitleAdmin.Height+26,AutoHeight=true,Visible=`!varCanManageQuestions`,Text="You do not have access to question administration".

Create cntAdminDiscardOverlay at screen root, matching the exit-overlay layout, Visible=varShowAdminDiscard. Add uniquely named Cancel (`Set(varShowAdminDiscard,false)`) and Confirm (`Set(varShowAdminDiscard,false); Select(btnAdminLoadCopy)`) buttons and a message that unsaved question edits will be discarded. Keep this dialog separate from top navigation. Apply the complete admin OnVisible block and admin action recipes. UI gating does not replace SharePoint configuration-list permissions.'''
    }[p]
