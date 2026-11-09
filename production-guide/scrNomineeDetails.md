# scrNomineeDetails — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrNomineeDetails
  cmpHeaderDetails [instance of cmpAppHeader]
  cmpNavDetails [instance of cmpAppNav]
  cmpStepperDetails [instance of cmpStepper]
  cntScrollDetails [Vertical container]
    cntPageDetails [plain Container]
      lblHeadingDetails [Label]
      lblSubtitleDetails [Label]
      cntDetailsCard [Container]
        lblType [Label]
        btnIndividualType [Button]
        btnTeamType [Button]
        lblNominator [Label]
        lblNominatorValue [Label]
        lblNominee [Label]
        cmbNominee [Classic Combo box]
        cntTeamDetails [Container]
          lblTeamName [Label]
          txtTeamName [Classic Text input]
          lblPrimaryContact [Label]
          cmbPrimaryContact [Classic Combo box]
          lblTeamMembers [Label]
          cmbTeamMemberToAdd [Classic Combo box]
          btnAddTeamMember [Button]
          galTeamMembers [Gallery]
            lblMemberName [Label]
            btnRemoveTeamMember [Button]
        cntRoleLevel [Container]
          lblRole [Label]
          txtRole [Classic Text input]
          lblLevel [Label]
          cmbLevel [Classic Combo box]
        lblDetailsHelp [Label]
      cntActionsDetails [Container]
        btnDetailsContinue [Button]
  btnStartNewDetails [hidden Button]
  btnGoMineDetails [hidden Button]
  cntExitOverlayDetails [plain Container]
    cntExitDialogDetails [plain Container]
      lblExitMessageDetails [Label]
      btnExitCancelDetails [Button]
      btnExitDiscardDetails [Button]
  cntBusyDetails [plain Container]
    lblBusyDetails [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrNomineeDetails.Fill | `varAppTheme.Page` |
| cmpHeaderDetails.X / Y | `0 / 0` |
| cmpHeaderDetails.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderDetails.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderDetails.UserText | `User().FullName` |
| cmpHeaderDetails.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavDetails.X / Y | `0 / cmpHeaderDetails.Y+cmpHeaderDetails.Height` |
| cmpNavDetails.Width / Height | `Parent.Width / 48` |
| cmpNavDetails.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavDetails.ActiveTab | `"New"` |
| cntScrollDetails.X | `0` |
| cntScrollDetails.Y | `cmpStepperDetails.Y+cmpStepperDetails.Height` |
| cntScrollDetails.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollDetails.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollDetails.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollDetails.LayoutGap / all paddings | `0` |
| cntPageDetails.Width | `Min(1030,Parent.Width)` |
| cntPageDetails.AlignInContainer | `AlignInContainer.Center` |
| cntPageDetails.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageDetails.Height | `cntActionsDetails.Y+cntActionsDetails.Height+If(App.Width<=760,40,56)` |
| lblHeadingDetails.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingDetails.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingDetails.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingDetails.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleDetails.X / Y | `lblHeadingDetails.X / lblHeadingDetails.Y+lblHeadingDetails.Height+8` |
| lblSubtitleDetails.Width / AutoHeight | `lblHeadingDetails.Width / true` |
| lblSubtitleDetails.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |
| cmpStepperDetails.X / Y | `(Parent.Width-Self.Width)/2 / cmpNavDetails.Y+cmpNavDetails.Height` |
| cmpStepperDetails.Width / Height | `Min(1060,Parent.Width) / 94` |
| cmpStepperDetails.CurrentStep | `varCurrentStep` |
| cmpStepperDetails.CurrentHex | `varAppTheme.PrimaryHex` |
| cmpStepperDetails.CompleteHex | `varAppTheme.SuccessHex` |
| cmpStepperDetails.PendingHex | `varAppTheme.BorderHex` |
| cmpStepperDetails.MutedHex | `varAppTheme.MutedHex` |
| cmpStepperDetails.HaloHex | `varAppTheme.PaleHex` |
| Control / property | Value or formula |
|---|---|
| cmpStepperDetails.Steps | [Copy full formula](fx/cmpStepperDetails.Steps.fx) |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavDetails.OnNew | [Copy full formula](fx/cmpNavDetails.OnNew.fx) |
| cmpNavDetails.OnMine | [Copy full formula](fx/cmpNavDetails.OnMine.fx) |
| btnStartNewDetails.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineDetails.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewDetails and btnGoMineDetails: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayDetails.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayDetails.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogDetails.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogDetails.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogDetails.Fill | `varAppTheme.Surface` |
| lblExitMessageDetails.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageDetails.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelDetails.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelDetails.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardDetails.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardDetails.Text | `"Discard"` |
| cntBusyDetails.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyDetails.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyDetails.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyDetails.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardDetails.OnSelect | [Copy full formula](fx/btnExitDiscardDetails.OnSelect.fx) |

## 5. Screen content, buttons and formulas



lblHeadingDetails.Text=`"Nominee details"`; lblSubtitleDetails.Text=`"Choose the nomination type and tell us who you are recognizing."`. cntActionsDetails.Y=`cntDetailsCard.Y+cntDetailsCard.Height+24`.


Inside cntActionsDetails, place these classic buttons. For this screen set cntActionsDetails.Height=`If(App.Width<=760,50,48)`. Each button Width=`If(App.Width<=760,Parent.Width,Min(240,(Parent.Width-0)/1))`, Height=38; X=`If(App.Width<=760,0,index*(Self.Width+12))`, Y=`If(App.Width<=760,index*50,0)`. Replace index with the literal number in the table; do not create an index variable.

| Index | Exact name | Text | OnSelect / exact block to copy |
|---|---|---|---|

| 0 | btnDetailsContinue | Continue | `complete Details Continue button OnSelect block` |

Create cntDetailsCard inside cntPageDetails: X=lblHeadingDetails.X,Width=lblHeadingDetails.Width,Y=lblSubtitleDetails.Y+lblSubtitleDetails.Height+26,Fill=varAppTheme.Surface. Build the type/person/team/role/level controls from **2. scrNomineeDetails** below inside this card, keeping their exact names for the shared formulas. Name the final helper label lblDetailsHelp; place it after the last level input, AutoHeight=true; cntDetailsCard.Height=`lblDetailsHelp.Y+lblDetailsHelp.Height+30`. btnDetailsContinue.DisplayMode=`If(varIsBusy,DisplayMode.Disabled,DisplayMode.Edit)`; incomplete details may proceed for draft saving. Screen OnVisible=`Set(varCurrentStep,1)`.

### Detailed content/control recipe

#### 2. scrNomineeDetails

OnVisible:

[Copy full formula](fx/scrNomineeDetails.01.fx) — paste into the property identified immediately above.


Heading “Nominee details”; subtitle “Choose the nomination type and tell us who you are recognizing.” These are UI instructions, not question content. Add white `cntDetailsCard` with the card styling in the layout guide. X/Width match the page heading; Y after subtitle +26. Internal horizontal padding `If(App.Width<=760,17,34)` and top padding `If(App.Width<=760,21,30)`. In the measurements below, `padding` means the expression `If(App.Width<=760,17,34)`, not an undeclared Power Fx variable. Use native controls in the following order. For each successive field label set Y to the previous visible control's Y+Height+18; its input starts at label.Y+label.Height+7. Use zero Height for hidden nominee/team sections so following fields move upward.

##### A. Type cards

Add label “Nomination type”, then `btnIndividualType` and `btnTeamType`, approximately 103px high. Desktop widths `(Min(590,Parent.Width-2*padding)-16)/2`, horizontal gap16; mobile stack, full available width. Use Fill `If(varAwardType="Individual",varAppTheme.Pale,varAppTheme.Surface)` for Individual, analogous Team; BorderColor primary when selected else border; BorderThickness 2 when selected else1; corner radii7. Text “Individual award” / “Team award”, Size12.75, Semibold, Align.Left, PaddingLeft18. A check icon or label with “Selected” is visible only on the selected card.

Individual OnSelect:

[Copy full formula](fx/scrNomineeDetails.02.fx) — paste into the property identified immediately above.


Team OnSelect changes the literal to `"Team"`. DisplayMode for both:

[Copy full formula](fx/scrNomineeDetails.03.fx) — paste into the property identified immediately above.


Award type locks once questions have been loaded, even before the first save, to avoid applying team inputs to an individual form. To start a different type after that point, use New nomination and confirm discarding unsaved changes. Before category selection, changing the type may retain hidden in-memory detail values for convenience; only the chosen type is stored by its typed form. There is no silent default category.

##### B. Nominator

Label “Nominated by”; read-only person row Text `User().FullName & Char(10) & varUserEmail`. Width `Min(590,Parent.Width-2*padding)`, Height56, Size9.75, white/pale fill. This is the signed-in nominator, never an editable field. On resumed records the form saves its loaded `varNominator`; My nominations only opens the current user's records.

##### C. Individual nominee — cmbNominee

Visible `varAwardType="Individual"`. Label “Nominee *”. Use a classic single-select Combo box `cmbNominee`, 56px high, width up to590. Apply directory style from the layout guide. Items:

[Copy full formula](fx/scrNomineeDetails.04.fx) — paste into the property identified immediately above.


This is a bounded directory search, not a locally copied directory. Search term and returned field names come from [Office 365 Users SearchUserV2](https://learn.microsoft.com/en-us/connectors/office365users/). Show helper text “Enter at least two characters. If no results appear, refine the search or check the directory connection.” Tenant policies can affect results; test with real authorized accounts.

DefaultSelectedItems:

[Copy full formula](fx/scrNomineeDetails.05.fx) — paste into the property identified immediately above.


OnChange:

[Copy full formula](fx/scrNomineeDetails.06.fx) — paste into the property identified immediately above.


Use UPN for the membership claim and Mail for display where available; do not assume they are always identical. Test guest identities separately if they will be allowed. The fixed schema does not include a guest/employee eligibility policy.

##### D. Team controls

Put these in manual container `cntTeamDetails` with Visible `varAwardType="Team"`, Height based on its last child. When hidden set its Height to0 so following fields move up. Add:

1. `txtTeamName`, label “Team name *”, Default `varTeamName`, MaxLength255, single-line. OnChange: `Set(varTeamName,Self.Text); Set(varHasChanges,true); Set(varDetailsComplete,false); Set(varDeclarationAccepted,false)`.
2. `cmbPrimaryContact`, label “Primary contact *”. Same directory Items formula and Combo styling as cmbNominee. DefaultSelectedItems uses `varPrimaryContact` instead of `varEmployee`. Its full OnChange is the cmbNominee formula with only `varEmployee` changed to `varPrimaryContact`.
3. `cmbTeamMemberToAdd`, label “Team members (optional)”, same directory Items, DefaultSelectedItems `Blank()`, SelectMultiple false. An Add member button appears alongside it. We use explicit Add/Remove so selected members remain visible even when a new directory search changes the result set.
4. Gallery `galTeamMembers`, Items `colTeamMembers`, TemplateSize40, Height `Min(200,CountRows(colTeamMembers)*40)`, ShowScrollbar true. Labels show ThisItem.DisplayName; remove icon/button OnSelect `Remove(colTeamMembers,ThisItem); Set(varHasChanges,true); Set(varDeclarationAccepted,false)`. Disable removal while busy/read-only.

Add member button OnSelect:

[Copy full formula](fx/scrNomineeDetails.07.fx) — paste into the property identified immediately above.


Team members are optional and may include the primary contact unless business rules later say otherwise. Do not invent a mandatory team-member count.

##### E. Role and level

Below the visible nominee/team section add `cntRoleLevel`. Width `Min(590,card.Width-2*padding)`. Desktop Height80, mobile Height170. Role label “Nominee role *” for Individual, “Primary contact role *” for Team. Level label likewise. Desktop two columns `(Parent.Width-18)/2`; mobile full width, level starts90px below role.

`txtRole`: Default `varRole`; MaxLength255; Height40. OnChange:

[Copy full formula](fx/scrNomineeDetails.08.fx) — paste into the property identified immediately above.


`cmbLevel`: classic Combo, SelectMultiple false; IsSearchable false; DisplayFields `["Value"]`; SearchFields `["Value"]`; Height40; InputTextPlaceholder “Select level”. Items read actual choice metadata:

[Copy full formula](fx/scrNomineeDetails.09.fx) — paste into the property identified immediately above.


The same expression is defined centrally as `LevelOptions` in App.Formulas, so you can set Items to `LevelOptions`. Before category selection the IndividualInnovation list supplies the common level choices; maintain identical choice values across all six lists. DefaultSelectedItems `Filter(LevelOptions,Value=varLevel)`. DetailsValid also checks the level is still an allowed choice. OnChange:

[Copy full formula](fx/scrNomineeDetails.10.fx) — paste into the property identified immediately above.


Below controls show a muted helper: “Required details are needed before review. You can select a category and save an incomplete draft.” `cntDetailsCard.Height` = last helper Y + Height +30; action row below card+24. Continue OnSelect is [Details.Continue.OnSelect.fx](Reference.md). It captures text values directly, then goes to category selection, or back to the existing form when a category is already loaded. Continue is allowed with incomplete details **to permit incomplete drafts**; review is not. Save draft is not present on this screen because a new record may not yet have a destination.


### Event file assignments — paste into these exact properties

| Control / property | Value or formula |
|---|---|
| btnDetailsContinue.OnSelect | [Copy full formula](fx/Details.Continue.OnSelect.fx) |

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
| cmpHeaderDetails.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
