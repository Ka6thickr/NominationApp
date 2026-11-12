# New tags — reuse Title and show three selectable coloured pills

Updated 12 November 2026. This document replaces the earlier Tags-column/Combo box proposal. It contains only the tag changes. Keep the current components, screen names, answers, attachments and save lifecycle.

**Implementation status:** manual instructions and formulas, not changes applied to the live app/site. The existing base FX files do not yet implement these changes. Apply all sections before enabling the pills. Multi-selection remains optional: users may select zero, one, two or all three tags.

## 1. Final data mapping

| Location | Column | Purpose / storage |
|---|---|---|
| AwardQuestions | Title (existing Single line of text) | Exactly three options, separated by a vertical bar: `Innovation|Customer Value|Teamwork` |
| AwardQuestions | QuestionText | Main question, unchanged |
| AwardQuestions | GuidanceText | Guidance, unchanged |
| AwardQuestions | QuestionKey / DisplayOrder | Heading becomes “Question 1”, “Question 2”, etc. |
| Each nomination list | Q1TagsSnapshot … Q6TagsSnapshot | Original three available options in their original order, stored as pipe-separated plain text |
| Each nomination list | Q1SelectedTags … Q6SelectedTags | Selected labels, pipe-separated plain text; blank means none |

**Do not create AwardQuestions.Tags or Tag1/Tag2/Tag3. Do not change Title's column type.** Title is currently used for criterion headings; all affected heading/snapshot/admin references must change as described here. Nomination-list Title still stores the nomination reference/title: do not repurpose it.

Keep labels at most 40 characters, nonempty and unique ignoring case. Do not include `|`, line breaks or `#` within a label; `#` is added only for display. The combined Title fits its 255-character limit.

### New columns in the six nomination lists

Create the following **12 columns on each list**: BestInnovatorIndividual, MDAward, TrendMarcherAward, BestInnovatorTeam, MDAwardTeam and SpecialTeamAward.

| Slot | Available-option snapshot | Selected values |
|---|---|---|
| Q1 | Q1TagsSnapshot | Q1SelectedTags |
| Q2 | Q2TagsSnapshot | Q2SelectedTags |
| Q3 | Q3TagsSnapshot | Q3SelectedTags |
| Q4 | Q4TagsSnapshot | Q4SelectedTags |
| Q5 | Q5TagsSnapshot | Q5SelectedTags |
| Q6 | Q6TagsSnapshot | Q6SelectedTags |

For every new column: Multiple lines of text, **Plain text**, Required=No, Append changes=No, default blank. Keep all six slots for Team lists even though only three questions are active. This is 72 additive columns, no added configuration column; previous 194 custom columns become 266, excluding built-in Title.

If you already created the previous proposal's columns, reuse the nomination tag columns. An unused AwardQuestions.Tags column may remain; nothing in this design reads it. Do not delete live columns/data as part of this documentation change. If records already contain newline-separated tag selections from that proposal, migrate those values deliberately before using the pipe parser; do not silently reinterpret them.

## 2. Safe configuration migration

| Step | Action |
|---|---|
| 1 | Save a development app checkpoint; create/verify new nomination columns and refresh all six data sources in Studio. |
| 2 | Create a **new complete question version**, leaving published historical rows unchanged. |
| 3 | Set each new row's Title to its three options. Preserve its QuestionText, GuidanceText, category and Q1–Qn sequence. Use new version-specific ConfigurationKey values. |
| 4 | Apply the load, form, review, administrator and validation changes below in the development app. |
| 5 | Validate all three labels per row, then publish the new version by updating the category pointer last. |
| 6 | Test a new nomination and an older saved nomination before release. |

Old saved nominations use their stored prompt/response snapshots. Blank new tag snapshots mean **no tag UI** for those old records. Do not fetch the latest Title to invent tag options on old drafts. Existing old heading text remains visible from its stored prompt. New nominations use “Question n” as their heading.

## 3. Add tag state in every answer record

Use two additional **text** fields in colAnswers: `TagOptions` and `SelectedTags`.

### App.OnStart and New nomination initialization

Replace the answer-record initialization in BOTH actions with:

```powerfx
ClearCollect(colAnswers,
    ForAll(Sequence(6) As n,
        {Slot:n.Value, Prompt:"", Required:false, Response:"",
         TagOptions:"", SelectedTags:""}
    )
);
ClearCollect(colCapturedAnswers,colAnswers);
```

Retain all other initialization, ResetForm and navigation statements. Only the record shape changes.

### Category load: replace its colAnswers construction

After the existing category/version/sequence validation and after setting varQuestionCount, use:

```powerfx
ClearCollect(colAnswers,
    ForAll(Sequence(6) As n,
        With({q:LookUp(colCandidateQuestions,DisplayOrder=n.Value)},
            {Slot:n.Value,
             Prompt:If(n.Value<=varQuestionCount,
                 "Question " & Text(n.Value) & Char(10) & q.QuestionText &
                 If(IsBlank(q.GuidanceText),"",
                    Char(10) & Char(10) & "Guidance: " & q.GuidanceText),""),
             Required:If(n.Value<=varQuestionCount,q.IsRequired,false),
             Response:"",
             TagOptions:If(n.Value<=varQuestionCount,
                 Concat(Split(q.Title,"|"),Trim(Value),"|"),""),
             SelectedTags:""}
        )
    )
);
```

Validate tag options **before this block or any ResetForm calls**. Add this condition to the existing invalid-configuration `If` condition using `||`:

```powerfx
CountIf(colCandidateQuestions As q,
    With({t:ForAll(Split(Coalesce(q.Title,""),"|"),{Value:Trim(Value)})},
        CountRows(t)<>3 ||
        CountRows(Distinct(t,Lower(Value)))<>3 ||
        CountIf(t,IsBlank(Value) || Len(Value)>40 ||
            Char(10) in Value || Char(13) in Value || "#" in Value)>0
    )
)>0
```

Retain the existing version and question validation conditions. Extend the error message to mention that each question needs three unique valid tags. Failure must leave current answers/attachments intact.

## 4. Reusable pill component — create once

Create a Canvas component **cmpQuestionTags**, Access app scope off, default Width=600, Height=44. It handles appearance and clicks only. State remains in the host app. Use custom **Event** properties for behavior, not Text/Data properties.

```text
cmpQuestionTags
  btnTagOne     [classic Button]
  btnTagTwo     [classic Button]
  btnTagThree   [classic Button]
```

### Custom properties

| Name | Property kind/type | Default |
|---|---|---|
| OptionsText | Data Input / Text | "Innovation|Customer Value|Teamwork" |
| SelectedText | Data Input / Text | "" |
| IsReadOnly | Data Input / Boolean | false |
| IsBusy | Data Input / Boolean | false |
| OnTagOne | Event, no parameters | Host-supplied formula |
| OnTagTwo | Event, no parameters | Host-supplied formula |
| OnTagThree | Event, no parameters | Host-supplied formula |

### Layout properties

| Property | btnTagOne | btnTagTwo | btnTagThree |
|---|---|---|---|
| X | 0 | `If(cmpQuestionTags.Width<=760,0,(cmpQuestionTags.Width-16)/3+8)` | `If(cmpQuestionTags.Width<=760,0,2*((cmpQuestionTags.Width-16)/3+8))` |
| Y | 0 | `If(cmpQuestionTags.Width<=760,48,0)` | `If(cmpQuestionTags.Width<=760,96,0)` |
| Width | `If(cmpQuestionTags.Width<=760,cmpQuestionTags.Width,(cmpQuestionTags.Width-16)/3)` | Same as btnTagOne.Width | Same as btnTagOne.Width |
| Height | 44 | 44 | 44 |
| OnSelect | `cmpQuestionTags.OnTagOne()` | `cmpQuestionTags.OnTagTwo()` | `cmpQuestionTags.OnTagThree()` |

The breakpoint uses the component's **available width**, not the whole screen. Below 760 units it stacks the pills, allowing a long label to fit in a narrow form. Set all four button corner-radius properties to 22; Font=Font.'Segoe UI', Size=9.75, BorderThickness=1, FocusedBorderThickness=2, TabIndex=0. Three wide pills in one row are only used when the component has enough width. Verify the full allowed label length at the smallest supported width.

All three buttons DisplayMode:

```powerfx
If(cmpQuestionTags.IsBusy,DisplayMode.Disabled,
    If(cmpQuestionTags.IsReadOnly,DisplayMode.View,DisplayMode.Edit))
```

### Each button's label and selection appearance

In the formulas below replace **K** with literal **1** for btnTagOne, **2** for btnTagTwo and **3** for btnTagThree. K is explanatory, not an app variable.

Text:

```powerfx
With({tag:Trim(Last(FirstN(Split(cmpQuestionTags.OptionsText,"|"),K)).Value)},
    If(tag in Split(cmpQuestionTags.SelectedText,"|").Value,"✓ ","") & "#" & tag)
```

AccessibleLabel:

```powerfx
With({tag:Trim(Last(FirstN(Split(cmpQuestionTags.OptionsText,"|"),K)).Value)},
    tag & If(tag in Split(cmpQuestionTags.SelectedText,"|").Value,
        ". Selected", ". Not selected"))
```

Use these colours for each button:

| Button | Dark / border | Pale background |
|---|---|---|
| btnTagOne | ColorValue("#E20074") | ColorValue("#FDE6F1") |
| btnTagTwo | ColorValue("#0F6CBD") | ColorValue("#E8F2FC") |
| btnTagThree | ColorValue("#107C10") | ColorValue("#EAF5EA") |

Fill formula (replace K, DARK and PALE with the literal slot and corresponding ColorValue expressions):

```powerfx
With({tag:Trim(Last(FirstN(Split(cmpQuestionTags.OptionsText,"|"),K)).Value)},
    If(tag in Split(cmpQuestionTags.SelectedText,"|").Value,DARK,PALE))
```

Color uses the same condition, returning Color.White if selected, otherwise DARK. BorderColor=DARK. HoverFill=Self.Fill, HoverColor=Self.Color, PressedFill=DARK, PressedColor=Color.White. Do not use a global selected flag for all pills: each reads its own label in SelectedText. The checkmark communicates selection independently of colour. Colours follow **option position in the saved snapshot**.

## 5. Insert one instance into each active question container

Example Q1 on Best Innovator Individual:

```text
dcIIQ1Response
  cntIIQ1
    lblIIQ1Heading
    cmpIIQ1Tags       [instance of cmpQuestionTags]
    lblIIQ1Prompt
    txtIIQ1
    lblIIQ1Counter
  errIIQ1
```

| Property | Formula |
|---|---|
| cmpIIQ1Tags.OptionsText | `LookUp(colAnswers,Slot=1,TagOptions)` |
| cmpIIQ1Tags.SelectedText | `LookUp(colAnswers,Slot=1,SelectedTags)` |
| cmpIIQ1Tags.IsReadOnly | `varReadOnly` |
| cmpIIQ1Tags.IsBusy | `varIsBusy` |
| cmpIIQ1Tags.X | 22 |
| cmpIIQ1Tags.Y | `lblIIQ1Heading.Y+lblIIQ1Heading.Height+8` |
| cmpIIQ1Tags.Width | `Parent.Width-44` |
| cmpIIQ1Tags.Visible | `1<=varQuestionCount && !IsBlank(Trim(Self.OptionsText))` |
| cmpIIQ1Tags.Height | `If(Self.Visible,If(Self.Width<=760,140,44),0)` |
| lblIIQ1Prompt.Y | `If(cmpIIQ1Tags.Visible,cmpIIQ1Tags.Y+cmpIIQ1Tags.Height+8,lblIIQ1Heading.Y+lblIIQ1Heading.Height+8)` |

Existing prompt → input → counter → container → card height calculations then move the rest of the form down automatically. Keep existing title/required-marker expressions: new Prompt begins with “Question n”; old snapshots retain their original headings.

### Host click handler — Q1 first pill

Set **cmpIIQ1Tags.OnTagOne** to:

```powerfx
If(!varIsBusy && !varReadOnly,
    With({a:LookUp(colAnswers,Slot=1)},
        With({options:ForAll(Split(a.TagOptions,"|"),{Value:Trim(Value)}),
              clicked:Trim(Last(FirstN(Split(a.TagOptions,"|"),1)).Value)},
            Patch(colAnswers,a,
                {SelectedTags:Concat(
                    Filter(options As option,
                        If(option.Value=clicked,
                            !(option.Value in Split(a.SelectedTags,"|").Value),
                            option.Value in Split(a.SelectedTags,"|").Value)),
                    Value,"|")})
        )
    );
    Set(varHasChanges,true);
    Set(varResponsesComplete,false);
    Set(varDeclarationAccepted,false)
)
```

For OnTagTwo and OnTagThree change only the FirstN count from 1 to 2 or 3. For another question change LookUp Slot=1 to that question's slot. Selections are serialized in option order, regardless of click order. Each click updates only that question. No direct SharePoint write occurs on a pill click.

### Exact instance names

| Screen / prefix | Instances inside corresponding cntXXQ1 … cntXXQ6 |
|---|---|
| scrBestInnovatorIndividual / II | cmpIIQ1Tags, cmpIIQ2Tags, cmpIIQ3Tags, cmpIIQ4Tags, cmpIIQ5Tags, cmpIIQ6Tags |
| scrMDAward / IC | cmpICQ1Tags, cmpICQ2Tags, cmpICQ3Tags, cmpICQ4Tags, cmpICQ5Tags, cmpICQ6Tags |
| scrTrendMarcherAward / IE | cmpIEQ1Tags, cmpIEQ2Tags, cmpIEQ3Tags, cmpIEQ4Tags, cmpIEQ5Tags, cmpIEQ6Tags |
| scrBestInnovatorTeam / TC | cmpTCQ1Tags, cmpTCQ2Tags, cmpTCQ3Tags, cmpTCQ4Tags, cmpTCQ5Tags, cmpTCQ6Tags |
| scrMDAwardTeam / TI | cmpTIQ1Tags, cmpTIQ2Tags, cmpTIQ3Tags, cmpTIQ4Tags, cmpTIQ5Tags, cmpTIQ6Tags |
| scrSpecialTeamAward / TT | cmpTTQ1Tags, cmpTTQ2Tags, cmpTTQ3Tags, cmpTTQ4Tags, cmpTTQ5Tags, cmpTTQ6Tags |

Apply the Q1 property table with the corresponding prefix/slot. Do not copy a component definition 36 times; insert 36 instances of the one definition. Hidden trailing slots have Height=0.

## 6. Save, capture and reopen — required integration

### Capture before Save draft, Review and Back to details

In every slot record in colCapturedAnswers, preserve the new strings from colAnswers. Example II/Q1:

```powerfx
{Slot:1,
 Prompt:LookUp(colAnswers,Slot=1,Prompt),
 Required:LookUp(colAnswers,Slot=1,Required),
 Response:txtIIQ1.Text,
 TagOptions:LookUp(colAnswers,Slot=1,TagOptions),
 SelectedTags:LookUp(colAnswers,Slot=1,SelectedTags)}
```

Apply to all six slots in all six forms' capture actions. Pills already update the collection on each click; do not attempt to read SelectedItems from a pill component. Retain the new fields when replacing colAnswers with colCapturedAnswers.

### Hidden native cards in each form

After refreshing the data source, add the twelve tag fields through Edit fields → Add field. Unlock cards, retain generated DataField/Default bindings, set Visible=false, Height=0, Required=false and place them with hidden metadata. For each prefix XX and slot n:

| Card name | DataField | Update pattern |
|---|---|---|
| dcXXQnTagsSnapshot | QnTagsSnapshot | `If(n<=varQuestionCount,LookUp(colAnswers,Slot=n,TagOptions),"")` |
| dcXXQnSelectedTags | QnSelectedTags | `If(n<=varQuestionCount,LookUp(colAnswers,Slot=n,SelectedTags),"")` |

Example exact Q1/II properties:

```powerfx
// dcIIQ1TagsSnapshot.Update
If(1<=varQuestionCount,LookUp(colAnswers,Slot=1,TagOptions),"")
```

```powerfx
// dcIIQ1SelectedTags.Update
If(1<=varQuestionCount,LookUp(colAnswers,Slot=1,SelectedTags),"")
```

Do not change answer-card Update, form OnSuccess or attachment bindings. SubmitForm saves the new card values with answers/files on the same nomination. The existing successful final status Patch stays where it is.

### Reopen from My nominations

Extend every slot record loaded from varRecordII/IC/IE/TC/TI/TT. Example II/Q1:

```powerfx
{Slot:1,
 Prompt:Coalesce(varRecordII.Q1PromptSnapshot,""),
 Required:Coalesce(varRecordII.Q1RequiredSnapshot,false),
 Response:Coalesce(varRecordII.Q1Response,""),
 TagOptions:Coalesce(varRecordII.Q1TagsSnapshot,""),
 SelectedTags:Coalesce(varRecordII.Q1SelectedTags,"")}
```

Repeat for slots 2–6 and each source-specific record variable. Keep the existing ResetForm/EditForm/ViewForm lifecycle. No current configuration lookup should replace saved tag options. New nomination and successful category changes clear tag selections via the new initialization; normal OnVisible must not clear them.

## 7. Submission validation

Add this named formula to App.Formulas and append `&& TagsValid` to the existing ResponsesValid expression. Keep all original answer-required and length checks.

```powerfx
TagsValid = CountIf(Filter(colAnswers,Slot<=varQuestionCount) As answer,
    With({opts:Filter(Split(Coalesce(answer.TagOptions,""),"|"),!IsBlank(Value)),
          chosen:Filter(Split(Coalesce(answer.SelectedTags,""),"|"),!IsBlank(Value))},
        If(IsEmpty(opts),
            !IsEmpty(chosen),
            CountRows(opts)<>3 ||
            CountRows(Distinct(opts,Lower(Value)))<>3 ||
            CountRows(chosen)>3 ||
            CountRows(Distinct(chosen,Lower(Value)))<>CountRows(chosen) ||
            CountIf(chosen As selected,!(selected.Value in opts.Value))>0
        )
    )
)=0;
```

Blank old snapshots with no selection pass. A selection outside its snapshot fails. Zero selected tags passes because tags are optional. Published configuration validation enforces valid label text before new nominations load. Show a useful tag-validation notification when Review is blocked by !TagsValid; do not mislabel this as a missing answer.

## 8. Question administration — reuse txtAdminTitle

| Control / location | Change |
|---|---|
| Label above txtAdminTitle | Text = "Tag options (three, separated by |)" |
| txtAdminTitle | Keep Default=ThisItem.Title, MaxLength=255, existing local Title OnChange; AccessibleLabel="Three tag options separated by vertical bars" |
| Help text | "Example: Innovation | Customer Value | Teamwork. Each label: 1–40 characters." |
| Question and guidance inputs | Keep unchanged |
| Admin copy/load | Keep copying Title; no new Tags field |
| Admin publication | Keep writing q.Title and checking saved/existing Title equality |
| Admin preview | Display "Question " & Text(ThisItem.Slot) as heading; show the three Title options as pills or a label below it |

Before building colAdminEdits for publishing, normalize the captured Title:

```powerfx
// Replace Title: row.txtAdminTitle.Text in the capture record with:
Title:Concat(Split(row.txtAdminTitle.Text,"|"),Trim(Value),"|")
```

The subsequent local Patch already copies edit.Title. Add the same three-option validation from section 3 to the invalid-publication condition, substituting **colAdminQuestions** for colCandidateQuestions. Keep all existing slot, version, text and key checks. The existing comparison of q.Title against existing.Title and saved.Title now validates tags as well. Do not add a new Tags field to the Patch or to the question schema.

Published old rows may have ordinary criterion titles. Copy them to a new version, replace each copied title with valid options, validate, then publish. The category pointer still changes only after saved-set read-back. No direct editing of previously published versions.

## 9. Review display

Inside each cntReviewQn insert an instance cmpReviewQnTags between lblReviewHeadingn and lblReviewPromptn. Bind OptionsText and SelectedText from that slot in colAnswers, IsReadOnly=true, IsBusy=varIsBusy. X=28, Width=Parent.Width-56, Y=heading.Y+heading.Height+8, Visible when OptionsText is nonblank, Height=`If(Self.Visible,If(Self.Width<=760,140,44),0)`.

Position the prompt below the instance when visible, otherwise below the heading. The existing answer and review-card height formulas expand from there. All three options remain visible with the selected pills filled; no clicking is permitted on review. Legacy snapshots show no tag instance. Submitted records use the native form in View mode with varReadOnly=true.

## 10. Apply and verify in this order

| Order | Task | Evidence |
|---|---|---|
| 1 | Create/verify nomination columns; refresh connectors | All twelve fields offered in each form |
| 2 | Extend answer state, loading, captures and reopen records | No tag data lost on Back/Review |
| 3 | Create cmpQuestionTags and its Event properties | Three independent toggle actions |
| 4 | Add II/Q1 instance and its hidden cards | Two selected tags save/reopen under same ID |
| 5 | Apply remaining slots and forms | Team trailing tag fields stay blank |
| 6 | Update admin title labels/validation and publish a new version | Exactly three options per new question |
| 7 | Add read-only review instances and TagsValid | Invalid selections block submission |
| 8 | Test old/new records, failures and mobile wrapping | No old snapshots replaced; no clipped labels |

Test click/deselect/all/none, two separate questions with independent state, draft reopen, declaration invalidation, new category discard Cancel/Confirm, attachment retention, server failure and read-only reopening. Verify palette colours remain attached to saved option positions after a later question-version change. No email/notification flow is added.

This is a manual change specification, not Studio-compiled code. Instructions with XX/n/K placeholders require literal substitutions stated above. Old tag-Combo-box instructions are superseded; do not combine the newline serialization with this pipe-separated design.
