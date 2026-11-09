# Prod — reusable components and screen build guides

Updated 10 November 2026. Build the shared components once, then follow one screen guide at a time. Each screen has its own Tree view, parent/control types, property tables and linked `.fx` files. The two existing forms are retained.

## Start here

1. [Set up the #E20074 global theme](production-guide/02-Theme.md), then [build reusable header, navigation and stepper](production-guide/00-Reusable-Components.md). This includes migration steps for your half-built first screen.
2. [Finish scrBestInnovatorIndividual](production-guide/scrBestInnovatorIndividual.md).
3. [Finish scrMDAward](production-guide/scrMDAward.md).
4. Build the remaining screens from the table below.

## Screen guides

| Screen | Guide | Main work |
|---|---|---|
| `scrBestInnovatorIndividual` | [Open guide](production-guide/scrBestInnovatorIndividual.md) | Keep existing form; finish shell/actions |
| `scrMDAward` | [Open guide](production-guide/scrMDAward.md) | Keep existing form; finish shell/actions |
| `scrTrendMarcherAward` | [Open guide](production-guide/scrTrendMarcherAward.md) | Build controls, properties and behavior |
| `scrBestInnovatorTeam` | [Open guide](production-guide/scrBestInnovatorTeam.md) | Build controls, properties and behavior |
| `scrMDAwardTeam` | [Open guide](production-guide/scrMDAwardTeam.md) | Build controls, properties and behavior |
| `scrSpecialTeamAward` | [Open guide](production-guide/scrSpecialTeamAward.md) | Build controls, properties and behavior |
| `scrHome` | [Open guide](production-guide/scrHome.md) | Build controls, properties and behavior |
| `scrNomineeDetails` | [Open guide](production-guide/scrNomineeDetails.md) | Build controls, properties and behavior |
| `scrCategorySelection` | [Open guide](production-guide/scrCategorySelection.md) | Build controls, properties and behavior |
| `scrReview` | [Open guide](production-guide/scrReview.md) | Build controls, properties and behavior |
| `scrConfirmation` | [Open guide](production-guide/scrConfirmation.md) | Build controls, properties and behavior |
| `scrMyNominations` | [Open guide](production-guide/scrMyNominations.md) | Build controls, properties and behavior |
| `scrQuestionAdministration` | [Open guide](production-guide/scrQuestionAdministration.md) | Build controls, properties and behavior |

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
| IND_INNOVATION | BestInnovatorIndividual | scrBestInnovatorIndividual | frmBestInnovatorIndividual |
| IND_CUSTOMER | MDAward | scrMDAward | frmMDAward |
| IND_EXCELLENCE | TrendMarcherAward | scrTrendMarcherAward | frmTrendMarcherAward |
| TEAM_COLLAB | BestInnovatorTeam | scrBestInnovatorTeam | frmBestInnovatorTeam |
| TEAM_IMPACT | MDAwardTeam | scrMDAwardTeam | frmMDAwardTeam |
| TEAM_TRANSFORM | SpecialTeamAward | scrSpecialTeamAward | frmSpecialTeamAward |

AwardCategories and AwardQuestions retain their names. Keep all fixed columns and Q1–Q6 slots. Team categories have three configured active question rows; unused slots stay hidden. Questions, categories and snapshots remain data-driven. Keep native attachments inside the matching form and the final status update inside form OnSuccess.

## Reference and validation

- [Full field/formula reference and earlier audit](production-guide/Reference.md). Its old copied-header layout is superseded by the component/screen guides above.
- [Stepper implementation](production-guide/01-Stepper.md).
- `.fx` files are formulas for properties, not importable applications. Copy the entire file into the named property.
- Source checks do not prove Studio compilation, rendering, permissions or runtime success. Finish the acceptance checklist in the reference before publication.

**Rebuild documentation:** run `tools/Build-ReusableGuides.py`. Do not run the older guide generators alone; they recreate the superseded single-file guide.
