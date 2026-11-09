# scrReview — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrReview
  cmpHeaderReview [instance of cmpAppHeader]
  cmpNavReview [instance of cmpAppNav]
  cmpStepperReview [instance of cmpStepper]
  cntScrollReview [Vertical container]
    cntPageReview [plain Container]
      lblHeadingReview [Label]
      lblSubtitleReview [Label]
      cntReviewDetails [Container]
        lblReviewDetails [Label]
        btnReviewEditDetails [Button]
      cntReviewQ1 [Container]
        lblReviewHeading1 [Label]
        lblReviewPrompt1 [Label]
        lblReviewAnswer1 [Label]
      cntReviewQ2 [Container]
        lblReviewHeading2 [Label]
        lblReviewPrompt2 [Label]
        lblReviewAnswer2 [Label]
      cntReviewQ3 [Container]
        lblReviewHeading3 [Label]
        lblReviewPrompt3 [Label]
        lblReviewAnswer3 [Label]
      cntReviewQ4 [Container]
        lblReviewHeading4 [Label]
        lblReviewPrompt4 [Label]
        lblReviewAnswer4 [Label]
      cntReviewQ5 [Container]
        lblReviewHeading5 [Label]
        lblReviewPrompt5 [Label]
        lblReviewAnswer5 [Label]
      cntReviewQ6 [Container]
        lblReviewHeading6 [Label]
        lblReviewPrompt6 [Label]
        lblReviewAnswer6 [Label]
      cntReviewEvidence [Container]
        lblEvidenceHeading [Label]
        lblReviewFiles [Label]
        btnReviewEditEvidence [Button]
      cntDeclaration [Container]
        chkDeclaration [Classic Checkbox]
        lblDeclarationHelp [Label]
      cntActionsReview [Container]
        btnReviewBack [Button]
        btnReviewSubmit [Button]
  btnStartNewReview [hidden Button]
  btnGoMineReview [hidden Button]
  cntExitOverlayReview [plain Container]
    cntExitDialogReview [plain Container]
      lblExitMessageReview [Label]
      btnExitCancelReview [Button]
      btnExitDiscardReview [Button]
  cntBusyReview [plain Container]
    lblBusyReview [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrReview.Fill | `varAppTheme.Page` |
| cmpHeaderReview.X / Y | `0 / 0` |
| cmpHeaderReview.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderReview.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderReview.UserText | `User().FullName` |
| cmpHeaderReview.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavReview.X / Y | `0 / cmpHeaderReview.Y+cmpHeaderReview.Height` |
| cmpNavReview.Width / Height | `Parent.Width / 48` |
| cmpNavReview.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavReview.ActiveTab | `"New"` |
| cntScrollReview.X | `0` |
| cntScrollReview.Y | `cmpStepperReview.Y+cmpStepperReview.Height` |
| cntScrollReview.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollReview.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollReview.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollReview.LayoutGap / all paddings | `0` |
| cntPageReview.Width | `Min(960,Parent.Width)` |
| cntPageReview.AlignInContainer | `AlignInContainer.Center` |
| cntPageReview.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageReview.Height | `cntActionsReview.Y+cntActionsReview.Height+If(App.Width<=760,40,56)` |
| lblHeadingReview.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingReview.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingReview.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingReview.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleReview.X / Y | `lblHeadingReview.X / lblHeadingReview.Y+lblHeadingReview.Height+8` |
| lblSubtitleReview.Width / AutoHeight | `lblHeadingReview.Width / true` |
| lblSubtitleReview.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |
| cmpStepperReview.X / Y | `(Parent.Width-Self.Width)/2 / cmpNavReview.Y+cmpNavReview.Height` |
| cmpStepperReview.Width / Height | `Min(1060,Parent.Width) / 94` |
| cmpStepperReview.CurrentStep | `varCurrentStep` |
| cmpStepperReview.CurrentHex | `varAppTheme.PrimaryHex` |
| cmpStepperReview.CompleteHex | `varAppTheme.SuccessHex` |
| cmpStepperReview.PendingHex | `varAppTheme.BorderHex` |
| cmpStepperReview.MutedHex | `varAppTheme.MutedHex` |
| cmpStepperReview.HaloHex | `varAppTheme.PaleHex` |
| Control / property | Value or formula |
|---|---|
| cmpStepperReview.Steps | [Copy full formula](fx/cmpStepperReview.Steps.fx) |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavReview.OnNew | [Copy full formula](fx/cmpNavReview.OnNew.fx) |
| cmpNavReview.OnMine | [Copy full formula](fx/cmpNavReview.OnMine.fx) |
| btnStartNewReview.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineReview.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewReview and btnGoMineReview: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayReview.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayReview.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogReview.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogReview.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogReview.Fill | `varAppTheme.Surface` |
| lblExitMessageReview.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageReview.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelReview.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelReview.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardReview.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardReview.Text | `"Discard"` |
| cntBusyReview.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyReview.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyReview.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyReview.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardReview.OnSelect | [Copy full formula](fx/btnExitDiscardReview.OnSelect.fx) |

## 5. Screen content, buttons and formulas



lblHeadingReview.Text=`"Review & submit"`; lblSubtitleReview.Text=`"Check the nomination and supporting evidence before submitting."`. cntActionsReview.Y=`cntDeclaration.Y+cntDeclaration.Height+24`.


Inside cntActionsReview, place these classic buttons. For this screen set cntActionsReview.Height=`If(App.Width<=760,100,48)`. Each button Width=`If(App.Width<=760,Parent.Width,Min(240,(Parent.Width-12)/2))`, Height=38; X=`If(App.Width<=760,0,index*(Self.Width+12))`, Y=`If(App.Width<=760,index*50,0)`. Replace index with the literal number in the table; do not create an index variable.

| Index | Exact name | Text | OnSelect / exact block to copy |
|---|---|---|---|

| 0 | btnReviewBack | Back | `Set(varDeclarationAccepted,false); then complete Return to the existing active form block` |
| 1 | btnReviewSubmit | Submit nomination | `complete Review screen Submit button OnSelect block` |

Create cntReviewDetails, cntReviewQ1 through cntReviewQ6, cntReviewEvidence and cntDeclaration inside cntPageReview. Their full content and expanding height formulas are in **1. scrReview** and **Six expanding review question blocks** below. X/Width match lblHeadingReview for all these blocks. cntReviewDetails.Y=lblSubtitleReview.Y+lblSubtitleReview.Height+26. Keep the review inputs in memory; do not refresh saved answers into this page. btnReviewSubmit.DisplayMode is the full declaration/DetailsValid/ResponsesValid/category/read-only guard in the review recipe. btnReviewBack clears declaration and uses the full active-form route without resets. Set screen OnVisible=`Set(varCurrentStep,4)`.

**Review container completion:** cntReviewQ1.Y=`cntReviewDetails.Y+cntReviewDetails.Height+18`; subsequent question Y/Height/Visible use the six expanded review blocks. cntReviewEvidence.Y=`cntReviewQ6.Y+cntReviewQ6.Height+18`. Name the declaration container **cntDeclaration**; X=lblHeadingReview.X,Width=lblHeadingReview.Width,Y=`cntReviewEvidence.Y+cntReviewEvidence.Height+18`. Place chkDeclaration inside it as documented. Add lblDeclarationHelp inside, X=20,Width=Parent.Width-40,Y=`chkDeclaration.Y+chkDeclaration.Height+12`,AutoHeight=true,Text="Submitting saves this nomination. Submitted nominations are read-only in this app." Set cntDeclaration.Height=`lblDeclarationHelp.Y+lblDeclarationHelp.Height+28`. These exact names complete the cntActionsReview.Y dependency.


### Detailed content/control recipe

#### 1. scrReview

Use the 960px centered page shell. OnVisible:

[Copy full formula](fx/scrReview.01.fx) — paste into the property identified immediately above.


Heading “Review & submit”; subtitle “Check the nomination and supporting evidence before submitting.” Step-3 Review buttons already validate required details/responses and capture text controls directly into colAnswers, plus filenames into colReviewFiles. They reset declaration each time. Never re-query nomination answers from SharePoint for this review; that would omit current unsaved changes.

##### A. Details summary

Add white `cntReviewDetails`, X/Width same as page heading, Y after subtitle+26, padding28. Add `lblReviewDetails` X28 Y24 WidthParent.Width-56, AutoHeight true, Size9.75, Text:

[Copy full formula](fx/scrReview.02.fx) — paste into the property identified immediately above.


For closer desktop fidelity, split this label into two columns of the same fields: left nominee/type/nominator, right category/role/level. Use 18px vertical and50px horizontal gaps; stack at760px. The one-label formula above is the simplest complete accessible fallback and preserves all information without clipping.

Add Edit details native button X28, Y `lblReviewDetails.Y+lblReviewDetails.Height+16`, Width120, Height38. OnSelect:

[Copy full formula](fx/scrReview.03.fx) — paste into the property identified immediately above.


cntReviewDetails.Height = edit button Y+Height+24. Do not auto-reset form controls when entering details; the following Continue goes back to the existing typed form, preserving queued files.

##### B. All questions and answers

Build the six expanding read-only blocks exactly as [Review-Question-Controls.md](Reference.md). Prompts/answers are dynamic snapshots, not hardcoded category text. All answer labels have AutoHeight true. The source prototype's five-line clipping is deliberately not carried over: the user must see the entire answer before accepting the declaration.

##### C. Evidence review

Add `cntReviewEvidence` after the final question block, same X/Width, white card, padding28. Heading “Supporting evidence”. Add Label `lblReviewFiles`, X28 Y58 WidthParent.Width-56, AutoHeight true, Text:

[Copy full formula](fx/scrReview.04.fx) — paste into the property identified immediately above.


This is the pending attachment filename list captured from the current native form. Files are not uploaded until SubmitForm. To inspect/add/remove evidence, return to the original form. Add Edit responses and evidence button below this label; OnSelect:

[Copy full formula](fx/scrReview.05.fx) — paste into the property identified immediately above.


Immediately after that statement paste the full action block from [Navigate-Active-Form.fx](Reference.md). Do not call NewForm/ResetForm. Set cntReviewEvidence.Height to edit button Y+Height+24.

##### D. Declaration and Submit

Add a white declaration card below evidence+18, same X/Width. Classic Checkbox `chkDeclaration`, X20 Y16 WidthParent.Width-40 Height80 (increase if text wraps on mobile), Text “I confirm that the information in this nomination is accurate and appropriate to submit.” This is proposed UI wording; replace with the approved declaration before release. Default `varDeclarationAccepted`; OnCheck `Set(varDeclarationAccepted,true)`; OnUncheck `Set(varDeclarationAccepted,false)`; DisplayMode disabled while varIsBusy.

Add helper label: “Submitting saves this nomination. Submitted nominations are read-only in this app.” Do not claim a notification email was sent; no notification flow is included. Card Height = checkbox Y+Height+helper Height+28.

Below add Back and Submit nomination buttons. Back resets declaration then uses Navigate-Active-Form.fx. Submit.OnSelect is the complete [Review.Submit.OnSelect.fx](Reference.md). Submit.DisplayMode:

[Copy full formula](fx/scrReview.06.fx) — paste into the property identified immediately above.


The file contains all six routing branches, fresh saved-item status/Modified checks, SaveIntent and SubmitForm calls. Each form's OnSuccess captures LastSubmit/ID, sets EditForm for subsequent saves, and performs the final status update only when SaveIntent is Submit. The busy state remains true through both phases. Navigation to confirmation occurs only in the successful status-update branch.

If the final status update fails, the first save has already returned an ID. Retain that ID, show the failure and check the current server status before retrying. A network timeout can make the outcome uncertain even if the server committed; do not promise that such an item definitely remains a Draft. Likewise, if the initial new-item SubmitForm times out before LastSubmit is returned, check My nominations before retrying creation. The fixed schema has no client-generated idempotency key, so exactly-once creation under an ambiguous network failure cannot be guaranteed by these client formulas.

### Six expanding review question blocks

Create these six manual containers directly in the review page content container, after `cntReviewDetails`. They display the complete current prompts and responses. Use no input controls and no fixed-line clipping. All labels use Segoe UI and wrap. Each container Fill = varAppTheme.Surface, BorderColor = varAppTheme.Border, BorderThickness = 1, corner radii = 8. The formula for its Height refers only to its children, not its parent Height, avoiding a layout cycle.

For the first container use X = `cntReviewDetails.X`, Width = `cntReviewDetails.Width`. Use that same X/Width for the remaining five. `cntReviewDetails` must have its explicit Height from the main review guide.

#### Review slot 1

| Control / property | Value |
|---|---|
| `cntReviewQ1.Y` | `cntReviewDetails.Y+cntReviewDetails.Height+If(1<=varQuestionCount,18,0)` |
| `cntReviewQ1.Visible` | `1<=varQuestionCount` |
| `cntReviewQ1.Height` | `If(Self.Visible,lblReviewAnswer1.Y+lblReviewAnswer1.Height+24,0)` |
| `lblReviewHeading1` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `varAppTheme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1"))` |
| `lblReviewPrompt1` | X `28`; Y `lblReviewHeading1.Y+lblReviewHeading1.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer1` | X `28`; Y `lblReviewPrompt1.Y+lblReviewPrompt1.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=1,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 2

| Control / property | Value |
|---|---|
| `cntReviewQ2.Y` | `cntReviewQ1.Y+cntReviewQ1.Height+If(2<=varQuestionCount,18,0)` |
| `cntReviewQ2.Visible` | `2<=varQuestionCount` |
| `cntReviewQ2.Height` | `If(Self.Visible,lblReviewAnswer2.Y+lblReviewAnswer2.Height+24,0)` |
| `lblReviewHeading2` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `varAppTheme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2"))` |
| `lblReviewPrompt2` | X `28`; Y `lblReviewHeading2.Y+lblReviewHeading2.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer2` | X `28`; Y `lblReviewPrompt2.Y+lblReviewPrompt2.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=2,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 3

| Control / property | Value |
|---|---|
| `cntReviewQ3.Y` | `cntReviewQ2.Y+cntReviewQ2.Height+If(3<=varQuestionCount,18,0)` |
| `cntReviewQ3.Visible` | `3<=varQuestionCount` |
| `cntReviewQ3.Height` | `If(Self.Visible,lblReviewAnswer3.Y+lblReviewAnswer3.Height+24,0)` |
| `lblReviewHeading3` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `varAppTheme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3"))` |
| `lblReviewPrompt3` | X `28`; Y `lblReviewHeading3.Y+lblReviewHeading3.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer3` | X `28`; Y `lblReviewPrompt3.Y+lblReviewPrompt3.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=3,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 4

| Control / property | Value |
|---|---|
| `cntReviewQ4.Y` | `cntReviewQ3.Y+cntReviewQ3.Height+If(4<=varQuestionCount,18,0)` |
| `cntReviewQ4.Visible` | `4<=varQuestionCount` |
| `cntReviewQ4.Height` | `If(Self.Visible,lblReviewAnswer4.Y+lblReviewAnswer4.Height+24,0)` |
| `lblReviewHeading4` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `varAppTheme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4"))` |
| `lblReviewPrompt4` | X `28`; Y `lblReviewHeading4.Y+lblReviewHeading4.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer4` | X `28`; Y `lblReviewPrompt4.Y+lblReviewPrompt4.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=4,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 5

| Control / property | Value |
|---|---|
| `cntReviewQ5.Y` | `cntReviewQ4.Y+cntReviewQ4.Height+If(5<=varQuestionCount,18,0)` |
| `cntReviewQ5.Visible` | `5<=varQuestionCount` |
| `cntReviewQ5.Height` | `If(Self.Visible,lblReviewAnswer5.Y+lblReviewAnswer5.Height+24,0)` |
| `lblReviewHeading5` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `varAppTheme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5"))` |
| `lblReviewPrompt5` | X `28`; Y `lblReviewHeading5.Y+lblReviewHeading5.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer5` | X `28`; Y `lblReviewPrompt5.Y+lblReviewPrompt5.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=5,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 6

| Control / property | Value |
|---|---|
| `cntReviewQ6.Y` | `cntReviewQ5.Y+cntReviewQ5.Height+If(6<=varQuestionCount,18,0)` |
| `cntReviewQ6.Visible` | `6<=varQuestionCount` |
| `cntReviewQ6.Height` | `If(Self.Visible,lblReviewAnswer6.Y+lblReviewAnswer6.Height+24,0)` |
| `lblReviewHeading6` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `varAppTheme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6"))` |
| `lblReviewPrompt6` | X `28`; Y `lblReviewHeading6.Y+lblReviewHeading6.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer6` | X `28`; Y `lblReviewPrompt6.Y+lblReviewPrompt6.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `varAppTheme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=6,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

Place `cntReviewEvidence.Y` at `cntReviewQ6.Y+cntReviewQ6.Height+18`. Hidden trailing question containers have zero Height and add no gap.


### Event file assignments — paste into these exact properties

| Control / property | Value or formula |
|---|---|
| btnReviewSubmit.OnSelect | [Copy full formula](fx/Review.Submit.OnSelect.fx) |
| btnReviewBack.OnSelect | [Copy full formula](fx/Review.Back.fx) |
| btnReviewEditEvidence.OnSelect | [Copy full formula](fx/Review.Back.fx) |

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
| cmpHeaderReview.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
