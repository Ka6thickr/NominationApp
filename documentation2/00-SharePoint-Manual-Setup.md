# 00 — Manually create SharePoint lists and columns

## 1. Create the eight lists

Open https://5v7nf4.sharepoint.com/sites/AISite/ → Settings → Site contents → New → List → Blank list. Enter each exact list name below. Create AwardCategories first, AwardQuestions second, then the six nomination lists. If a configuration list already exists, verify its schema instead of creating a duplicate. Do not delete or rename the previous nomination lists for this fresh setup.

| Category code (retain) | New list / Power Fx source |
|---|---|
| `IND_INNOVATION` | `MDAward` |
| `IND_CUSTOMER` | `TrendMarcherAward` |
| `IND_EXCELLENCE` | `BestInnovatorIndividual` |
| `TEAM_COLLAB` | `MDAwardTeam` |
| `TEAM_IMPACT` | `BestInnovatorTeam` |
| `TEAM_TRANSFORM` | `SpecialTeamAward` |

Also create/verify `AwardCategories` and `AwardQuestions`.

For each list, Settings → List settings → Columns → Create column. Enter the exact internal name shown in the tables on initial creation, with no spaces. Keep that display name too so the supplied formulas match. If an incorrect internal name was created, a display-name rename will not fix it; inspect the Field parameter in its column-settings URL before proceeding.

`Title` already exists: edit it instead of creating another Title column. ID, Created, Modified, Created By and Modified By are built in; do not recreate them. Attachments is the built-in list attachment feature, not a custom column.

## 2. Column type settings

- Text: Single line of text, maximum 255 characters, default blank unless listed.
- Note: Multiple lines of text, Plain text, append changes No; do not use rich text. Keep list validation empty. The app applies its answer length rules.
- Number: Number with zero decimal places; leave default blank unless listed.
- Choice: single-select Drop-down menu, exact choices below, fill-in choices No. Explicitly clear any automatically selected default except NominationStatus = Draft.
- Boolean: Yes/No; set the table's default.
- Lookup: Lookup to AwardCategories, display Title, single value, no additional lookup fields, no enforced relationship deletion behavior.
- User: Person or Group, People Only, allow multiple selections No. UserMulti: same with multiple selections Yes.
- DateTime: Date and Time, include time, no default.
- Required, unique and indexed settings must match the table. Unique columns automatically require an index. For other indexed columns use List settings → Indexed columns → Create a new index.

Do not add mandatory validation to nomination columns: incomplete drafts must save. The app enforces required questions at submission.

## 3. Exact schema for every list

### AwardCategories

| Internal / display name | Type | Required | Default / choices | Indexed | Unique |
|---|---|---|---|---|---|
| `Title` | Text | Yes | Blank | No | No |
| `CategoryCode` | Text | Yes | Blank | Yes | Yes |
| `AwardType` | Choice | Yes | Individual, Team | No | No |
| `Description` | Note | No | Blank | No | No |
| `DisplayOrder` | Number | Yes | Blank | No | No |
| `IsActive` | Boolean | No | Default: No | No | No |
| `PublishedQuestionVersion` | Number | No | Blank | No | No |

### AwardQuestions

| Internal / display name | Type | Required | Default / choices | Indexed | Unique |
|---|---|---|---|---|---|
| `Title` | Text | Yes | Blank | No | No |
| `Category` | Lookup | Yes | Blank | Yes | No |
| `QuestionSetVersion` | Number | Yes | Blank | Yes | No |
| `QuestionKey` | Choice | Yes | Q1, Q2, Q3, Q4, Q5, Q6 | No | No |
| `QuestionText` | Note | Yes | Blank | No | No |
| `GuidanceText` | Note | No | Blank | No | No |
| `DisplayOrder` | Number | Yes | Blank | No | No |
| `IsRequired` | Boolean | No | Default: Yes | No | No |
| `ConfigurationKey` | Text | Yes | Blank | Yes | Yes |

### MDAward

| Internal / display name | Type | Required | Default / choices | Indexed | Unique |
|---|---|---|---|---|---|
| `Title` | Text | No | Blank | No | No |
| `Category` | Lookup | No | Blank | No | No |
| `QuestionSetVersion` | Number | No | Blank | No | No |
| `QuestionCount` | Number | No | Blank | No | No |
| `NominatedBy` | User | No | Blank | No | No |
| `NominatorEmail` | Text | No | Blank | Yes | No |
| `EmployeeRole` | Text | No | Blank | No | No |
| `EmployeeLevel` | Choice | No | L1, L2, L3, L4, L5, L6 | No | No |
| `NominationStatus` | Choice | No | Draft, Submitted; Default: Draft | Yes | No |
| `DeclarationAccepted` | Boolean | No | Default: No | No | No |
| `SubmittedOn` | DateTime | No | Blank | No | No |
| `Q1PromptSnapshot` | Note | No | Blank | No | No |
| `Q1RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q1Response` | Note | No | Blank | No | No |
| `Q2PromptSnapshot` | Note | No | Blank | No | No |
| `Q2RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q2Response` | Note | No | Blank | No | No |
| `Q3PromptSnapshot` | Note | No | Blank | No | No |
| `Q3RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q3Response` | Note | No | Blank | No | No |
| `Q4PromptSnapshot` | Note | No | Blank | No | No |
| `Q4RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q4Response` | Note | No | Blank | No | No |
| `Q5PromptSnapshot` | Note | No | Blank | No | No |
| `Q5RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q5Response` | Note | No | Blank | No | No |
| `Q6PromptSnapshot` | Note | No | Blank | No | No |
| `Q6RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q6Response` | Note | No | Blank | No | No |
| `NominatedEmployee` | User | No | Blank | No | No |

### TrendMarcherAward

| Internal / display name | Type | Required | Default / choices | Indexed | Unique |
|---|---|---|---|---|---|
| `Title` | Text | No | Blank | No | No |
| `Category` | Lookup | No | Blank | No | No |
| `QuestionSetVersion` | Number | No | Blank | No | No |
| `QuestionCount` | Number | No | Blank | No | No |
| `NominatedBy` | User | No | Blank | No | No |
| `NominatorEmail` | Text | No | Blank | Yes | No |
| `EmployeeRole` | Text | No | Blank | No | No |
| `EmployeeLevel` | Choice | No | L1, L2, L3, L4, L5, L6 | No | No |
| `NominationStatus` | Choice | No | Draft, Submitted; Default: Draft | Yes | No |
| `DeclarationAccepted` | Boolean | No | Default: No | No | No |
| `SubmittedOn` | DateTime | No | Blank | No | No |
| `Q1PromptSnapshot` | Note | No | Blank | No | No |
| `Q1RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q1Response` | Note | No | Blank | No | No |
| `Q2PromptSnapshot` | Note | No | Blank | No | No |
| `Q2RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q2Response` | Note | No | Blank | No | No |
| `Q3PromptSnapshot` | Note | No | Blank | No | No |
| `Q3RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q3Response` | Note | No | Blank | No | No |
| `Q4PromptSnapshot` | Note | No | Blank | No | No |
| `Q4RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q4Response` | Note | No | Blank | No | No |
| `Q5PromptSnapshot` | Note | No | Blank | No | No |
| `Q5RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q5Response` | Note | No | Blank | No | No |
| `Q6PromptSnapshot` | Note | No | Blank | No | No |
| `Q6RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q6Response` | Note | No | Blank | No | No |
| `NominatedEmployee` | User | No | Blank | No | No |

### BestInnovatorIndividual

| Internal / display name | Type | Required | Default / choices | Indexed | Unique |
|---|---|---|---|---|---|
| `Title` | Text | No | Blank | No | No |
| `Category` | Lookup | No | Blank | No | No |
| `QuestionSetVersion` | Number | No | Blank | No | No |
| `QuestionCount` | Number | No | Blank | No | No |
| `NominatedBy` | User | No | Blank | No | No |
| `NominatorEmail` | Text | No | Blank | Yes | No |
| `EmployeeRole` | Text | No | Blank | No | No |
| `EmployeeLevel` | Choice | No | L1, L2, L3, L4, L5, L6 | No | No |
| `NominationStatus` | Choice | No | Draft, Submitted; Default: Draft | Yes | No |
| `DeclarationAccepted` | Boolean | No | Default: No | No | No |
| `SubmittedOn` | DateTime | No | Blank | No | No |
| `Q1PromptSnapshot` | Note | No | Blank | No | No |
| `Q1RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q1Response` | Note | No | Blank | No | No |
| `Q2PromptSnapshot` | Note | No | Blank | No | No |
| `Q2RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q2Response` | Note | No | Blank | No | No |
| `Q3PromptSnapshot` | Note | No | Blank | No | No |
| `Q3RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q3Response` | Note | No | Blank | No | No |
| `Q4PromptSnapshot` | Note | No | Blank | No | No |
| `Q4RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q4Response` | Note | No | Blank | No | No |
| `Q5PromptSnapshot` | Note | No | Blank | No | No |
| `Q5RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q5Response` | Note | No | Blank | No | No |
| `Q6PromptSnapshot` | Note | No | Blank | No | No |
| `Q6RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q6Response` | Note | No | Blank | No | No |
| `NominatedEmployee` | User | No | Blank | No | No |

### MDAwardTeam

| Internal / display name | Type | Required | Default / choices | Indexed | Unique |
|---|---|---|---|---|---|
| `Title` | Text | No | Blank | No | No |
| `Category` | Lookup | No | Blank | No | No |
| `QuestionSetVersion` | Number | No | Blank | No | No |
| `QuestionCount` | Number | No | Blank | No | No |
| `NominatedBy` | User | No | Blank | No | No |
| `NominatorEmail` | Text | No | Blank | Yes | No |
| `EmployeeRole` | Text | No | Blank | No | No |
| `EmployeeLevel` | Choice | No | L1, L2, L3, L4, L5, L6 | No | No |
| `NominationStatus` | Choice | No | Draft, Submitted; Default: Draft | Yes | No |
| `DeclarationAccepted` | Boolean | No | Default: No | No | No |
| `SubmittedOn` | DateTime | No | Blank | No | No |
| `Q1PromptSnapshot` | Note | No | Blank | No | No |
| `Q1RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q1Response` | Note | No | Blank | No | No |
| `Q2PromptSnapshot` | Note | No | Blank | No | No |
| `Q2RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q2Response` | Note | No | Blank | No | No |
| `Q3PromptSnapshot` | Note | No | Blank | No | No |
| `Q3RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q3Response` | Note | No | Blank | No | No |
| `Q4PromptSnapshot` | Note | No | Blank | No | No |
| `Q4RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q4Response` | Note | No | Blank | No | No |
| `Q5PromptSnapshot` | Note | No | Blank | No | No |
| `Q5RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q5Response` | Note | No | Blank | No | No |
| `Q6PromptSnapshot` | Note | No | Blank | No | No |
| `Q6RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q6Response` | Note | No | Blank | No | No |
| `TeamName` | Text | No | Blank | No | No |
| `TeamPrimaryContact` | User | No | Blank | No | No |
| `TeamMembers` | UserMulti | No | Blank | No | No |

### BestInnovatorTeam

| Internal / display name | Type | Required | Default / choices | Indexed | Unique |
|---|---|---|---|---|---|
| `Title` | Text | No | Blank | No | No |
| `Category` | Lookup | No | Blank | No | No |
| `QuestionSetVersion` | Number | No | Blank | No | No |
| `QuestionCount` | Number | No | Blank | No | No |
| `NominatedBy` | User | No | Blank | No | No |
| `NominatorEmail` | Text | No | Blank | Yes | No |
| `EmployeeRole` | Text | No | Blank | No | No |
| `EmployeeLevel` | Choice | No | L1, L2, L3, L4, L5, L6 | No | No |
| `NominationStatus` | Choice | No | Draft, Submitted; Default: Draft | Yes | No |
| `DeclarationAccepted` | Boolean | No | Default: No | No | No |
| `SubmittedOn` | DateTime | No | Blank | No | No |
| `Q1PromptSnapshot` | Note | No | Blank | No | No |
| `Q1RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q1Response` | Note | No | Blank | No | No |
| `Q2PromptSnapshot` | Note | No | Blank | No | No |
| `Q2RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q2Response` | Note | No | Blank | No | No |
| `Q3PromptSnapshot` | Note | No | Blank | No | No |
| `Q3RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q3Response` | Note | No | Blank | No | No |
| `Q4PromptSnapshot` | Note | No | Blank | No | No |
| `Q4RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q4Response` | Note | No | Blank | No | No |
| `Q5PromptSnapshot` | Note | No | Blank | No | No |
| `Q5RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q5Response` | Note | No | Blank | No | No |
| `Q6PromptSnapshot` | Note | No | Blank | No | No |
| `Q6RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q6Response` | Note | No | Blank | No | No |
| `TeamName` | Text | No | Blank | No | No |
| `TeamPrimaryContact` | User | No | Blank | No | No |
| `TeamMembers` | UserMulti | No | Blank | No | No |

### SpecialTeamAward

| Internal / display name | Type | Required | Default / choices | Indexed | Unique |
|---|---|---|---|---|---|
| `Title` | Text | No | Blank | No | No |
| `Category` | Lookup | No | Blank | No | No |
| `QuestionSetVersion` | Number | No | Blank | No | No |
| `QuestionCount` | Number | No | Blank | No | No |
| `NominatedBy` | User | No | Blank | No | No |
| `NominatorEmail` | Text | No | Blank | Yes | No |
| `EmployeeRole` | Text | No | Blank | No | No |
| `EmployeeLevel` | Choice | No | L1, L2, L3, L4, L5, L6 | No | No |
| `NominationStatus` | Choice | No | Draft, Submitted; Default: Draft | Yes | No |
| `DeclarationAccepted` | Boolean | No | Default: No | No | No |
| `SubmittedOn` | DateTime | No | Blank | No | No |
| `Q1PromptSnapshot` | Note | No | Blank | No | No |
| `Q1RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q1Response` | Note | No | Blank | No | No |
| `Q2PromptSnapshot` | Note | No | Blank | No | No |
| `Q2RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q2Response` | Note | No | Blank | No | No |
| `Q3PromptSnapshot` | Note | No | Blank | No | No |
| `Q3RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q3Response` | Note | No | Blank | No | No |
| `Q4PromptSnapshot` | Note | No | Blank | No | No |
| `Q4RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q4Response` | Note | No | Blank | No | No |
| `Q5PromptSnapshot` | Note | No | Blank | No | No |
| `Q5RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q5Response` | Note | No | Blank | No | No |
| `Q6PromptSnapshot` | Note | No | Blank | No | No |
| `Q6RequiredSnapshot` | Boolean | No | Default: No | No | No |
| `Q6Response` | Note | No | Blank | No | No |
| `TeamName` | Text | No | Blank | No | No |
| `TeamPrimaryContact` | User | No | Blank | No | No |
| `TeamMembers` | UserMulti | No | Blank | No | No |

## 4. List-level settings

1. All eight lists: List settings → Versioning settings → create a version each time an item is edited = Yes. Content approval = No for this design.
2. Six nomination lists: Advanced settings → Attachments = Enabled; read access = Read items that were created by the user; create/edit access = Create items and edit items that were created by the user. These settings do not restrict site owners and do not make Submitted records immutable. If server-enforced submission locking is required, implement and test an approved backend permission workflow before production.
3. Six nomination lists: add an index for Modified, in addition to NominatorEmail and NominationStatus specified above. ID already has a built-in index.
4. Configuration lists: grant normal app users Read and configuration administrators the necessary edit permissions. Test with ordinary accounts. Hiding an admin screen is not security. Configure the administrator identity in App.OnStart; its all-zero placeholder intentionally grants nobody admin UI access.
5. Leave extra custom validation and required fields off. Do not add the future question tags.
6. Verify 194 custom columns total: AwardCategories 6, AwardQuestions 8, each individual list 29, each team list 31. These counts exclude built-in Title. Tables include Title for its required setting.

## 5. Configure dynamic categories and questions manually

1. In AwardCategories create six rows using the CategoryCode/list mapping above; set AwardType to Individual or Team as appropriate. Set Title and Description to approved business-facing content, DisplayOrder to 1–6, IsActive = No, PublishedQuestionVersion blank. List names are storage identifiers, not approved category copy.
2. The optional `provisioning/seed-data.json` contains the prior prototype's provisional category and question content. Review it before using it with the newly named awards. Do not assume old innovation/customer/excellence wording matches the new business awards.
3. In AwardQuestions create 3–6 rows per category for version 1. Category selects the matching AwardCategories item, QuestionSetVersion = 1, QuestionKey = Q1 through Qn, DisplayOrder = 1 through n, Title = approved criterion heading, QuestionText = full approved question, GuidanceText = optional guidance, IsRequired = approved Yes/No. No synthetic people or nomination rows are needed.
4. Set ConfigurationKey exactly to `<CategoryCode>-V1-Q<slot>`, for example `IND_INNOVATION-V1-Q1`. For version 2 use `IND_INNOVATION-V2-Q1`. Every key must be unique. This format matches the administration formulas.
5. Read back every row. Confirm correct lookup, one row per slot, contiguous Q1–Qn, nonempty title and question, and the same version number. After content approval set that category's PublishedQuestionVersion = 1 and IsActive = Yes. Until this step category selection is intentionally empty.
6. Later changes use a new complete version; retain old rows. Update PublishedQuestionVersion only after verifying the new set. Saved nominations retain their original question snapshots.

## 6. Connect the new Canvas app

Create the solution and app using `manual-build/README.md`. Add SharePoint connection for this site and all eight exact lists. Verify their Data pane identifiers match the names in this package. Add Office365Users. Create every referenced screen and form before setting shared formulas. Use the existing screen/control identifiers even where they contain the previous category terminology.

For deployment across environments, create Data Source environment variables for the SharePoint site and each list within the solution, then use the Advanced connection selection to bind those variables. Validate each target list's column types/internal names before switching. A new list title alone does not migrate existing records or attachments.

## Sources

- [Microsoft: create list columns](https://support.microsoft.com/en-us/sharepoint/lists/data-and-lists/create-a-column-in-a-list-or-library)
- [Microsoft: column types and options](https://support.microsoft.com/en-us/sharepoint/lists/data-and-lists/list-and-library-column-types-and-options)
- [Microsoft: Canvas data-source environment variables](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables-data-source-canvas-apps)
