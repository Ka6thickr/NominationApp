"""Generate the additive manual schema and implementation checklist for tags."""
from pathlib import Path
import csv
root=Path(__file__).resolve().parents[1]
out=root/'production-guide'
rows=[('II','BestInnovatorIndividual'),('IC','MDAward'),('IE','TrendMarcherAward'),('TC','BestInnovatorTeam'),('TI','MDAwardTeam'),('TT','SpecialTeamAward')]
fields=[('AwardQuestions','Tags')]+[(name,f'Q{i}{suffix}') for p,name in rows for i in range(1,7) for suffix in ('TagsSnapshot','SelectedTags')]
with (out/'Tag-Columns.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.writer(f);writer.writerow(['List','InternalName','Type','Required','RichText','AppendChanges'])
    writer.writerows((name,field,'Multiple lines of text','No','No','No') for name,field in fields)
parts=['''# Selectable question tags — additive schema and manual implementation

This is the newly requested schema extension. It supersedes earlier statements that tags are deferred or no columns may be added. Existing columns remain unchanged. The current implementation below assumes optional multi-select tags, with at most three options per question. Required/single-select tags are not introduced silently.

**Status:** manual implementation specification. The new site's actual URL and live app are not connected here, so no live columns or controls have been created. Existing FX files do not yet contain this extension: apply every integration step below before enabling tag selection in the app. Do not add only the UI and assume tags will save.

## 1. Create the columns first

Use List settings → Create column. Enter the exact internal name on initial creation. For every new column choose **Multiple lines of text → Plain text**, Required=No, Append changes=No, default blank. Do not use a SharePoint Choice column: the available options vary by question/version.

| List | Columns | Purpose |
|---|---|---|
| AwardQuestions | Tags | Available tag options for this question/version |
| Each of the six nomination lists | Q1TagsSnapshot through Q6TagsSnapshot | Original available options saved with the nomination |
| Each of the six nomination lists | Q1SelectedTags through Q6SelectedTags | User's selections saved with the answer |

See [the exact 73-row column checklist](Tag-Columns.csv). AwardCategories needs no change. With the previous schema this raises custom columns from 194 to 267 (excluding built-in Title). Each individual form gains 12 metadata cards; each team form gains 12. Keep Q4–Q6 tag columns even for Team categories with only three questions.

Store one tag per line, without the decorative # prefix:

```text
Innovation
Customer Value
Teamwork
```

Blank means no options/selection. For new versions trim labels, remove blank lines, forbid embedded line breaks within a label and duplicates ignoring case, and limit to three labels. Do not append tags to Title, GuidanceText or QnResponse. The answer remains plain answer text.

## 2. Refresh connections and add native cards

| Step | Action |
|---|---|
| 1 | Refresh AwardQuestions and all six nomination data sources in Studio after creating columns. |
| 2 | In each form choose Edit fields → Add field; add all twelve new fields. |
| 3 | Rename new cards using the screen-specific tables below; preserve generated DataField and Default bindings. |
| 4 | Set each new card Visible=false, Height=0, Required=false. Put them after existing metadata cards. |
| 5 | Apply their Update formulas below. SubmitForm then saves tags with answers and attachments in the same item save. No separate tag Patch is needed after submission. |

## 3. Extend in-memory state before adding controls

Add two text fields to every colAnswers record: **TagOptions** and **SelectedTags**.

| Lifecycle location | Required fields in each record |
|---|---|
| App.OnStart and New nomination initialization | `TagOptions: "", SelectedTags: ""` |
| Category load: the record inside ForAll(Sequence(6)) | `TagOptions: If(n.Value <= varQuestionCount, Coalesce(q.Tags,""), ""), SelectedTags: ""` |
| Save/Review/Back capture into colCapturedAnswers | Preserve TagOptions from matching colAnswers slot; capture SelectedTags from that question's combo SelectedItems. |
| Reopen saved nomination | Load TagOptions from QnTagsSnapshot and SelectedTags from QnSelectedTags, with Coalesce(..., ""). |
| Changing category after confirmation | Initialize the new snapshots and clear selections together with answers; existing ResetForm calls reset selectors. |

For example, the complete Q1 capture record for II becomes:

```powerfx
{Slot: 1,
 Prompt: LookUp(colAnswers,Slot=1,Prompt),
 Required: LookUp(colAnswers,Slot=1,Required),
 Response: txtIIQ1.Text,
 TagOptions: LookUp(colAnswers,Slot=1,TagOptions),
 SelectedTags: Concat(cmbIIQ1Tags.SelectedItems,Value,Char(10))}
```

Use the corresponding slot and prefix in all six forms' Save draft, Review and Back-to-details capture tables. Preserve both new fields when copying colCapturedAnswers into colAnswers. Do not rebuild a three-field record and lose the selections.

## 4. Per-question controls and hidden card Update formulas

Inside each existing question container cntXXQn, add a **classic Combo box** immediately below its heading and above the prompt. Do not place it outside the native response card. Tags are optional and distinct from required answer text.

| Property on every tag Combo box | Value |
|---|---|
| SelectMultiple | true |
| IsSearchable | false |
| DisplayFields / SearchFields | ["Value"] / ["Value"] |
| X / Width | 22 / Parent.Width-44 |
| Height | If(Self.Visible,40,0) |
| Fill / Color / BorderColor | varAppTheme.Pale / varAppTheme.Primary / varAppTheme.Border |
| SelectionFill / SelectionColor | varAppTheme.Primary / Color.White |
| InputTextPlaceholder | "Select tags (optional)" |
| AccessibleLabel | "Optional tags for this question" |

The following tables specify the exact names and formulas for every form. Items removes empty lines and trims values; publish-time validation remains responsible for rejecting duplicate or excessive options. If tags are blank, the control is hidden with zero height. # is presentation only; do not add it to the saved values.
''']
for p,name in rows:
    parts.append(f'\n### scr{name} / frm{name}\n\n| New hidden card | DataField | Update |\n|---|---|---|')
    for i in range(1,7):
        parts += [f'| dc{p}Q{i}TagsSnapshot | Q{i}TagsSnapshot | `If({i}<=varQuestionCount,LookUp(colAnswers,Slot={i},TagOptions),"")` |',f'| dc{p}Q{i}SelectedTags | Q{i}SelectedTags | `If({i}<=varQuestionCount,Concat(cmb{p}Q{i}Tags.SelectedItems,Value,Char(10)),"")` |']
    for i in range(1,7):
        c=f'cmb{p}Q{i}Tags'
        parts.append(f'''\n#### {c}

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot={i},TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{{Value:Trim(Value)}})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot={i},SelectedTags),""),Char(10)).Value)` |
| Visible | `{i}<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot={i},TagOptions)))` |
| Y | `lbl{p}Q{i}Heading.Y+lbl{p}Q{i}Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dc{p}Q{i}Response.DisplayMode)` |
| lbl{p}Q{i}Prompt.Y | `If({c}.Visible,{c}.Y+{c}.Height+8,lbl{p}Q{i}Heading.Y+lbl{p}Q{i}Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot={i}),
    {{SelectedTags:Concat(Self.SelectedItems,Value,Char(10))}});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecord{p}.Q{i}TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecord{p}.Q{i}SelectedTags,"")` to slot {i}'s record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.
''')
parts.append('''
## 5. Extend the question administrator workflow

Add classic multiline Text input **txtAdminTags** to the galAdminQuestions template, below chkAdminRequired. Label it “Tag options — one per line, maximum 3”. Default=`ThisItem.Tags`, Mode=TextMode.MultiLine, DelayOutput=false, Height=90. Increase TemplateSize to at least 570 desktop / 650 mobile so the new input does not overlap the next row.

```powerfx
// txtAdminTags.OnChange
Patch(colAdminQuestions,LookUp(colAdminQuestions,Slot=ThisItem.Slot),
    {Tags:Substitute(Self.Text,Char(13),"")});
Set(varAdminDirty,true)
```

| Existing code location | Exact integration |
|---|---|
| App initialization and Add question record | Add `Tags:""` to the local record schema. |
| Admin.LoadCopy.OnSelect: empty three-row initialization | Add `Tags:""`. |
| Admin.LoadCopy.OnSelect: record from colAdminSource as q | Add `Tags:Coalesce(q.Tags,"")`. |
| Admin.Publish.OnSelect: colAdminEdits capture | Add `Tags:Substitute(row.txtAdminTags.Text,Char(13),"")`. |
| Admin.Publish: Patch local colAdminQuestions | Add `Tags:edit.Tags`. |
| New AwardQuestions Patch record | Add `Tags:q.Tags`. |
| Existing partial-version row equality check | Also require `Coalesce(existing.Tags,"")=q.Tags`. |
| Saved-set read-back mismatch check | Also reject `Coalesce(saved.Tags,"")<>q.Tags`. |

Before creating any SharePoint rows, normalize each Tags field by splitting on Char(10), trimming values, dropping empty lines and joining with Char(10). Validate count <=3 and uniqueness ignoring case. If invalid, notify the administrator and do not enter the publish branch. Include Tags in every equality/read-back check; otherwise the version pointer could advance despite an incomplete tag save. Only update PublishedQuestionVersion after the entire set, including tags, has been saved and verified.

Publish a **new** question version to add/change tag options. Do not edit existing published rows or backfill old nomination snapshots automatically. Direct list editing must follow the same normalization/validation rules.

## 6. Review and submit validation

For each review block add a label after lblReviewPromptn and before lblReviewAnswern. Text uses the snapshot selection, not a current question lookup. Example:

```powerfx
// lblReviewTags1.Text
Concat(Filter(Split(Coalesce(LookUp(colAnswers,Slot=1,SelectedTags),""),Char(10)),
    !IsBlank(Value)), "#" & Value, "   ")
```

Use varAppTheme.Primary text, varAppTheme.Pale fill, AutoHeight=true, Visible when nonblank. Set answer Y below this label when visible, otherwise retain the existing prompt-relative Y. Repeat slots 1–6. Do not clip wrapped tags.

In ResponsesValid, retain existing required-answer/length rules and additionally reject any active slot where selected tags are not a subset of its TagOptions snapshot, exceed three or contain duplicates. Tags remain optional: an empty selection is valid. Validate available options before loading a category too, because direct SharePoint edits can bypass the administrator UI. Gate final submission with these checks; do not silently discard invalid tags.

## 7. Manual acceptance tests

| Test | Expected |
|---|---|
| Question without Tags | No selector; existing flow works |
| Select two tags and save draft | Answer, snapshot options and selections saved on the same item |
| Reopen draft | Same selections restored; no new item created |
| Return from Review | Selections and pending attachments retained |
| Change tag selection | Declaration and response completion reset |
| Submit / ViewForm | Saved tags visible; selector read-only |
| Publish changed tag labels | Old nominations retain old available/selected tags |
| Team with three questions | Q4–Q6 tag fields blank |
| Legacy record with blank snapshots | No selection invented from current configuration |
| Invalid/duplicate/four tag options | Loading/publication blocked; no pointer update |
| Failed SubmitForm | No false success; inputs remain |

The classic combo supports multiple selection through SelectMultiple and SelectedItems; see [Microsoft Combo box properties](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-combo-box). These recipes require Studio type checking and runtime testing after the schema extension.
''')
(out/'03-Question-Tags.md').write_text('\n'.join(parts),encoding='utf-8')
print('Created tag specification and exact checklist for 73 additive columns.')
