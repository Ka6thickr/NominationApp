# scrQuestionAdministration — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrQuestionAdministration
  cmpHeaderAdmin [instance of cmpAppHeader]
  cmpNavAdmin [instance of cmpAppNav]
  cntScrollAdmin [Vertical container]
    cntPageAdmin [plain Container]
      lblHeadingAdmin [Label]
      lblSubtitleAdmin [Label]
      lblAdminDenied [Label]
      cntAdminEditor [Container]
        cmbAdminCategory [Classic Combo box]
        lblAdminVersion [Label]
        btnAdminCopyVersion [Button]
        galAdminQuestions [Gallery]
          lblAdminSlot [Label]
          txtAdminTitle [Classic Text input]
          txtAdminQuestion [Classic Text input]
          txtAdminGuidance [Classic Text input]
          chkAdminRequired [Classic Checkbox]
        btnAdminAddQuestion [Button]
        btnAdminRemoveQuestion [Button]
        galAdminPreview [Gallery]
          lblAdminPreview [Label]
        galAdminErrors [Gallery]
          lblAdminError [Label]
      cntActionsAdmin [Container]
        btnAdminPublish [Button]
        btnAdminFreshVersion [Button]
      btnAdminLoadCopy [Button]
  btnStartNewAdmin [hidden Button]
  btnGoMineAdmin [hidden Button]
  cntExitOverlayAdmin [plain Container]
    cntExitDialogAdmin [plain Container]
      lblExitMessageAdmin [Label]
      btnExitCancelAdmin [Button]
      btnExitDiscardAdmin [Button]
  cntBusyAdmin [plain Container]
    lblBusyAdmin [Label]
  cntAdminDiscardOverlay [Container]
    cntAdminDiscardDialog [Container]
      lblAdminDiscardMessage [Label]
      btnAdminDiscardCancel [Button]
      btnAdminDiscardConfirm [Button]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrQuestionAdministration.Fill | `varAppTheme.Page` |
| cmpHeaderAdmin.X / Y | `0 / 0` |
| cmpHeaderAdmin.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderAdmin.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderAdmin.UserText | `User().FullName` |
| cmpHeaderAdmin.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavAdmin.X / Y | `0 / cmpHeaderAdmin.Y+cmpHeaderAdmin.Height` |
| cmpNavAdmin.Width / Height | `Parent.Width / 48` |
| cmpNavAdmin.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavAdmin.ActiveTab | `""` |
| cntScrollAdmin.X | `0` |
| cntScrollAdmin.Y | `cmpNavAdmin.Y+cmpNavAdmin.Height` |
| cntScrollAdmin.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollAdmin.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollAdmin.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollAdmin.LayoutGap / all paddings | `0` |
| cntPageAdmin.Width | `Min(1030,Parent.Width)` |
| cntPageAdmin.AlignInContainer | `AlignInContainer.Center` |
| cntPageAdmin.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageAdmin.Height | `cntActionsAdmin.Y+cntActionsAdmin.Height+If(App.Width<=760,40,56)` |
| lblHeadingAdmin.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingAdmin.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingAdmin.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingAdmin.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleAdmin.X / Y | `lblHeadingAdmin.X / lblHeadingAdmin.Y+lblHeadingAdmin.Height+8` |
| lblSubtitleAdmin.Width / AutoHeight | `lblHeadingAdmin.Width / true` |
| lblSubtitleAdmin.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavAdmin.OnNew | [Copy full formula](fx/cmpNavAdmin.OnNew.fx) |
| cmpNavAdmin.OnMine | [Copy full formula](fx/cmpNavAdmin.OnMine.fx) |
| btnStartNewAdmin.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineAdmin.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewAdmin and btnGoMineAdmin: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayAdmin.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayAdmin.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogAdmin.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogAdmin.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogAdmin.Fill | `varAppTheme.Surface` |
| lblExitMessageAdmin.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageAdmin.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelAdmin.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelAdmin.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardAdmin.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardAdmin.Text | `"Discard"` |
| cntBusyAdmin.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyAdmin.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyAdmin.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyAdmin.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardAdmin.OnSelect | [Copy full formula](fx/btnExitDiscardAdmin.OnSelect.fx) |

## 5. Screen content, buttons and formulas



lblHeadingAdmin.Text=`"Manage award questions"`; lblSubtitleAdmin.Text=`"Create a new question version and publish after checking it."`. cntActionsAdmin.Y=`cntAdminEditor.Y+cntAdminEditor.Height+24`.


Inside cntActionsAdmin, place these classic buttons. For this screen set cntActionsAdmin.Height=`If(App.Width<=760,100,48)`. Each button Width=`If(App.Width<=760,Parent.Width,Min(240,(Parent.Width-12)/2))`, Height=38; X=`If(App.Width<=760,0,index*(Self.Width+12))`, Y=`If(App.Width<=760,index*50,0)`. Replace index with the literal number in the table; do not create an index variable.

| Index | Exact name | Text | OnSelect / exact block to copy |
|---|---|---|---|

| 0 | btnAdminPublish | Publish new version | `complete Question administration Publish button OnSelect block` |
| 1 | btnAdminFreshVersion | Use fresh version | `complete Use a fresh version number action in admin recipe` |

Create cntAdminEditor inside cntPageAdmin, X/Width match heading,Y=lblSubtitleAdmin.Y+lblSubtitleAdmin.Height+26,Visible=varCanManageQuestions. Place cmbAdminCategory and btnAdminCopyVersion at top; copy button Text="Copy to new version". Add same-screen hidden btnAdminLoadCopy with the complete load/copy action. btnAdminCopyVersion uses the guarded varAdminDirty action from the admin recipe.

Create galAdminQuestions inside cntAdminEditor using the exact input/control names and slot updates from **4. scrQuestionAdministration**. Add galAdminPreview below the editor gallery and galAdminErrors below the preview, Items=colPublishErrors, TemplateSize=60,Height=`CountRows(colPublishErrors)*60`; set editor Height=galAdminErrors.Y+galAdminErrors.Height+24. Grow editor/preview gallery row heights to fit all fields; retain their documented local collection binding. Set cntActionsAdmin.Visible=varCanManageQuestions; apply the full Publish button DisplayMode guard from the recipe. Add lblAdminDenied at page root, same X/Width as heading,Y=lblSubtitleAdmin.Y+lblSubtitleAdmin.Height+26,AutoHeight=true,Visible=`!varCanManageQuestions`,Text="You do not have access to question administration".

Create cntAdminDiscardOverlay at screen root, matching the exit-overlay layout, Visible=varShowAdminDiscard. Add uniquely named Cancel (`Set(varShowAdminDiscard,false)`) and Confirm (`Set(varShowAdminDiscard,false); Select(btnAdminLoadCopy)`) buttons and a message that unsaved question edits will be discarded. Keep this dialog separate from top navigation. Apply the complete admin OnVisible block and admin action recipes. UI gating does not replace SharePoint configuration-list permissions.

**Admin editor placement:** cmbAdminCategory X=20,Y=20,Width=`Parent.Width-40`,Height=40. btnAdminCopyVersion X=20,Y=`cmbAdminCategory.Y+cmbAdminCategory.Height+12`,Width=220,Height=38. galAdminQuestions X=20,Y=`btnAdminCopyVersion.Y+btnAdminCopyVersion.Height+20`,Width=`Parent.Width-40`,TemplateSize=`If(App.Width<=760,520,440)`,Height=`Min(1000,CountRows(colAdminQuestions)*Self.TemplateSize)`. Keep the gallery scrolling. galAdminPreview X=20,Y=`galAdminQuestions.Y+galAdminQuestions.Height+20`,Width=Parent.Width-40,TemplateSize=180,Height=`Min(540,CountRows(colAdminQuestions)*180)`,Items=`Sort(colAdminQuestions,Slot,SortOrder.Ascending)`. Its label Text=`ThisItem.Title & Char(10) & ThisItem.QuestionText & Char(10) & ThisItem.GuidanceText`,X/Y=12,Width=Parent.TemplateWidth-24,AutoHeight=true; increase TemplateSize if actual approved content wraps beyond 156 units. galAdminErrors X=20,Y=`galAdminPreview.Y+galAdminPreview.Height+20`,Width=Parent.Width-40; template label X/Y=8,Width=Parent.TemplateWidth-16,AutoHeight=true,Text=`Text(ThisItem.Slot) & ": " & ThisItem.Message`. Increase error TemplateSize if text does not fit. These properties complete cntAdminEditor.Height and cntActionsAdmin.Y dependencies.


### Detailed content/control recipe

#### 4. scrQuestionAdministration

This stage is included so question wording, guidance, required flags and count stay dynamic. Publication is a deliberate administrator action and activates the category. Do not publish the current seed wording/levels until approved for the intended development or production use. The guide itself does not change the live publication state.

Use the page shell without stepper; heading “Manage award questions”. The main editing container Visible `varCanManageQuestions`. If false, show “You do not have access to question administration” plus a Home button. All load/publish handlers also check the flag, but **the real write restriction is SharePoint permissions**, not this variable.

OnVisible:

[Copy full formula](fx/scrQuestionAdministration.01.fx) — paste into the property identified immediately above.


##### A. Category and new version

Add `cmbAdminCategory`: Items colAdminCategories; DisplayFields `["Title"]`; SelectMultiple false; IsSearchable false. Add label displaying loaded category, published version and editing version:

[Copy full formula](fx/scrQuestionAdministration.02.fx) — paste into the property identified immediately above.


Add hidden local button `btnAdminLoadCopy`, OnSelect full [Admin.LoadCopy.OnSelect.fx](Reference.md). Visible button “Copy to new version” has DisplayMode disabled when no selected ID or busy. OnSelect:

[Copy full formula](fx/scrQuestionAdministration.03.fx) — paste into the property identified immediately above.


Add dialog Visible varShowAdminDiscard, text “Discard local question edits and load the selected category?”. Cancel sets false; Confirm sets false then Select(btnAdminLoadCopy). Initialize varShowAdminDiscard false in App.OnStart. The load code selects the current published version, or highest staged version when none is published; it allocates highest existing version+1. It never edits a previously saved question row. Test delegation for the filtered/sorted highest-version query before relying on a long version history. It assumes a coordinated single publisher per category; it is not a distributed version allocator.

##### B. Editor gallery

Use a vertical gallery `galAdminQuestions`, Items `Sort(colAdminQuestions,Slot,SortOrder.Ascending)`, TemplateSize440, TemplatePadding12, Height `Min(1000,CountRows(colAdminQuestions)*440)`. At 390px use TemplateSize520. Keep the gallery scrollable and the Publish/Preview buttons visible below or in a sticky action area.

Inside each template create the following controls with **these exact names** (gallery controls have one name reused across rows):

| Control | Core properties |
|---|---|
| Slot label | Text `"Q" & Text(ThisItem.Slot)`; X16 Y12; Height24; Semibold |
| `txtAdminTitle` | Default `ThisItem.Title`; X16 Y48; WidthParent.TemplateWidth-32; Height40; MaxLength255; single-line; accessible label “Criterion title” |
| `txtAdminQuestion` | Default `ThisItem.QuestionText`; X16 Y110; Width same; Height120; Mode TextMode.MultiLine; accessible label “Question text” |
| `txtAdminGuidance` | Default `ThisItem.GuidanceText`; X16 Y254; Width same; Height100; Mode TextMode.MultiLine; accessible label “Optional guidance” |
| `chkAdminRequired` | Default `ThisItem.IsRequired`; X16 Y374; Height40; Text “Required response” |

Add native field labels in the gaps above the text inputs; on mobile expand TemplateSize/positions as needed to avoid overlaps. Text controls DelayOutput false, DisplayMode disabled while busy. Each OnChange patches only the local collection:

[Copy full formula](fx/scrQuestionAdministration.04.fx) — paste into the property identified immediately above.


txtAdminQuestion uses `{QuestionText:Self.Text}`; txtAdminGuidance uses `{GuidanceText:Self.Text}`. Checkbox OnCheck uses `{IsRequired:true}`, OnUncheck `{IsRequired:false}`, followed by Set(varAdminDirty,true). No SharePoint writes occur while typing. Unlike employee responses, this is a bounded administrator editor with at most six rows. The Publish action also captures currently realized editor values before validating to avoid losing a last focused edit.

Add question button DisplayMode disabled if CountRows(colAdminQuestions)>=6 or busy; OnSelect:

[Copy full formula](fx/scrQuestionAdministration.05.fx) — paste into the property identified immediately above.


Remove last question button disabled at<=3; OnSelect:

[Copy full formula](fx/scrQuestionAdministration.06.fx) — paste into the property identified immediately above.


Removing only the last local slot keeps Q1..QN contiguous. To reorder content, edit the local slots' contents; do not renumber published rows or change ConfigurationKey. No saved SharePoint rows are deleted by this editor.

##### C. Preview and publish

Add a preview panel or read-only gallery Items `Sort(colAdminQuestions,Slot,SortOrder.Ascending)`. Show Title, QuestionText, GuidanceText and required marker with the same fonts/card styling as employee cards. The preview does not set varCategory/colAnswers or overwrite an employee nomination in progress. If there are unsaved employee changes, navigate to Admin only through a discard/save confirmation.

Add “Publish new version and activate category” button. DisplayMode:

[Copy full formula](fx/scrQuestionAdministration.07.fx) — paste into the property identified immediately above.


OnSelect is the complete [Admin.Publish.OnSelect.fx](Reference.md). It requires a successful configuration load, captures local editor values, validates 3–6 contiguous slots, checks the old category pointer, creates missing question rows, checks any existing keys match exactly, re-reads the saved set, checks the pointer again, then updates PublishedQuestionVersion and IsActive **last**. A failed load cannot publish stale editor content under a newly selected category. It never overwrites existing published rows. Add errors gallery Items colPublishErrors, labels ThisItem.Slot/Message.

If a row save fails, the category pointer is unchanged by that attempt and partial new-version rows may remain. Retry with identical content can reuse matching keys. If content has changed since a partial save, do not overwrite those keys: allocate a fresh version while retaining local edits. Add “Use a fresh version number” button, DisplayMode disabled while busy/no category; OnSelect:

[Copy full formula](fx/scrQuestionAdministration.08.fx) — paste into the property identified immediately above.


A pointer-update timeout has an uncertain outcome; refresh before retrying. Coordinate one publisher per category. Strong concurrent publication requires a serialized backend mechanism, which is outside this fixed-schema manual Canvas implementation. Keep old versions and snapshots intact.

##### D. Category descriptions and inactive state

The six category codes/destinations are fixed. Authorized managers can change Title, Description and DisplayOrder in the AwardCategories SharePoint list; the app reads them dynamically. IsActive=false removes a category from new nominations but does not hide history in My nominations. Do not change CategoryCode, delete categories used by nominations, or set PublishedQuestionVersion to an unvalidated set. Adding a seventh category requires a new agreed source/form mapping, not only a config row.

No tag editors/columns are included. The proposed three question tags need a later storage and UX decision.


### Event file assignments — paste into these exact properties

| Control / property | Value or formula |
|---|---|
| btnAdminLoadCopy.OnSelect | [Copy full formula](fx/Admin.LoadCopy.OnSelect.fx) |
| btnAdminPublish.OnSelect | [Copy full formula](fx/Admin.Publish.OnSelect.fx) |

## 6. Verify before the next screen

| Check | Expected |
|---|---|
| Tree view | Matches the listed parents; no duplicate existing form |
| Components | Header/nav built once; instances have values/events |
| Scroll | Last input, error and action reachable at desktop/mobile widths |
| Cancel | Unsaved answers and queued files retained |
| Formulas | No unresolved names; English separators or locale equivalent |
| Runtime | Test synthetic draft/save/reopen before submission |

## Header image and theme initialization

| Control / property | Value or formula |
|---|---|
| cmpHeaderAdmin.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
