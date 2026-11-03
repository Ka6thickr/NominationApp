# Nomination SharePoint setup

Target: AISite. Branding remains Contoso. Question tags are deferred and no tag columns are provisioned.

## Configuration

- `environment.json` is the single editable source for the site URL and all eight physical list names. Keep the logical keys/category codes unchanged across environments.
- `seed-data.json` contains six categories and 21 questions copied from the supplied HTML prototype. No sample people or nomination records are uploaded. The criterion heading becomes `Title`; the existing explanatory prompt becomes `QuestionText`; `GuidanceText` is initially empty and can be configured later.
- Category titles, descriptions, ordering, active status, published question version, question wording, guidance, and required flags are SharePoint data, not hardcoded Power Fx content.
- L1-L6 and category/question wording remain provisional. Categories stay inactive with no published version by default. Changing the approval flags is a business decision, not a prerequisite for creating the lists.
- Do not put passwords, application secrets, or access tokens in any of these files. Pass the existing approved application Client ID as a parameter for interactive authentication.

## Local checks

```powershell
pwsh -NoProfile -File ./provisioning/Provision-NominationLists.ps1 -ValidateOnly
pwsh -NoProfile -File ./provisioning/Test-Provisioning.ps1
```

## Provisioning

From PowerShell 7.4 or later with PnP.PowerShell 3.x installed:

```powershell
./provisioning/Provision-NominationLists.ps1 -ClientId 'YOUR_ENTRA_APP_CLIENT_ID' -InspectOnly
./provisioning/Provision-NominationLists.ps1 -ClientId 'YOUR_ENTRA_APP_CLIENT_ID'
```

In an already authenticated PowerShell session targeting the configured site, use `-UseExistingConnection` instead of `-ClientId`. Connection validation checks the exact site before writes.

The script checks existing target list types and column types, choice values, lookup targets, and plain-text settings before provisioning. It creates missing resources, enables version history and native nomination attachments, applies required/unique/index settings, and verifies the resulting schema. It never deletes lists, columns, items, or files. It preserves extra existing columns, business-owned category records, and published questions. An incompatible schema or differing existing draft seed causes an explicit error instead of silently replacing data. A partial failure can be repaired and rerun.

On success, `deployment-result.json` records the verified list GUIDs and URLs. This is a generated record, not another editable list-name configuration.

After business approval, update the two approval flags in `environment.json`, then use `-PublishSeed`. Publication checks all version-one records before setting the category version pointer and activating it. Later question changes belong in a new version through the planned question administration interface; this bootstrap script does not edit published versions. A single publisher is assumed; the pointer recheck is not an atomic lock.

## Security and deployment work still required

The script sets own-item read/edit behavior on all six nomination lists. This does not override administrator/Manage Lists privileges or remove inherited delete rights. Configuration-manager and awards-administrator group assignments, ordinary-user delete restrictions, and direct-access tests require the approved security groups. Do not release the app to ordinary users until this is completed.

Submitted-item protection (app-only or optional permission flow) remains undecided. No permission-lock flow, notification email, approval, scoring, or winner selection is created.

For Canvas app environment moves, connect the eight typed data sources through solution data-source environment variables: one site URL and eight list GUID values. A text list name in `App.OnStart` cannot dynamically rebind a SharePoint form. Resolve target list GUIDs from the generated deployment report; retain identical column internal names and field types across environments. This does not change the SharePoint data backend to Dataverse.

Sources: [PnP interactive authentication](https://pnp.github.io/powershell/articles/authentication.html), [field XML](https://pnp.github.io/powershell/cmdlets/Add-PnPFieldFromXml.html), [list settings](https://pnp.github.io/powershell/cmdlets/Set-PnPList.html), [Canvas data-source environment variables](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables-data-source-canvas-apps).
