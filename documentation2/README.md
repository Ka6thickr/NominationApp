# Nomination App — fresh manual setup, version 2

This package supersedes the old list-name references for your new manual build. It does not rename or create live lists, migrate records, or modify the existing Canvas app. All runtime tests remain pending. Keep the original columns and Contoso branding; three question tags remain deferred.

## List mapping

The new list names are assigned in the order supplied. Category codes, screen names, control names and variable names remain stable. A list name does not change the category's displayed title or question wording; maintain those in AwardCategories and AwardQuestions. In particular, BestInnovatorIndividual currently routes through the existing IND_EXCELLENCE contract, and BestInnovatorTeam through TEAM_IMPACT. Review the provisional seed wording before activation.

| Category code (retain) | New list / Power Fx source |
|---|---|
| `IND_INNOVATION` | `MDAward` |
| `IND_CUSTOMER` | `TrendMarcherAward` |
| `IND_EXCELLENCE` | `BestInnovatorIndividual` |
| `TEAM_COLLAB` | `MDAwardTeam` |
| `TEAM_IMPACT` | `BestInnovatorTeam` |
| `TEAM_TRANSFORM` | `SpecialTeamAward` |

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
