# Team and Individual Nomination App — screen plan

Status: implementation blueprint, not a deployed Canvas app. Contoso branding is retained. The eight-list SharePoint schema is fixed. Question tags are deferred; no tag storage or behavior has been assumed.

The complete manual implementation is now in [manual-build/README.md](manual-build/README.md). It refines this blueprint by keeping nominee editing on step 1, using the six typed forms in View mode for submitted records instead of duplicating scrViewNomination, and initially copying shared native visual controls while making the stepper reusable. Follow the manual's exact control names/formulas for construction. These formulas have not yet been compiled or tested in Canvas Studio.

## Data-driven behavior

| Content/behavior | Source | Change without editing screen layout? |
|---|---|---|
| Category name, description, order, active status | Category configuration records | Yes |
| Published question version | Category configuration record | Yes, through controlled publication |
| Question text, guidance, required flag, order | Question configuration records | Yes |
| Question count, 3–6 | Validated rows in the published category/version | Yes |
| Employee levels | Choice metadata of the selected nomination list | Yes; synchronize choices across all six lists |
| Employee/person search | Approved employee directory connection | Yes; no sample-person records in app formulas |
| Current nominator | Signed-in user's identity | Yes; read-only |
| Historical prompts and required flags | Nomination Q1–Q6 snapshots | Frozen for each saved nomination |
| Site and physical destination lists | Deployment configuration and solution data-source environment variables | Environment rebinding, not a runtime string lookup |
| Contoso logo, brand text, colors | One app theme/branding component | Centralized app change later |
| Six stable category-to-form mappings | Explicit app routing | A new category/list requires app changes |

All question wording comes from SharePoint. Six reserved response slots are a storage layout, not six hardcoded questions. No wording should be embedded in question controls or category-specific formulas.

The current category records are inactive and have no published version pointer. Until development publication is approved, the employee category page should show a clear no-active-categories state. Question administration can preview the unpublished seed rows.

## Environment setup

1. Use the user-selected **Ka6thickMSFT** Power Platform environment; verify its environment ID in the maker portal before deployment. Solution/publisher naming remains to be set.
2. Create the responsive Canvas app inside that solution.
3. Configure one SharePoint site data-source environment variable and eight list data-source environment variables. List values are destination GUIDs from `provisioning/deployment-result.json`.
4. Connect each source through its environment variable. Preserve the typed data source for each form. Do not attempt to assign a list-name string to a form's DataSource.
5. Add the approved employee directory connection; document its ownership and sharing requirements.
6. Disable desktop-only scaling/locked aspect behavior and use responsive layout containers. Validate control-specific properties in the target Studio version.
7. Create shared branding, navigation, stepper, summary, action-bar, and message components.

## Screen and control inventory

| Screen | Main controls | Data and behavior |
|---|---|---|
| `scrHome` | `cmpHeader`, `cmpNavigation`, Individual/Team selection cards, instructions, My nominations button | Entry point; selects award type; administration entry visible only to authorized managers |
| `scrNomineeDetails` | `cmpStepper`, signed-in nominator label, type selector, nominee/team/contact pickers, role and level inputs | Step 1; details held in memory until category selection; no persistent save before a valid destination is known |
| `scrCategorySelection` | `cmpStepper`, `galCategories`, empty/error message, Back/Continue buttons | Three active categories for the award type, sorted by DisplayOrder; explicit selection; validates published questions |
| `scrIndividualInnovation` | `frmIndividualInnovation`, nominee picker, role/level inputs, six question cards, native attachment card, progress summary | Typed form for `IND_INNOVATION` |
| `scrIndividualCustomer` | `frmIndividualCustomer`, same visual/control pattern | Typed form for `IND_CUSTOMER` |
| `scrIndividualExcellence` | `frmIndividualExcellence`, same visual/control pattern | Typed form for `IND_EXCELLENCE` |
| `scrTeamCollaboration` | `frmTeamCollaboration`, team name/contact/member pickers, role/level, six question cards, native attachment card, progress summary | Typed form for `TEAM_COLLAB` |
| `scrTeamImpact` | `frmTeamImpact`, same team visual/control pattern | Typed form for `TEAM_IMPACT` |
| `scrTeamTransformation` | `frmTeamTransformation`, same team visual/control pattern | Typed form for `TEAM_TRANSFORM` |
| `scrReview` | Nominee summary, category summary, snapshot/answer review, file list, Edit links, declaration, Submit | Reviews current unsaved edits; submission delegates to the active typed form |
| `scrConfirmation` | Success state, derived reference, saved timestamp/category/nominee, View and New buttons | Reached only after successful Submitted status update |
| `scrMyNominations` | Award-type/category/status selectors, source-specific gallery, empty/error/loading states | Delegable own-record queries against the selected list; does not merge six unbounded lists into a collection |
| `scrViewNomination` | Read-only details, saved prompts/answers, attachment links | Refreshes status; no edit/submit actions for Submitted items |
| `scrQuestionAdministration` | Category/version selectors, editable draft question rows, Add/Remove slot, Preview, Publish | Restricted configuration management; copy to a new version; never edit a published version |

The latest user reference establishes the four displayed steps: **Nominee details → Award category → Criteria & evidence → Review & submit**. Initial nominee details are held in app state before category selection; persistent draft saving becomes available only after a category and valid question version identify the destination. Do not silently choose a category to enable an early save. The category-specific typed form receives those initial details when initialized. The backend schema remains unchanged.

## Reusable components

- `cmpHeader`: Contoso mark, app name, signed-in display, Help action when a real help destination is supplied.
- `cmpNavigation`: New nomination/My nominations; administration is a separate restricted entry.
- `cmpStepper`: reusable four-step presentation with current/completed/upcoming states, input-driven labels and theme colors. Use an SVG Image control for explicit SVG fill/stroke changes, or HTML Text with inline CSS for the HTML-only variant. Drive appearance with Power Fx input properties; do not depend on JavaScript or embedded HTML click handlers. Use native Canvas buttons for any step navigation. See `Process-Stepper-Component.md` for setup, state handling and SVG Power Fx. Completed state represents validated progress, not a saved/submitted record.
- `cmpNominationSummary`: award type, category, nominee/team from current state.
- `cmpActionBar`: Back, Save draft, Review/Submit; all mutation actions disabled while busy.
- `cmpStatusMessage`: loading, save success, failure, configuration unavailable, and conflict states with accessible text.
- Question card layout: slot number, wrapped prompt snapshot, required indicator, multiline response, character counter, completion indicator. The actual editable controls remain associated with the relevant typed form; avoid putting a SharePoint attachment editor in a generic component or gallery.

## Form data contract

Each category form uses its own source and its own saved record. Share only presentation/state primitives, not records assumed interchangeable across lists.

| Form section | Individual | Team |
|---|---|---|
| Nominator | Signed-in user, read-only | Signed-in user, read-only |
| Nominee identity | NominatedEmployee | TeamName and TeamPrimaryContact |
| Role and level | Nominee role/level | Primary contact role/level |
| Additional people | None | Optional TeamMembers |
| Questions | Q1–Q6, visible up to saved count | Same |
| Evidence | One nomination-level attachment card | Same |

Metadata cards set category, question version/count, nominator identity/email, draft status, declaration, and timestamps through app state. Snapshot cards store prompt/guidance and required flags captured at initialization. They are never replaced by current question configuration when resuming a draft.

Use six explicit input slots with consistent naming per form (`txtQ1Response` through `txtQ6Response` with a form-specific prefix). A slot is visible only when its number is at most QuestionCount. Required behavior uses its saved flag. Configure response length and whitespace validation consistently. The initial 2,000-character limit is centralized app configuration.

For historical display, use the full saved prompt, which contains guidance when present. Do not rely on the current question Title/GuidanceText to reconstruct an older question. A generic heading such as “Question 1” can accompany the stored prompt without adding columns.

## State and lifecycle

| State | Responsibility |
|---|---|
| CurrentAwardType | Individual or Team |
| CurrentCategory | Selected configuration record and stable code |
| CurrentQuestionVersion / CurrentQuestionCount | Captured, validated version and count |
| CurrentQuestions | Bounded question set, at most six rows |
| CurrentNominationId | Blank until first save; retained on every retry |
| IsBusy / SaveIntent | Prevent duplicate actions; distinguish Draft and Submit |
| ReviewModel | Normalized display of current edits, snapshot text, answers and filenames |
| DeclarationAccepted | Reset after editing reviewed content |
| PendingNavigation | User-confirmed handling of unsaved changes |

### New nomination

1. Enter nominee/team details and choose award type in step 1. Hold these in memory. Choose the category in step 2 before the first persistent save.
2. Read category's published version and retrieve only that question set.
3. Validate 3–6 rows, contiguous Q1..QN, matching DisplayOrder, unique keys, nonblank text and matching category/version.
4. Initialize snapshots and blank responses in the correct typed form.
5. Permit incomplete draft saving. No required-answer or nominee-required validation at draft save; enforce field formats and maximum response length.
6. Once saved, retain the item ID and switch to editing that item. Lock its category and question version.

### Review and submit

1. Validate required nominee details and required responses; whitespace-only answers are empty.
2. Build the review from current input, including unsaved changes and intended attachment state.
3. Require the declaration. Editing or returning to change content resets it.
4. Set busy/save intent and submit the active form as Draft.
5. In that form's success event, capture LastSubmit and the exact saved ID.
6. Only then change that saved item to Submitted, with declaration and submission time.
7. Navigate to confirmation only on status-update success. If the second save fails, retain the saved ID and report that submission was not confirmed. Refresh status before retrying: a timeout can occur after the server has committed, so do not assert that it definitely remains a Draft. An ambiguous timeout during the initial new-item save also requires checking My nominations before creating again; the fixed schema has no client idempotency key.
8. Form failure preserves entered data and stays on the form/review; all terminal paths clear busy state.

### Resume/view

Refresh the item and check its current status. Drafts load saved snapshots, responses and native attachments. Submitted items open read-only. Refresh status again before submission and handle detected conflicts; these checks are not atomic locking. References combine stable category code with padded list item ID.

### Question administration

Select category; copy a version into a new unpublished version; edit prompt/guidance/required flags; add or remove slots within 3–6; preview the employee card layout; save all records; re-read and validate; update the category published pointer last. Keep old versions and nomination snapshots. Coordinate a single publisher per category unless a serialized publication mechanism is later implemented.

## Visual baseline from supplied CSS

These are source values, not a claim of pixel-perfect Canvas rendering. Power Apps control font units, font-weight options, native shadows, and line-height behavior must be checked in Studio rather than blindly copying CSS numbers.

| Token/layout | Source value |
|---|---|
| Font | Segoe UI |
| Primary / hover | `#0f6cbd` / `#0b5a9e` |
| Heading / body / muted | `#17253f` / `#27364f` / `#667085` |
| Background / surface | `#f4f6f8` / `#ffffff` |
| Border / subtle border | `#d8dee7` / `#e8ebf0` |
| Success / error | `#107c10` / `#c50f1f` |
| Header | 64px height; 40px horizontal padding |
| Stepper | 1060px maximum width; 94px height; 20px horizontal padding |
| Main page | 1030px maximum width; 39px top, 24px horizontal, 56px bottom padding |
| Form card | 30px vertical, 34px horizontal padding |
| Main heading | 30px CSS font size; 1.2 line height; weight 650 |
| Two-column detail row | 18px gap; 590px maximum width |
| Question area/sidebar | Flexible main area + 260px sidebar; 22px gap |
| Question card | 8px corner radius; 18px bottom spacing |
| Question header | 20px vertical, 22px horizontal padding; 17px title |
| Buttons | 38px height; 4px corner radius; 16px horizontal padding |
| Responsive breakpoint | 760px |

The screenshots appear to use a more violet primary accent than the CSS token. Resolve screenshot-versus-CSS visual differences in the first screen review; do not silently treat them as identical. Keep a single theme definition so the approved palette can be updated once.

At narrow widths: stack category cards and detail fields, put progress above the questions, keep controls within viewport width, wrap long prompts, and show nomination rows as stacked cards. Do not copy the prototype's five-line clipping of review responses: employees need to read the full answer before declaring it accurate. Test at approximately 390px, tablet width, and desktop width.

## Validation sequence

1. Connect one form and test empty draft → save → reload same ID, including native files.
2. Add dynamic question retrieval/snapshots and test a new published version does not change existing drafts.
3. Add review/declaration and simulate form failure and final status-update failure.
4. Apply the same pattern to all six typed forms and execute the source specification's acceptance matrix for each category.
5. Test My nominations above the nondelegation limit, including status filters.
6. Test question publication failure, duplicate keys and old-version retention.
7. Test direct SharePoint permissions with separate nominator/admin accounts; test submitted-item policy once chosen.
8. Complete keyboard, screen-reader, long-text and responsive checks before release.

## Outstanding inputs

- Verify the selected Ka6thickMSFT environment ID and choose solution/publisher naming.
- Approval to activate the current seed content for development, distinct from production approval.
- Official category/question wording and employee levels for production.
- Nominator, configuration-manager and awards-administrator groups.
- Submitted-item enforcement option, attachment policy and directory connector approval.
- Resolve CSS/screenshot accent differences; the four-step order now follows the latest user reference.

No new SharePoint columns are required by this plan. Deferred question tags must be discussed separately before any schema changes.
