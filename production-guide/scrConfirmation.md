# scrConfirmation — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrConfirmation
  cmpHeaderConfirmation [instance of cmpAppHeader]
  cmpNavConfirmation [instance of cmpAppNav]
  cntScrollConfirmation [Vertical container]
    cntPageConfirmation [plain Container]
      lblHeadingConfirmation [Label]
      lblSubtitleConfirmation [Label]
      cntConfirmationCard [Container]
        lblConfirmationReference [Label]
        lblConfirmationCategory [Label]
        lblConfirmationNominee [Label]
        lblConfirmationTime [Label]
      cntActionsConfirmation [Container]
        btnConfirmationView [Button]
        btnConfirmationMine [Button]
        btnConfirmationNew [Button]
  btnStartNewConfirmation [hidden Button]
  btnGoMineConfirmation [hidden Button]
  cntExitOverlayConfirmation [plain Container]
    cntExitDialogConfirmation [plain Container]
      lblExitMessageConfirmation [Label]
      btnExitCancelConfirmation [Button]
      btnExitDiscardConfirmation [Button]
  cntBusyConfirmation [plain Container]
    lblBusyConfirmation [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrConfirmation.Fill | `varAppTheme.Page` |
| cmpHeaderConfirmation.X / Y | `0 / 0` |
| cmpHeaderConfirmation.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderConfirmation.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderConfirmation.UserText | `User().FullName` |
| cmpHeaderConfirmation.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavConfirmation.X / Y | `0 / cmpHeaderConfirmation.Y+cmpHeaderConfirmation.Height` |
| cmpNavConfirmation.Width / Height | `Parent.Width / 48` |
| cmpNavConfirmation.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavConfirmation.ActiveTab | `""` |
| cntScrollConfirmation.X | `0` |
| cntScrollConfirmation.Y | `cmpNavConfirmation.Y+cmpNavConfirmation.Height` |
| cntScrollConfirmation.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollConfirmation.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollConfirmation.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollConfirmation.LayoutGap / all paddings | `0` |
| cntPageConfirmation.Width | `Min(1030,Parent.Width)` |
| cntPageConfirmation.AlignInContainer | `AlignInContainer.Center` |
| cntPageConfirmation.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageConfirmation.Height | `cntActionsConfirmation.Y+cntActionsConfirmation.Height+If(App.Width<=760,40,56)` |
| lblHeadingConfirmation.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingConfirmation.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingConfirmation.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingConfirmation.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleConfirmation.X / Y | `lblHeadingConfirmation.X / lblHeadingConfirmation.Y+lblHeadingConfirmation.Height+8` |
| lblSubtitleConfirmation.Width / AutoHeight | `lblHeadingConfirmation.Width / true` |
| lblSubtitleConfirmation.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavConfirmation.OnNew | [Copy full formula](fx/cmpNavConfirmation.OnNew.fx) |
| cmpNavConfirmation.OnMine | [Copy full formula](fx/cmpNavConfirmation.OnMine.fx) |
| btnStartNewConfirmation.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineConfirmation.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewConfirmation and btnGoMineConfirmation: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayConfirmation.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayConfirmation.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogConfirmation.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogConfirmation.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogConfirmation.Fill | `varAppTheme.Surface` |
| lblExitMessageConfirmation.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageConfirmation.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelConfirmation.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelConfirmation.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardConfirmation.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardConfirmation.Text | `"Discard"` |
| cntBusyConfirmation.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyConfirmation.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyConfirmation.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyConfirmation.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardConfirmation.OnSelect | [Copy full formula](fx/btnExitDiscardConfirmation.OnSelect.fx) |

## 5. Screen content, buttons and formulas



lblHeadingConfirmation.Text=`"Nomination submitted"`; lblSubtitleConfirmation.Text=`NominationReference`. cntActionsConfirmation.Y=`cntConfirmationCard.Y+cntConfirmationCard.Height+24`.


Inside cntActionsConfirmation, place these classic buttons. For this screen set cntActionsConfirmation.Height=`If(App.Width<=760,150,48)`. Each button Width=`If(App.Width<=760,Parent.Width,Min(240,(Parent.Width-24)/3))`, Height=38; X=`If(App.Width<=760,0,index*(Self.Width+12))`, Y=`If(App.Width<=760,index*50,0)`. Replace index with the literal number in the table; do not create an index variable.

| Index | Exact name | Text | OnSelect / exact block to copy |
|---|---|---|---|

| 0 | btnConfirmationView | View nomination | `complete Return to the existing active form block` |
| 1 | btnConfirmationMine | My nominations | `Select(btnGoMineConfirmation)` |
| 2 | btnConfirmationNew | New nomination | `Select(btnStartNewConfirmation)` |

Create cntConfirmationCard inside cntPageConfirmation: Width=`Min(640,Parent.Width-32)`,X=`(Parent.Width-Self.Width)/2`,Y=lblSubtitleConfirmation.Y+lblSubtitleConfirmation.Height+26,Height=300,Fill=varAppTheme.Surface. Add labels lblConfirmationReference, lblConfirmationCategory, lblConfirmationNominee and lblConfirmationTime inside at X=24,Width=Parent.Width-48,AutoHeight=true. First Y=24, subsequent Y=previous label.Y+previous label.Height+16. Text values are NominationReference,varCategory.Title,NomineeDisplay,Text(varSubmittedOn,"dd mmm yyyy, hh:mm"). Set card Height=lblConfirmationTime.Y+lblConfirmationTime.Height+24. Only form submission success navigates here. View nomination uses the active form already in View mode. No reset in OnVisible.

### Detailed content/control recipe

#### 2. scrConfirmation

Use the page shell without stepper. Center a white card Width `Min(640,parent.Width-32)`, X centered, Y48, padding32. Add native success icon/circle, heading “Nomination submitted”, and labels:

| Label | Text |
|---|---|
| Reference | `NominationReference` |
| Category | `varCategory.Title` |
| Nominee/team | `NomineeDisplay` |
| Time | `Text(varSubmittedOn,"dd mmm yyyy, hh:mm")` |

Time is displayed in the app user's local context; SharePoint stores the underlying date/time. Add View nomination with OnSelect the full Navigate-Active-Form block. Forms have already been placed in View mode by successful submission. Add My nominations → Navigate(scrMyNominations); New nomination → full NewNomination block. No fabricated nominee/reference/date should appear here.


### Event file assignments — paste into these exact properties

| Control / property | Value or formula |
|---|---|
| btnConfirmationView.OnSelect | [Copy full formula](fx/NavigateActiveForm.fx) |
| btnConfirmationMine.OnSelect | [Copy full formula](fx/cmpNavConfirmation.OnMine.fx) |
| btnConfirmationNew.OnSelect | [Copy full formula](fx/cmpNavConfirmation.OnNew.fx) |

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
| cmpHeaderConfirmation.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
