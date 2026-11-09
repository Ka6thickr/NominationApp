# Team and Individual Nomination App

Power Apps Canvas app backed by SharePoint, with dynamic award categories and questions, six typed nomination forms, draft saving, evidence attachments and a four-stage process stepper. Contoso branding is retained.

## Current state

As of 3 November 2026, the SharePoint provisioning and manual implementation guides are complete. The live Canvas app is **partially implemented and unpublished**. Three scaffold screens and an Innovation form were verified; Studio stalled during subsequent form editing. End-to-end draft and submission tests have not run.

This repository contains the source design, provisioning scripts, Power Fx recipes and handover documentation. It does **not** contain an exported `.msapp` or deployable solution package. Publishing this repository does not publish the live Power App.

## Start here

**Continue your manual build:** [stepstocomplete.md](stepstocomplete.md) starts after the confirmed II/IC form corrections and walks through scrolling containers, all screen layouts, shared state and end-to-end testing, with the full formula reference included.

**Current environment:** [Prod.md — reviewed screen exports, latest mapping and full build guide](Prod.md). This supersedes documentation2's order-based list mapping and uses the destination screen/form names supplied on 9 November 2026.

**New manual rebuild:** [documentation2 — complete setup with the six updated list names](documentation2/README.md). Use this package for MDAward, TrendMarcherAward, BestInnovatorIndividual, MDAwardTeam, BestInnovatorTeam and SpecialTeamAward. The original documentation below is retained as a historical reference.

- [Implementation status and exact manual resume steps](documentation/Implementation-Status.md)
- [Full GitHub Copilot app guide](documentation/GitHub-Copilot-App-Guide.md)
- [Manual screen and formula guide](documentation/manual-build/README.md)
- [Offline manual package](documentation/NominationApp-Manual-Build.zip)
- [Screen plan](documentation/PowerApps-Screen-Plan.md)
- [Dynamic SVG / HTML process stepper](documentation/Process-Stepper-Component.md)
- [SharePoint provisioning instructions](provisioning/README.md)
- [Original specification](Exsistingfiles/Employee_Team_Awards_Canvas_App_Codex_Spec.md)

## Configuration and portability

Edit physical list names and site URL in `provisioning/environment.json`; preserve the agreed columns and logical category keys. Canvas data sources require explicit binding to the destination lists; list names cannot be dynamically resolved from text in Power Fx. Solution environment-variable rebinding remains pending.

Questions and categories are data-driven. Seed categories remain inactive pending content approval. Future question tags are deferred without schema changes. Keep credentials out of repository files; provisioning uses interactive authentication.

## Validation

Run `python tools/Test-ManualGuide.py` for structural guide validation and `pwsh -File provisioning/Test-Provisioning.ps1` for local provisioning/schema tests. These checks do not compile Power Fx or validate Canvas runtime behavior. Complete the [acceptance checklist](documentation/manual-build/04-Validation-and-Handover.md) before publishing the app.

The HTML prototype and reference screenshots are under `Exsistingfiles/`. The prototype is a design reference, not the deployed Canvas app.
