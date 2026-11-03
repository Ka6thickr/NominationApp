# Employee and Team Award Nominations
## Canvas Power Apps implementation specification for Codex

Document version: 1.0  
Target platform: Microsoft Power Apps Canvas app  
Backend: SharePoint Online  
Supporting automation: Power Automate, where explicitly required  
Document purpose: Business plan, technical design, implementation instructions, and acceptance criteria

---

## 1. Instructions to Codex

Use this document as the implementation specification, not merely as a request for a mockup.

Build the solution incrementally using the supported tools available in the user's environment. Preserve the six separate category-specific nomination lists. Do not replace them with one combined nominations list or a Dataverse backend without user approval.

Before creating or changing tenant resources:

1. Inspect the available project, authenticated connections, Power Platform tooling, and target environment.
2. Confirm the deployment inputs in section 4.
3. Identify existing lists, apps, and flows. Reuse compatible resources; never overwrite existing business data.
4. Explain which steps can be executed and which need an authorized Microsoft 365 or Power Platform administrator.
5. Ask for missing business decisions instead of inventing official award names, employee levels, or security policies.

Implementation rules:

- Use supported Power Platform and SharePoint tooling.
- Do not invent an importable Canvas app package, unsupported source format, or working tenant connection.
- If an existing supported Canvas source project is available, follow its format and tooling version.
- If tenant access or app-authoring capabilities are unavailable, deliver reproducible provisioning scripts, schema definitions, a screen/control specification, Power Fx formulas, flow instructions, and a manual setup guide. Clearly label these as not deployed or not runtime-tested.
- Never claim that a text specification or a UI mockup is a working Power App.
- Do not store credentials, access tokens, or real employee data in source files.
- Use synthetic sample data only.
- Validate the exact behavior in this document and record any unmet requirements.
- Do not introduce approvals, scoring, leaderboards, or winner selection.

Expected deliverables:

1. SharePoint provisioning assets for all eight lists.
2. Initial category and question configuration data.
3. Canvas app implementation, if supported authenticated authoring is available; otherwise complete build instructions and formulas.
4. Question administration implementation.
5. Optional submitted-record permission flow, only after the security decision is confirmed.
6. Deployment and connection instructions.
7. Test cases and execution results.
8. A clear list of manual steps, limitations, and outstanding decisions.

---

## 2. Business problem and intended outcome

Employees need a consistent, accessible way to nominate colleagues and teams for recognition. Each award category has different criteria, and business administrators need to manage those questions without repeatedly redesigning the app.

The solution must:

- Support three Individual award categories and three Team award categories.
- Store nominations for each category in its own SharePoint list.
- Display three to six category-specific questions.
- Capture a written response for each required question.
- Store supporting files at nomination level.
- Allow incomplete drafts, resume, review, and final submission.
- Preserve the questions originally presented to each nominee's nominator.
- Restrict ordinary users to their own nominations.
- Work on desktop, tablet, and mobile.

The initial release is a nomination capture solution, not an awards adjudication system.

---

## 3. Confirmed design and assumptions

### 3.1 Confirmed design

| Requirement | Decision |
|---|---|
| Application | Responsive Canvas Power App |
| Data platform | SharePoint Online |
| Award types | Individual and Team |
| Award categories | Six total: three per type |
| Nomination storage | One separate list per category |
| Question management | Business-managed Award Questions configuration list |
| Question count | Three to six per category |
| Evidence | Nomination-level SharePoint attachments |
| Responses | Columns on the category's nomination item |
| Statuses | Draft and Submitted |
| History | Versioned question sets and nomination snapshots |

### 3.2 Proposed defaults requiring confirmation

- The category names in this document are placeholders.
- Employee levels L1-L6 are placeholders.
- All seeded questions are required.
- Responses have a 2,000-character application limit.
- Nominated By is the signed-in user and cannot be changed in the app.
- Role and level for Team nominations describe the team's primary contact.
- Existing drafts retain their original question version.
- A saved draft cannot move to another category.
- Email notifications are excluded unless separately approved.
- No self-nomination or repeat-nomination restriction is imposed until the business defines one.
- Submitted-record backend enforcement requires the security decision in section 13.

---

## 4. Deployment inputs and decisions

Collect these before production deployment:

| Input | Needed for |
|---|---|
| SharePoint site URL | List provisioning and connections |
| Power Platform environment | Canvas app and flow deployment |
| App name and publisher/solution conventions | Consistent deployment |
| Six official category names and stable codes | Data and app mapping |
| Approved questions and guidance | Initial configuration |
| Employee level values | Dropdown choices |
| Nominator audience/security group | App sharing and permissions |
| Configuration manager group | Question administration |
| Awards administrator group | All-nomination access |
| Approved employee directory connector | Employee search |
| Attachment types and size policy | Evidence validation |
| Retention policy | Records and file retention |
| Expected annual volume | Index and unique-permission planning |
| Submitted-item protection requirement | App-only versus backend enforcement |
| Accessibility and branding standards | UI acceptance |
| Dev/test/production deployment requirements | Environment separation |

Do not silently substitute a personal site, production tenant, or a connection owned by an arbitrary user.

---

## 5. Business process

### 5.1 New nomination

1. User opens the application.
2. User chooses Individual or Team.
3. App displays the three active categories for that type.
4. User selects a category.
5. App loads and validates the category's published question set.
6. App initializes nomination data and question snapshots.
7. User enters nominee details, responses, and optional files.
8. User saves an incomplete draft or continues to review.
9. App validates all required details and responses before final submission.
10. User accepts the accuracy declaration.
11. App saves the form and attachments as Draft.
12. App changes the saved item to Submitted only after the form save succeeds.
13. App shows the reference and confirmation only after submission succeeds.

### 5.2 Resume draft

1. User opens My Nominations.
2. User selects award type and category.
3. App retrieves the user's matching items using delegable filters.
4. User opens a Draft.
5. App uses saved prompt snapshots, required flags, and answers.
6. User edits and saves or submits the same item.

### 5.3 Question publication

1. Authorized business administrator selects a category.
2. Administrator copies a question version into a new version.
3. Administrator edits three to six questions.
4. Administrator previews the question set.
5. App validates the full set.
6. App saves and verifies all question records.
7. App updates the category's published version pointer last.
8. New nominations use the new version.
9. Existing drafts and submissions remain unchanged.

---

## 6. Solution architecture

```text
Canvas Power App
|
+-- AwardCategories
|       |
|       +-- AwardQuestions
|
+-- Nom_IndividualInnovation
+-- Nom_IndividualCustomer
+-- Nom_IndividualExcellence
+-- Nom_TeamCollaboration
+-- Nom_TeamImpact
+-- Nom_TeamTransformation
        |
        +-- Native SharePoint item attachments

Optional: Power Automate flow for submitted-item permission enforcement
```

There are eight lists. No separate response list or evidence library is required for this design.

Each nomination belongs to exactly one category-specific list. Each item contains its own details, question snapshots, answers, and attachments.

---

## 7. SharePoint backend specification

### 7.1 General provisioning rules

- Use stable internal column names without spaces.
- Create internal names first; set friendly display names afterward where needed.
- Provision compatible existing resources idempotently; report incompatible schemas.
- Enable list version history.
- Enable attachments on nomination lists.
- Use plain-text multiline fields for prompts and responses.
- Disable append-only behavior for multiline fields.
- Keep nomination-entry fields optional at SharePoint level where incomplete drafts require it.
- Enforce required submission fields in the app; do not describe this as server-side validation.
- Create appropriate indexes before production volumes grow.
- Avoid unnecessary lookup/person expansion in high-volume queries.
- Do not remove columns or items during a provisioning rerun.

### 7.2 AwardCategories

Purpose: One row per award category and its currently published question version.

| Internal name | Type | Constraints / behavior |
|---|---|---|
| ID | Built-in ID | Automatic |
| Title | Single line of text | Required; category display name |
| CategoryCode | Single line of text | Required; unique; stable |
| AwardType | Choice | Required; Individual or Team |
| Description | Multiple lines, plain text | Optional |
| DisplayOrder | Number | Required; integer |
| IsActive | Yes/No | New nominations only when active |
| PublishedQuestionVersion | Number | Positive integer for an active category |

Built-in Created, Modified, Created By, and Modified By support auditing.

Category-to-list mapping:

| CategoryCode | Placeholder title | Type | Nomination list |
|---|---|---|---|
| IND_INNOVATION | Innovation Champion | Individual | Nom_IndividualInnovation |
| IND_CUSTOMER | Customer Impact | Individual | Nom_IndividualCustomer |
| IND_EXCELLENCE | Excellence in Execution | Individual | Nom_IndividualExcellence |
| TEAM_COLLAB | Collaboration Excellence | Team | Nom_TeamCollaboration |
| TEAM_IMPACT | Business Impact | Team | Nom_TeamImpact |
| TEAM_TRANSFORM | Transformation & Innovation | Team | Nom_TeamTransformation |

The mapping is implemented explicitly in the app. A list name stored as text is not a dynamic Canvas data source.

Changing the display name requires no mapping change. Adding a seventh category or changing its destination list requires application work.

### 7.3 AwardQuestions

Purpose: Store question definitions by category and version.

| Internal name | Type | Constraints / behavior |
|---|---|---|
| ID | Built-in ID | Automatic |
| Title | Single line of text | Required; short admin-friendly title |
| Category | Lookup to AwardCategories | Required; single value |
| QuestionSetVersion | Number | Required; positive integer |
| QuestionKey | Choice | Required; Q1, Q2, Q3, Q4, Q5, Q6 |
| QuestionText | Multiple lines, plain text | Required |
| GuidanceText | Multiple lines, plain text | Optional |
| DisplayOrder | Number | Required; integer |
| IsRequired | Yes/No | Submission validation flag |
| ConfigurationKey | Single line of text | Required; unique |

ConfigurationKey format:

```text
<CategoryCode>-V<QuestionSetVersion>-<QuestionKey>
Example: IND_INNOVATION-V1-Q1
```

Question set rules:

- Three to six records.
- Contiguous QuestionKey values starting at Q1.
- DisplayOrder matches the numeric question slot, 1 through QuestionCount.
- No duplicate keys or display orders.
- Nonblank question text.
- All records belong to the same category and version.
- Published versions are immutable through the app.
- Published versions and referenced historical versions must not be deleted.

The category's PublishedQuestionVersion determines the active set. Do not use independently editable per-question active flags to partially publish a version.

### 7.4 Common columns on all six nomination lists

| Internal name | Type | Behavior |
|---|---|---|
| ID | Built-in ID | Unique only within the list |
| Title | Single line of text | App-generated short title |
| Category | Lookup to AwardCategories | App sets correct category |
| QuestionSetVersion | Number | Captured at nomination initialization |
| QuestionCount | Number | Integer 3-6 |
| NominatedBy | Person, single | Signed-in nominator |
| NominatorEmail | Single line of text | Lowercase signed-in email |
| EmployeeRole | Single line of text | Individual role or team contact role |
| EmployeeLevel | Choice | Approved organizational levels |
| NominationStatus | Choice | Draft or Submitted; default Draft |
| DeclarationAccepted | Yes/No | Default No |
| SubmittedOn | Date and time | Blank for Draft |

Use built-in Created, Created By, Modified, Modified By, and Attachments.

Created By is the ownership source when using SharePoint's own-item permissions. NominatorEmail supports app filtering; it is not an authorization boundary.

### 7.5 Individual-only columns

Add these to all three Individual nomination lists:

| Internal name | Type | Behavior |
|---|---|---|
| NominatedEmployee | Person, single | Required at submission |

### 7.6 Team-only columns

Add these to all three Team nomination lists:

| Internal name | Type | Behavior |
|---|---|---|
| TeamName | Single line of text | Required at submission |
| TeamPrimaryContact | Person, single | Required at submission |
| TeamMembers | Person, multiple | Optional |

### 7.7 Question snapshot and response columns

Create these three columns for each slot N from 1 through 6 in every nomination list:

| Column pattern | Type | Behavior |
|---|---|---|
| QNPromptSnapshot | Multiple lines, plain text | Full question text and guidance originally displayed |
| QNRequiredSnapshot | Yes/No | Original required-answer flag |
| QNResponse | Multiple lines, plain text | Answer; application maximum 2,000 characters |

Actual first-slot names are Q1PromptSnapshot, Q1RequiredSnapshot, and Q1Response; repeat through Q6.

Snapshot format:

```text
<QuestionText>

Guidance: <GuidanceText>
```

Omit the Guidance line if guidance is empty.

Rules:

- Capture snapshots when the nomination is initialized, before the first save.
- Persist them with the first successful draft save.
- Do not refresh them from current configuration while editing an existing draft.
- Use them for review and read-only views.
- Slots above QuestionCount remain blank and hidden.
- Required flags for unused slots are No.
- Do not append answers or overwrite unrelated slots during save.

This design intentionally reserves all six slots so increasing a category from three questions to six does not require schema changes.

### 7.8 Indexing

Evaluate and create indexes for:

- AwardCategories.CategoryCode, including its unique constraint.
- AwardQuestions.ConfigurationKey, including its unique constraint.
- AwardQuestions.Category and QuestionSetVersion, based on the actual query.
- Nomination lists' NominatorEmail and NominationStatus.
- Created/Modified where used in supported sorted queries.

Validate actual SharePoint query behavior and delegation warnings. Indexes do not make a nondelegable Canvas formula delegable.

### 7.9 Attachments

- Use native attachments on each nomination item.
- Evidence belongs to the whole nomination.
- Support adding/removing files in Draft.
- Support opening/downloading files in Submitted view.
- Use the supported attachment control inside a SharePoint-bound form.
- Do not store binary content in text columns.
- Apply approved attachment count/size settings supported by the control.
- Confirm any required file-type enforcement separately; do not promise extension restrictions without an implemented validation mechanism.
- Test file behavior on target browsers and mobile clients.

---

## 8. Relationships and data integrity

| Parent | Child | Relationship |
|---|---|---|
| AwardCategories | AwardQuestions | One category to many question/version rows |
| AwardCategories | Each nomination list | One category to many nominations |
| Nomination item | Native attachments | One item to many files |

```text
AwardCategories.ID
   |
   +--< AwardQuestions.Category
   |       QuestionSetVersion + QuestionKey
   |
   +--< Nom_<Category>.Category
           QuestionSetVersion
           QuestionCount
           Q1-Q6 snapshots and answers
           |
           +--< Native item attachments
```

SharePoint lookups are not equivalent to full database transactions or composite foreign keys.

The app must enforce:

- Category matches the current destination list.
- Award type matches category.
- QuestionCount is 3-6.
- The selected question set is valid.
- One nomination uses one consistent set of snapshots.

Submitted answers remain understandable even if configuration later changes because snapshots are stored locally on the nomination.

---

## 9. Initial configuration data

Seed version 1 for each category using these placeholder titles. Business owners must approve full question wording and guidance before production.

| Category | Question titles |
|---|---|
| Innovation Champion | Originality; Implementation and ownership; Measurable impact |
| Customer Impact | Understanding customer needs; Service quality; Customer outcomes; Sustained commitment |
| Excellence in Execution | Quality and reliability; Ownership and accountability; Results delivered |
| Collaboration Excellence | Cross-functional collaboration; Inclusion and knowledge sharing; Collective outcomes |
| Business Impact | Business alignment; Measurable results; Resource efficiency; Sustainability |
| Transformation & Innovation | Novel approach; Adoption and change management; Measurable improvement; Scalability |

For each title, draft a complete question asking for specific actions and outcomes. Mark seeded questions required and provide concise guidance.

Seed all questions before setting PublishedQuestionVersion to 1 and activating the category.

---

## 10. Canvas app design

### 10.1 Visual and accessibility requirements

- Microsoft Fluent-style business interface.
- Segoe UI or the approved corporate font.
- Blue primary actions, white cards, light gray background.
- Responsive layout containers rather than fixed-position desktop-only layouts.
- Clearly labeled inputs, accessible names, keyboard navigation, and visible focus.
- Never communicate errors or state through color alone.
- Wrap long question labels and allow automatic height.
- Put each multiline response below its question.
- No horizontal scrolling at supported mobile widths.
- Test desktop, tablet, and approximately 390-pixel mobile width.

### 10.2 Screens

| Screen | Purpose |
|---|---|
| Home | Award type selection, instructions, My Nominations |
| Category Selection | Three category cards filtered by award type |
| Individual Innovation Form | Form bound to its dedicated list |
| Individual Customer Form | Form bound to its dedicated list |
| Individual Excellence Form | Form bound to its dedicated list |
| Team Collaboration Form | Form bound to its dedicated list |
| Team Impact Form | Form bound to its dedicated list |
| Team Transformation Form | Form bound to its dedicated list |
| Review | Read current nomination state, edit, declare, submit |
| Confirmation | Reference and submission result |
| My Nominations | Category-specific list of own records |
| Question Administration | Restricted question drafting, preview, publication |

Six separate SharePoint-bound edit forms are intentional. Reuse layouts/components, but do not attempt to turn a list name string into a dynamically typed form data source.

### 10.3 Home

- Heading: Employee & Team Award Nominations.
- Individual Award and Team Award selection cards.
- My Nominations button.
- Restricted administration navigation.

### 10.4 Category selection

- Read active categories for the selected type.
- Sort by DisplayOrder.
- Show title and description.
- Load only the selected category's published question set.
- Validate the complete set before proceeding.
- If missing or invalid, block creation and show an explicit administrator-contact message.
- A retired category is unavailable for new records but existing records remain viewable.
- Proposed behavior: allow existing drafts in a retired category to continue. Confirm any closure policy before adding deadline restrictions.

### 10.5 Category forms

Sections:

1. Nominator: signed-in name/email, read-only.
2. Nominee/team details.
3. Three to six question cards using snapshots and response inputs.
4. Nomination-level attachments.
5. Back, Save draft, Review actions.

Use required indicators based on saved snapshot flags.

Show character counters and enforce the agreed answer limit. Count trimmed content for empty-answer validation; do not accept whitespace-only answers.

Use Office 365 Users or the approved connector for employee search. Save person fields using supported SharePoint person-record structures, resolving selected directory users correctly. Test people picker behavior; do not assume a directory search result can be patched directly without transformation.

### 10.6 Review

- Review current unsaved edits as well as saved fields.
- Display nominee/team, category, snapshots, answers, and filenames.
- Provide Edit navigation without resetting the form.
- Show required accuracy declaration.
- Editing after review resets declaration acceptance and requires review again.
- Submit is disabled while saving or submitting.

### 10.7 Confirmation and references

Reference format:

```text
<CategoryCode>-<SharePoint item ID padded for display>
Example: IND_INNOVATION-000125
```

Never use item ID alone as a cross-category reference.

A derived display reference is sufficient. Add a stored reference column only if an approved downstream integration requires it.

### 10.8 My Nominations

- Select award type, category, and status.
- Use a known category-specific data source.
- Filter by current user and optional status using validated delegable formulas.
- Show reference, nominee/team, category, status, modified date, and action.
- Draft action: Continue editing.
- Submitted action: View.
- Opening an existing item must reload its current status before permitting edits.

Do not ClearCollect all six unbounded lists and claim complete results. A global cross-category summary requires a separately designed scalable query/index strategy.

### 10.9 Back, exit, and category changes

- Back to review/form preserves input.
- Warn before leaving unsaved changes.
- Before the first save, changing category warns and clears incompatible answers only after confirmation.
- After saving, the category is fixed.
- Starting another category creates a new nomination; it does not move the saved item or its attachments.

---

## 11. App state and implementation patterns

Suggested state names may be adapted to project conventions:

| State | Purpose |
|---|---|
| CurrentAwardType | Individual or Team |
| CurrentCategory | Selected category record |
| CurrentQuestionVersion | Captured version |
| CurrentQuestions | Small, bounded validated question collection |
| CurrentNominationId | Saved item ID, blank before first save |
| CurrentQuestionCount | Captured count |
| IsBusy | Prevent repeated actions |
| SaveIntent | Draft or Submit |
| ReviewModel | Current values for review |

Use explicit category routing with Switch or equivalent. Keep form-specific typed records attached to their own sources; normalize only the view/review model where useful.

Do not build six unnecessarily different implementations. Keep validation, naming, snapshots, and layout consistent.

### 11.1 Save event sequence

SubmitForm is asynchronous. Do not immediately patch Submitted status on the line after SubmitForm and assume the save finished.

Implement:

1. Set SaveIntent and busy state.
2. Submit the active category form as Draft.
3. In the form's OnSuccess, capture LastSubmit and its ID.
4. If SaveIntent is Draft, show saved confirmation and clear busy state.
5. If SaveIntent is Submit, update that exact saved item to Submitted with timestamp and declaration.
6. Handle the status update success/failure explicitly.
7. Use OnFailure for form/attachment save failures and retain input.

On subsequent saves, ensure the form is in Edit mode against the existing item. Do not create another New item on retry.

### 11.2 Error handling

- Use supported Power Fx error handling and form error information.
- Show understandable error messages; avoid exposing sensitive diagnostics.
- Retain unsaved responses when a save fails.
- Do not navigate to confirmation on failure.
- If form save succeeds but status update fails, say the nomination is saved as Draft and allow retry.
- Clear busy state on both successful and failed terminal paths.
- Do not silently substitute empty question sets or fake employee data.

### 11.3 Concurrency

- Refresh and check current status when opening and before submitting.
- Use supported conflict/error detection where available.
- Do not silently overwrite a detected conflict; ask the user to reload after warning about unsaved changes.
- Do not claim these client checks provide atomic locking or prevent all concurrent edits.
- Confirm whether simultaneous editing across browser sessions must be strictly blocked; that requires an additional concurrency design.

---

## 12. Question administration and versioning

### 12.1 Administrative functions

- Select a category.
- View current published questions.
- Create a new version by copying a prior version.
- Edit titles, text, guidance, and required flags.
- Add/remove slots within the 3-6 range.
- Preview the employee question layout.
- Validate and publish.

Category-to-list mapping and stable category codes are not editable by business users in the app.

### 12.2 Publication safeguards

1. Allocate a new version number.
2. Use unique ConfigurationKey values to detect duplicate slots.
3. Save all rows for that version.
4. Re-read and validate exact count, keys, ordering, and nonblank prompts.
5. Update PublishedQuestionVersion only after successful validation.
6. If any row fails, keep the old published pointer and show the failure.
7. Detect if another administrator changed the pointer while publication was being prepared.

SharePoint does not provide an atomic transaction across these records. For the initial release, coordinate a single active publisher per category and handle conflicts explicitly. If concurrent publishing is required, implement a supported serialized publication mechanism before claiming it is safe.

### 12.3 Immutable history

Published versions are not edited through the app.

Even a wording change is published as a new version. Existing drafts do not automatically migrate. Site owners retain administrative power, so governance and permissions must also restrict direct list editing.

---

## 13. Security and permissions

### 13.1 Roles

| Role | Configuration | Nominations |
|---|---|---|
| Nominator | Read | Create/read/edit own drafts; read own submitted records |
| Question Administrator | Manage approved configuration | No all-nomination access unless separately assigned |
| Awards Administrator | Read/manage as approved | Access all nominations |

App screen visibility is not security. Enforce SharePoint permissions independently.

### 13.2 Own-record access

- Configure own-item read/edit settings on each nomination list.
- Use least-privilege list permissions; avoid giving ordinary users Manage Lists.
- Verify inherited groups do not grant broader access.
- Use Created By as the own-item identity.
- If records are created through a service-account flow, own-item behavior changes; do not use that pattern without redesigning ownership permissions.
- Restrict ordinary users from deleting nominations unless the business explicitly permits it.
- Test direct SharePoint list and attachment access using separate accounts.

### 13.3 Submitted-item enforcement decision

Choose and document one:

**Option A: App-only read-only behavior**

- App blocks editing submitted records.
- Does not prevent direct SharePoint edits by users who still have permission.
- Suitable only if business explicitly accepts this limitation.

**Option B: Asynchronous SharePoint item permission enforcement**

- A controlled Power Automate flow detects Submitted items.
- Breaks item inheritance and applies an explicit approved permission set.
- Retains required administrator/service access.
- Grants nominator read-only access.
- Removes unintended editor assignments.
- Is idempotent and reports failures.
- Revalidates current status and ownership before applying changes.

Important limitations:

- Flow execution is delayed; this is not an immediate atomic lock.
- Unique item permissions require capacity and operational planning.
- Do not rely on copying broad inherited permissions and merely adding Read for the owner; inherited/copied Edit grants may still allow editing.
- Review attachment operations and direct API access in testing.
- Define how administrators remediate partially applied permission changes.

If strict immediate immutability or server-enforced submission validation is mandatory, stop and agree an enhanced backend design. The initial Canvas/SharePoint pattern does not guarantee those properties.

### 13.4 Administrative and connection security

- App sharing does not automatically grant data access.
- Grant access to lists and connectors separately as required.
- Use approved connection ownership and service accounts.
- Never use a broadly privileged flow to return arbitrary nominations based only on caller-supplied email or item ID.
- Keep configuration managers separate from awards reviewers unless explicitly approved.

---

## 14. Automation

The only planned optional automation is submitted-item permission enforcement.

If selected, document:

- Trigger and trigger conditions.
- Connection owner.
- Exact list scope, including all six lists.
- Permission role assignments.
- Idempotency and loop prevention.
- Retry and partial-failure handling.
- Administrator notification/monitoring channel.
- Expected lock delay.
- Scale and unique-permission limits validated for the target tenant.

Do not add approval, scoring, or email workflows without a scope change.

---

## 15. Validation rules

| Stage | Required checks |
|---|---|
| Category load | Active category, valid mapping, published version, valid 3-6 question set |
| Draft save | Valid field formats, response length, valid category/snapshots |
| Review | All required nominee fields and required responses |
| Submission | Review validation plus accepted declaration and current Draft status |
| Publish questions | Complete version, contiguous keys/order, unique records, nonblank text |

For Individual submission require NominatedEmployee, EmployeeRole, and EmployeeLevel.

For Team submission require TeamName, TeamPrimaryContact, EmployeeRole, and EmployeeLevel.

Evidence and TeamMembers are optional.

Do not add unapproved minimum answer lengths, scoring rules, or mandatory attachments.

---

## 16. Performance, operations, and deployment

- Use delegable filters and known data sources for nomination galleries.
- Only cache bounded configuration, such as a six-question set.
- Validate results above the app's nondelegation row limit.
- Review SharePoint threshold behavior and selected indexes with realistic volume.
- Use separate dev/test/production resources if required.
- Parameterize site URLs and approved environment-specific settings where supported.
- Keep stable category codes across environments.
- Do not embed production list IDs into otherwise portable assets without a mapping step.
- Version app releases and retain rollback instructions.
- Enable audit/version history and align retention with company policy.
- Do not delete production records during upgrades.

Provisioning assets must validate prerequisites and report authorization/schema errors rather than silently skipping resources.

---

## 17. Acceptance test matrix

| ID | Test | Expected result |
|---|---|---|
| AT01 | Select Individual | Exactly its three configured active categories appear |
| AT02 | Select Team | Exactly its three configured active categories appear |
| AT03 | Open each category | Correct version and 3-6 questions appear |
| AT04 | Use long question text | Wraps without clipping on desktop/mobile |
| AT05 | Save empty/incomplete draft | Draft saves without mandatory-answer errors |
| AT06 | Reopen draft | Same item, snapshots, answers, and files restored |
| AT07 | Submit missing nominee data | Clear errors; no Submitted status |
| AT08 | Submit whitespace-only mandatory answer | Rejected as empty |
| AT09 | Enter 2,000 characters | Accepted |
| AT10 | Attempt more than 2,000 characters | Prevented or rejected without silent loss |
| AT11 | Leave optional question blank | Allowed |
| AT12 | Add/remove files and reopen | Saved attachment state is correct |
| AT13 | Reject declaration | Submission blocked |
| AT14 | Successful submission | Same item becomes Submitted with timestamp and reference |
| AT15 | Form/attachment save failure | No success screen; input retained |
| AT16 | Final status update failure | Record remains Draft; explicit retry message |
| AT17 | Repeated submit clicks | No duplicate item created |
| AT18 | Retry failed submission | Existing saved item updated, not duplicated |
| AT19 | Publish a new question version | New nominations use it; old drafts/submissions do not change |
| AT20 | Increase 3 questions to 6 | Works without new nomination columns |
| AT21 | Reduce 6 questions to 3 | New items hide unused slots; old items retain six |
| AT22 | Publish incomplete/duplicate question set | Publication blocked; old version remains current |
| AT23 | Cancel category-change warning | Existing unsaved information preserved |
| AT24 | Change saved draft category | Blocked; start-new route offered |
| AT25 | Open another user's direct list/item URL | Access denied under agreed security |
| AT26 | Ordinary user edits configuration directly | Denied |
| AT27 | Open Submitted in app | Read-only |
| AT28 | Direct SharePoint edit after lock flow | Denied under Option B; measured delay documented |
| AT29 | Lock flow fails | Failure visible to administrators; no false lock claim |
| AT30 | Query above nondelegation row limit | Own/category/status results remain complete |
| AT31 | Edit in two sessions | No silent overwrite of detected conflict; limitation documented |
| AT32 | Missing directory connection | Explicit setup/error state, not fake users |
| AT33 | Retire category | New creation blocked; existing records retained |
| AT34 | Back/edit after review | Answers preserved; declaration reset |
| AT35 | Run provisioning twice | No duplicate resources or destructive changes |

Run applicable tests across all six lists, not just one representative category.

---

## 18. Implementation sequence

### Phase 1: Confirm inputs

- Resolve section 4 and security Option A/B.
- Obtain official category/question content.
- Check tooling, licenses, and permissions.

### Phase 2: Provision SharePoint

- Create configuration lists.
- Create six nomination lists.
- Add fields, indexes, version history, and attachment settings.
- Apply initial permissions.
- Verify schemas without using production employee data.

### Phase 3: Seed configuration

- Create six categories initially inactive.
- Create and validate initial question sets.
- Publish version pointers.
- Activate categories.

### Phase 4: Build employee app

- Build Home and Category Selection.
- Implement six typed forms with shared visual patterns.
- Implement snapshots, drafts, attachments, review, and submission.
- Implement My Nominations and read-only viewing.
- Add responsive/accessibility behavior and explicit errors.

### Phase 5: Build question administration

- Restrict access.
- Implement version copying, editing, validation, preview, publication, and conflict handling.

### Phase 6: Implement agreed backend enforcement

- Implement and test permission automation if Option B is selected.
- Validate direct SharePoint access, flow delays, and recovery.

### Phase 7: Validate and deploy

- Execute acceptance matrix.
- Fix failed cases.
- Package/deploy using supported tooling.
- Configure connections and sharing.
- Complete user acceptance testing.
- Record unverified/manual steps and obtain release approval.

---

## 19. Definition of done

The solution is complete only when:

- All eight lists exist with verified schemas.
- Six category mappings are correct.
- Three-to-six-question configuration works for every category.
- Snapshot history is preserved.
- Draft, attachment, review, submit, and retry paths work.
- Business administrators can safely publish new versions.
- User data isolation is tested outside the app.
- Submitted-item limitations are documented and accepted.
- Responsive and accessibility checks pass.
- Deployment instructions are reproducible.
- Test results distinguish executed tests from unexecuted tests.
- No unsupported app package or undeployed feature is represented as working.

---

## 20. Starter instruction to paste into Codex

```text
Read Employee_Team_Awards_Canvas_App_Codex_Spec.md and use it as the
implementation contract.

First inspect the workspace, available supported Power Platform/SharePoint
tooling, and authenticated environment access. Ask for missing deployment
inputs and security decisions before changing tenant resources.

Implement the eight-list SharePoint backend and responsive Canvas app:
six separate category nomination lists, one AwardCategories list, and one
AwardQuestions list. Preserve business-managed versioned question sets,
Q1-Q6 snapshots and responses, nomination-level attachments, incomplete
drafts, review, reliable submission, and own-record security.

Follow the implementation phases and acceptance tests. Use supported
authoring/provisioning formats only. Do not replace the backend, invent
tenant connections, or claim a deployed working app without runtime
verification.

If direct app authoring or tenant access is unavailable, create reproducible
provisioning assets, complete screen/control and Power Fx instructions,
flow setup instructions, and a deployment/test guide. Clearly identify
what was implemented, what was tested, and what needs manual completion.
```
