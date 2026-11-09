# scrCategorySelection — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrCategorySelection
  cmpHeaderCategory [instance of cmpAppHeader]
  cmpNavCategory [instance of cmpAppNav]
  cmpStepperCategory [instance of cmpStepper]
  cntScrollCategory [Vertical container]
    cntPageCategory [plain Container]
      lblHeadingCategory [Label]
      lblSubtitleCategory [Label]
      cntCategorySummary [Container]
        lblCategorySummary [Label]
      galCategories [Gallery]
        cntCategoryTile [Container]
          lblCategoryTitle [Label]
          lblCategoryDescription [Label]
          lblCategorySelected [Label]
        btnSelectCategory [Button]
      lblCategoryState [Label]
      cntActionsCategory [Container]
        btnCategoryBack [Button]
        btnCategoryContinue [Button]
      btnLoadCategory [Button]
      btnRefreshCategories [Button]
  btnStartNewCategory [hidden Button]
  btnGoMineCategory [hidden Button]
  cntExitOverlayCategory [plain Container]
    cntExitDialogCategory [plain Container]
      lblExitMessageCategory [Label]
      btnExitCancelCategory [Button]
      btnExitDiscardCategory [Button]
  cntBusyCategory [plain Container]
    lblBusyCategory [Label]
  cntCategoryChangeOverlay [Container]
    cntCategoryChangeDialog [Container]
      lblCategoryChangeMessage [Label]
      btnCategoryChangeCancel [Button]
      btnCategoryChangeConfirm [Button]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrCategorySelection.Fill | `varAppTheme.Page` |
| cmpHeaderCategory.X / Y | `0 / 0` |
| cmpHeaderCategory.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderCategory.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderCategory.UserText | `User().FullName` |
| cmpHeaderCategory.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavCategory.X / Y | `0 / cmpHeaderCategory.Y+cmpHeaderCategory.Height` |
| cmpNavCategory.Width / Height | `Parent.Width / 48` |
| cmpNavCategory.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavCategory.ActiveTab | `"New"` |
| cntScrollCategory.X | `0` |
| cntScrollCategory.Y | `cmpStepperCategory.Y+cmpStepperCategory.Height` |
| cntScrollCategory.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollCategory.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollCategory.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollCategory.LayoutGap / all paddings | `0` |
| cntPageCategory.Width | `Min(1030,Parent.Width)` |
| cntPageCategory.AlignInContainer | `AlignInContainer.Center` |
| cntPageCategory.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageCategory.Height | `cntActionsCategory.Y+cntActionsCategory.Height+If(App.Width<=760,40,56)` |
| lblHeadingCategory.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingCategory.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingCategory.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingCategory.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleCategory.X / Y | `lblHeadingCategory.X / lblHeadingCategory.Y+lblHeadingCategory.Height+8` |
| lblSubtitleCategory.Width / AutoHeight | `lblHeadingCategory.Width / true` |
| lblSubtitleCategory.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |
| cmpStepperCategory.X / Y | `(Parent.Width-Self.Width)/2 / cmpNavCategory.Y+cmpNavCategory.Height` |
| cmpStepperCategory.Width / Height | `Min(1060,Parent.Width) / 94` |
| cmpStepperCategory.CurrentStep | `varCurrentStep` |
| cmpStepperCategory.CurrentHex | `varAppTheme.PrimaryHex` |
| cmpStepperCategory.CompleteHex | `varAppTheme.SuccessHex` |
| cmpStepperCategory.PendingHex | `varAppTheme.BorderHex` |
| cmpStepperCategory.MutedHex | `varAppTheme.MutedHex` |
| cmpStepperCategory.HaloHex | `varAppTheme.PaleHex` |
| Control / property | Value or formula |
|---|---|
| cmpStepperCategory.Steps | [Copy full formula](fx/cmpStepperCategory.Steps.fx) |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavCategory.OnNew | [Copy full formula](fx/cmpNavCategory.OnNew.fx) |
| cmpNavCategory.OnMine | [Copy full formula](fx/cmpNavCategory.OnMine.fx) |
| btnStartNewCategory.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineCategory.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewCategory and btnGoMineCategory: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayCategory.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayCategory.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogCategory.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogCategory.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogCategory.Fill | `varAppTheme.Surface` |
| lblExitMessageCategory.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageCategory.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelCategory.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelCategory.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardCategory.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardCategory.Text | `"Discard"` |
| cntBusyCategory.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyCategory.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyCategory.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyCategory.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardCategory.OnSelect | [Copy full formula](fx/btnExitDiscardCategory.OnSelect.fx) |

## 5. Screen content, buttons and formulas



lblHeadingCategory.Text=`"Award category"`; lblSubtitleCategory.Text=`"Choose the category that best matches the nomination."`. cntActionsCategory.Y=`Max(galCategories.Y+galCategories.Height,lblCategoryState.Y+lblCategoryState.Height)+24`.


Inside cntActionsCategory, place these classic buttons. For this screen set cntActionsCategory.Height=`If(App.Width<=760,100,48)`. Each button Width=`If(App.Width<=760,Parent.Width,Min(240,(Parent.Width-12)/2))`, Height=38; X=`If(App.Width<=760,0,index*(Self.Width+12))`, Y=`If(App.Width<=760,index*50,0)`. Replace index with the literal number in the table; do not create an index variable.

| Index | Exact name | Text | OnSelect / exact block to copy |
|---|---|---|---|

| 0 | btnCategoryBack | Back | `Navigate(scrNomineeDetails,ScreenTransition.None)` |
| 1 | btnCategoryContinue | Continue | `guarded category selection handler in scrCategorySelection recipe` |

Create cntCategorySummary inside cntPageCategory: X/Width match heading,Y=lblSubtitleCategory.Y+lblSubtitleCategory.Height+18,Height=72. Add lblCategorySummary inside, X/Y=16,Width=Parent.Width-32,AutoHeight=true,Text=NomineeDisplay. Create galCategories inside cntPageCategory below summary+22; use the full gallery/template recipe below. Create lblCategoryState below gallery+12, X/Width match heading,AutoHeight=true,Text=`If(varCategoryLoadError,"Categories could not be loaded.",If(IsEmpty(colCategoryOptions),"No categories are currently published for this nomination type.",""))`.

Create hidden btnLoadCategory on this screen, DisplayMode.Edit; its OnSelect uses the complete Category load action. btnCategoryContinue uses the guarded Continue handler in **3. scrCategorySelection**, including varShowCategoryChangeDialog. Add cntCategoryChangeOverlay at screen root, matching the dimensions of cntExitOverlayCategory, Visible=varShowCategoryChangeDialog. Inside add a centered dialog, message, Cancel (`Set(varShowCategoryChangeDialog,false)`) and Confirm (`Select(btnLoadCategory)`) buttons; use the discard-dialog sizes above and unique names lblCategoryChangeMessage, btnCategoryChangeCancel and btnCategoryChangeConfirm. The load handler handles closing/reset only after successful validation. Keep this separate from the top navigation exit dialog. Apply the complete category OnVisible block; do not use only Set(varCurrentStep,2).

### Detailed content/control recipe

#### 3. scrCategorySelection

OnVisible:

[Copy full formula](fx/scrCategorySelection.01.fx) — paste into the property identified immediately above.


This collection is the bounded category configuration (three categories per type), not nomination data. Add heading “Award category” and subtitle “Choose the category that best matches the nomination.” Add a summary strip with current nominee/type. Back OnSelect `Navigate(scrNomineeDetails,ScreenTransition.None)`.

##### A. Category cards

Insert vertical gallery `galCategories` with Items `colCategoryOptions`. Set WrapCount `If(App.Width<=760,1,3)`, TemplatePadding8, TemplateSize261, Width equal to page inner width. Height `If(App.Width<=760,CountRows(colCategoryOptions)*261,261)`. Remove generated image/body controls. Inside each item add a manual container Width `Parent.TemplateWidth-16`, Height245, X8, Y8, Fill `If(ThisItem.ID=varPendingCategory.ID,varAppTheme.Pale,varAppTheme.Surface)`, BorderColor primary if selected else border, BorderThickness2 if selected else1, corner radii8.

Add a small native icon in a 43px pale square, heading Title label X20 Y78 WidthParent.Width-40 AutoHeight Size12.75 Semibold, description X20 Yheadingbottom+10 WidthParent.Width-40 AutoHeight Size9.75, and Selected indicator in top right. Icons can be stable per category code, but text/order/availability come from SharePoint. As a baseline use the same award SVG for all categories; icon differences are cosmetic and do not require new columns. Verify long descriptions fit; increase card/gallery row height together if business copy is longer.

Add a native transparent selection button within the gallery template, outside the decorative container so `ThisItem` is the gallery item. X/Y8, WidthParent.TemplateWidth-16, Height245, Text `""`, AccessibleLabel `"Select " & ThisItem.Title`. OnSelect:

[Copy full formula](fx/scrCategorySelection.02.fx) — paste into the property identified immediately above.


Use a clearly visible focus border. DisplayMode disabled when busy or when a nomination has already been saved. A saved record never changes category/version through this screen.

Empty-state label Visible `!varCategoryLoadError && IsEmpty(colCategoryOptions)`, Text “No categories are currently published for this nomination type.” Error label Visible varCategoryLoadError, Text “Categories could not be loaded. Check the connection and try again.” Add Retry `Select(btnRefreshCategories)` only if a same-screen hidden button holds the OnVisible refresh code; alternatively paste that refresh block directly into Retry. Do not make an empty state look like a loading spinner indefinitely.

##### B. Load the selected question version

Add same-screen hidden `btnLoadCategory`, DisplayMode.Edit, OnSelect the full [Category.Load.OnSelect.fx](Reference.md). It re-reads the selected category/published pointer and validates 3–6 ordered Q1..QN rows before initializing snapshots. Changing an unsaved selection resets all form controls and queued evidence **only after confirmation and successful configuration validation**. Returning to the same selected category preserves current answers and attachments.

Continue DisplayMode:

[Copy full formula](fx/scrCategorySelection.03.fx) — paste into the property identified immediately above.


Continue OnSelect:

[Copy full formula](fx/scrCategorySelection.04.fx) — paste into the property identified immediately above.


Add a modal dialog Visible `varShowCategoryChangeDialog`: “Changing category clears the current responses and selected evidence. Nominee details will be retained.” Cancel `Set(varShowCategoryChangeDialog,false)`. Confirm `Select(btnLoadCategory)`. Disable both while busy. Configuration errors retain the old answers and let the user cancel the dialog.

On each step-3 form, add Change category button Visible `!varReadOnly && IsBlank(varNominationId)`, OnSelect:

[Copy full formula](fx/scrCategorySelection.05.fx) — paste into the property identified immediately above.


No new snapshot is fetched when resuming a saved draft; use the per-category gallery Open formula instead. Seed rows remain inactive until an approved administrator publishes them. The UI must not automatically substitute prototype questions when no published configuration exists.

Continue with the six [typed form recipes](Reference.md), then [review, browse and administration](Reference.md).


### Event file assignments — paste into these exact properties

| Control / property | Value or formula |
|---|---|
| btnLoadCategory.OnSelect | [Copy full formula](fx/Category.Load.OnSelect.fx) |

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
| cmpHeaderCategory.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
