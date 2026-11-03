# Manual build guide — Team and Individual Nomination App

Prepared 31 October 2026 for **Ka6thickMSFT**, using the supplied HTML/CSS and screenshots. This is a manual implementation package, **not a built/importable or Studio-tested Power App**. The SharePoint backend is provisioned; these instructions are the next stage. Keep Contoso branding. No SharePoint columns are added by this guide. Future question tags remain deferred.

## Build in this order

| Stage | File | Result / checkpoint |
|---|---|---|
| 1 | This file | App, connections, settings, screen names, shared state |
| 2 | [01-Screens-and-Layout.md](01-Screens-and-Layout.md) | Header, navigation, responsive page, visual controls |
| 3 | [02-Details-and-Categories.md](02-Details-and-Categories.md) | Nominee details, directory people, category and question loading |
| 4 | [Form-Mapping.md](Form-Mapping.md), then all six `Form-*.md` files | Bound forms, all field updates, draft saves, attachment handling |
| 5 | [03-Review-Browse-and-Administration.md](03-Review-Browse-and-Administration.md) | Review, submit, confirmation, own nominations, question publication |
| 6 | [04-Validation-and-Handover.md](04-Validation-and-Handover.md) | Execute acceptance tests before publishing |

The `.fx` files contain formulas for the **single property named in each filename**. Open as text, copy their entire contents into that property. They are not app packages. `Navigate-Active-Form.fx` is an action block to paste where instructed. Do not paste an `.fx` filename into a formula property. The form recipes have all six list-specific formulas expanded; you do not need to convert one list's Patch formula into another's.

Use classic Label, Text input, Button, Combo box, Checkbox and Edit form controls unless a recipe explicitly says otherwise. Modern controls expose different properties, such as Value rather than Text in some controls; mixing them into these formulas will require adjustments. Formula examples use English authoring separators: commas for function arguments, semicolons for action sequences. Locales using semicolons for arguments require `;;` for action sequences. `App.Formulas` contains named formulas separated by semicolons; paste it into App.Formulas, not OnStart.

## 1. Create the solution and blank app

1. Open the Power Apps maker portal and select **Ka6thickMSFT**. Verify the displayed environment ID before creating resources. No app has yet been created there by this guide.
2. Open Solutions. Create an unmanaged development solution, for example `NominationApp`, with your organization-approved publisher. This is a suggested solution name, not a new SharePoint list.
3. Add a blank Canvas app, tablet/landscape starting layout. Name it `Team and Individual Nominations` or your approved name.
4. Settings → Display: turn **Scale to fit off**, **Lock aspect ratio off**, and allow responsive orientation. Use approximately 1366×768 as the desktop authoring canvas. Test at 390px and 760px as well. Do not enforce a desktop-sized minimum width on every screen. [Microsoft responsive layout guidance](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-responsive-layout).
5. Keep formula-level error management enabled. Save a development version before adding controls. Leave the app unshared until permissions and tests are complete.
6. Create all screens listed below before pasting formulas that reference them. Insert all six forms and connect their data sources before pasting App.OnStart. Unresolved names are expected while the referenced controls have not yet been added; they must be resolved before testing.

| Screen | Purpose |
|---|---|
| `scrHome` | New nomination / My nominations entry |
| `scrNomineeDetails` | Step 1, award type and person/team details |
| `scrCategorySelection` | Step 2, category cards |
| `scrIndividualInnovation` | Step 3, individual innovation form |
| `scrIndividualCustomer` | Step 3, individual customer form |
| `scrIndividualExcellence` | Step 3, individual excellence form |
| `scrTeamCollaboration` | Step 3, team collaboration form |
| `scrTeamImpact` | Step 3, team impact form |
| `scrTeamTransformation` | Step 3, team transformation form |
| `scrReview` | Step 4, current input review / declaration |
| `scrConfirmation` | Successful saved submission |
| `scrMyNominations` | Selected list's own records |
| `scrQuestionAdministration` | Restricted new question-version publication |

Implementation simplification from the earlier screen plan: submitted records use the same six typed forms in `ViewForm` mode; a separate duplicate `scrViewNomination` is not needed. Nominee editing lives on step 1 rather than being duplicated inside every form. Shared visual header/navigation/summary/action-bar controls may be copied initially; only the stepper must be made into a reusable component for this recipe. This avoids requiring preview component behavior events for a manual build.

## 2. Connections and environment portability

Connect these existing AISite lists via the SharePoint connector. The formulas use these stable data-source identifiers:

| Identifier | Role |
|---|---|
| `AwardCategories` | Dynamic category configuration |
| `AwardQuestions` | Versioned dynamic question configuration |
| `Nom_IndividualInnovation` | IND_INNOVATION |
| `Nom_IndividualCustomer` | IND_CUSTOMER |
| `Nom_IndividualExcellence` | IND_EXCELLENCE |
| `Nom_TeamCollaboration` | TEAM_COLLAB |
| `Nom_TeamImpact` | TEAM_IMPACT |
| `Nom_TeamTransformation` | TEAM_TRANSFORM |

Also add **Office 365 Users**, exposed as `Office365Users`, for directory search. Do not copy the prototype's fictional people into the app.

**A list-name text variable cannot bind a Canvas form to a different SharePoint list.** Preserve typed connections. The one-place physical list-name configuration is `provisioning/environment.json`; that file drives provisioning, not runtime Canvas data-source resolution.

For deployment, use a solution SharePoint **Site** data-source environment variable and eight **List** data-source environment variables. In the solution, New → More → Environment variable, select Data source / SharePoint, configure the Site parameter first, then each List using that site. Use the target list GUIDs from `provisioning/deployment-result.json` (not title text) as the list environment-variable values. In Canvas Data → SharePoint, use the Advanced/environment-variable selection to add each configured source. Studio labels can vary; verify each connection actually uses the variables before export. Microsoft documents this binding process and list/site dependency in [data-source environment variables](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables-data-source-canvas-apps).

On import into another environment, provide the new site and list GUIDs in the deployment configuration. Keep schemas and logical app identifiers consistent, rebind connections, and test them. Do not edit every form's source to a runtime `Set(varListName, "...")`. If Studio initially assigns a different source identifier, use its actual identifier consistently throughout the formula package; the current package assumes the eight identifiers above. Never rename SharePoint columns to make a formula compile.

## 3. Shared state and formulas

1. Select App in Tree view. Set **StartScreen** to `scrHome`.
2. Paste [App.Formulas.fx](App.Formulas.fx) into **App.Formulas**. It defines `Theme`, `LevelOptions`, `DetailsValid`, `ResponsesValid`, `NomineeDisplay`, and `NominationReference`.
3. Paste [App.OnStart.fx](App.OnStart.fx) into **App.OnStart**.
4. Run OnStart from the App menu after controls/connections exist. Do not run it during unsaved editing; it intentionally initializes session state.
5. Add a New nomination button on Home. Its OnSelect is [NewNomination.OnSelect.fx](NewNomination.OnSelect.fx). This initializes six blank form contexts and navigates to details. Use the same block only after the discard confirmation described below when leaving an active nomination.

The all-zero object ID in App.OnStart is an intentionally invalid **placeholder** for the administration UI allowlist. Replace/add approved administrators' Entra object IDs, lowercased, when identities are agreed. It grants no SharePoint permission. Do not use the prototype's names/emails for this purpose. Configuration-list permissions must separately restrict writes. Until configured, administration entry remains hidden.

| State | Meaning |
|---|---|
| `varEmployee`, `varPrimaryContact`, `colTeamMembers` | SharePoint-compatible person record(s) |
| `varRole`, `varLevel`, `varTeamName` | Step-1 current inputs |
| `varCategory`, `varQuestionVersion`, `varQuestionCount` | Fixed selection and snapshot version |
| `colAnswers` | Six bounded slots: Slot, Prompt, Required, Response |
| `varRecordII` / IC / IE / TC / TI / TT | Typed saved record per list |
| `varNominationId`, `varLoadedModified` | Save identity and concurrency check |
| `varIsBusy`, `varSaveIntent` | Prevent repeat saves; Draft or Submit |
| `varDeclarationAccepted` | Reset when reviewed data changes |
| `varHasChanges` | Navigation warning, including queued attachments |
| `varReadOnly` | View mode for submitted records |

`colAnswers.Prompt` captures the criterion Title, newline, QuestionText and optional guidance. Thus the existing QnPromptSnapshot fields preserve the full display text without adding a title column. Loading a saved nomination reads those snapshots, never the current question configuration. Old prompts without a newline still display as full prompt text.

## 4. Shared navigation and discard confirmation

Disable all mutation/navigation controls while `varIsBusy`; use `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)`. A busy overlay can also block pointer input, but disabled controls are still required for keyboard users.

On every **working** screen, New nomination and My nominations must confirm when `varHasChanges` is true. Add local hidden buttons `btnStartNewLocal` and `btnGoMineLocal` (use unique screen suffixes in actual names). `btnStartNewLocal.OnSelect` gets the whole NewNomination block. `btnGoMineLocal.OnSelect` is `Set(varShowExitDialog,false); Navigate(scrMyNominations,ScreenTransition.None)`.

New navigation action, using that screen's actual local button name:

```powerfx
If(varHasChanges && !varReadOnly,
    Set(varExitAction, "New"); Set(varShowExitDialog, true),
    Select(btnStartNewLocal)
)
```

My nominations action:

```powerfx
If(varHasChanges && !varReadOnly,
    Set(varExitAction, "Mine"); Set(varShowExitDialog, true),
    Select(btnGoMineLocal)
)
```

Add a full-screen dimmed container and centered white dialog, Visible `varShowExitDialog`, with text **“Leave this nomination? Changes since the last save, including selected files, will be discarded.”** Cancel: `Set(varShowExitDialog,false)`. Discard:

```powerfx
Set(varShowExitDialog, false);
Set(varHasChanges, false);
If(varExitAction = "New", Select(btnStartNewLocal), Select(btnGoMineLocal))
```

`Select` must target a button on the **same screen**. Do not target a hidden action button on a different screen. Hidden action buttons have DisplayMode.Edit; visible callers supply the guard. On My nominations, reopen always resets/reloads the form, so leaving it does not reuse abandoned attachment edits.

Use the same pattern with `varAdminDirty` on the administration screen. To catch closing the browser/player, set App.ConfirmExit to `varHasChanges || varAdminDirty` and ConfirmExitMessage to `"You have unsaved changes."` where the host supports these properties. Verify the warning in your actual host; it is not a server-side save guarantee.

## Current limits and decisions

- Existing categories are **inactive with blank publication pointers**. An empty employee category screen is expected until an approved question version is published. This guide does not activate data automatically.
- L1–L6 and seed wording await business/development approval. Level options are read from SharePoint choice metadata; all six lists must have consistent choices.
- App-only submitted read-only behavior is implemented in these formulas. Strong backend immutability needs the separately agreed permission-enforcement approach. Preflight checks do not create an atomic lock.
- The source HTML's blue `#0f6cbd` is the initial central token. The screenshot appears more violet; change `Theme.PrimaryHex` and `Theme.Primary` together after visual comparison if that accent is preferred.
- Native form controls, font rendering and shadows differ from browser CSS. The guide reproduces structure and dimensions; pixel-level comparison and client testing remain required.

Continue with [01-Screens-and-Layout.md](01-Screens-and-Layout.md).
