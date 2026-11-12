# Selectable question tags — additive schema and manual implementation

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


### scrBestInnovatorIndividual / frmBestInnovatorIndividual

| New hidden card | DataField | Update |
|---|---|---|
| dcIIQ1TagsSnapshot | Q1TagsSnapshot | `If(1<=varQuestionCount,LookUp(colAnswers,Slot=1,TagOptions),"")` |
| dcIIQ1SelectedTags | Q1SelectedTags | `If(1<=varQuestionCount,Concat(cmbIIQ1Tags.SelectedItems,Value,Char(10)),"")` |
| dcIIQ2TagsSnapshot | Q2TagsSnapshot | `If(2<=varQuestionCount,LookUp(colAnswers,Slot=2,TagOptions),"")` |
| dcIIQ2SelectedTags | Q2SelectedTags | `If(2<=varQuestionCount,Concat(cmbIIQ2Tags.SelectedItems,Value,Char(10)),"")` |
| dcIIQ3TagsSnapshot | Q3TagsSnapshot | `If(3<=varQuestionCount,LookUp(colAnswers,Slot=3,TagOptions),"")` |
| dcIIQ3SelectedTags | Q3SelectedTags | `If(3<=varQuestionCount,Concat(cmbIIQ3Tags.SelectedItems,Value,Char(10)),"")` |
| dcIIQ4TagsSnapshot | Q4TagsSnapshot | `If(4<=varQuestionCount,LookUp(colAnswers,Slot=4,TagOptions),"")` |
| dcIIQ4SelectedTags | Q4SelectedTags | `If(4<=varQuestionCount,Concat(cmbIIQ4Tags.SelectedItems,Value,Char(10)),"")` |
| dcIIQ5TagsSnapshot | Q5TagsSnapshot | `If(5<=varQuestionCount,LookUp(colAnswers,Slot=5,TagOptions),"")` |
| dcIIQ5SelectedTags | Q5SelectedTags | `If(5<=varQuestionCount,Concat(cmbIIQ5Tags.SelectedItems,Value,Char(10)),"")` |
| dcIIQ6TagsSnapshot | Q6TagsSnapshot | `If(6<=varQuestionCount,LookUp(colAnswers,Slot=6,TagOptions),"")` |
| dcIIQ6SelectedTags | Q6SelectedTags | `If(6<=varQuestionCount,Concat(cmbIIQ6Tags.SelectedItems,Value,Char(10)),"")` |

#### cmbIIQ1Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=1,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=1,SelectedTags),""),Char(10)).Value)` |
| Visible | `1<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=1,TagOptions)))` |
| Y | `lblIIQ1Heading.Y+lblIIQ1Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIIQ1Response.DisplayMode)` |
| lblIIQ1Prompt.Y | `If(cmbIIQ1Tags.Visible,cmbIIQ1Tags.Y+cmbIIQ1Tags.Height+8,lblIIQ1Heading.Y+lblIIQ1Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=1),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordII.Q1TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordII.Q1SelectedTags,"")` to slot 1's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIIQ2Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=2,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=2,SelectedTags),""),Char(10)).Value)` |
| Visible | `2<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=2,TagOptions)))` |
| Y | `lblIIQ2Heading.Y+lblIIQ2Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIIQ2Response.DisplayMode)` |
| lblIIQ2Prompt.Y | `If(cmbIIQ2Tags.Visible,cmbIIQ2Tags.Y+cmbIIQ2Tags.Height+8,lblIIQ2Heading.Y+lblIIQ2Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=2),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordII.Q2TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordII.Q2SelectedTags,"")` to slot 2's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIIQ3Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=3,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=3,SelectedTags),""),Char(10)).Value)` |
| Visible | `3<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=3,TagOptions)))` |
| Y | `lblIIQ3Heading.Y+lblIIQ3Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIIQ3Response.DisplayMode)` |
| lblIIQ3Prompt.Y | `If(cmbIIQ3Tags.Visible,cmbIIQ3Tags.Y+cmbIIQ3Tags.Height+8,lblIIQ3Heading.Y+lblIIQ3Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=3),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordII.Q3TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordII.Q3SelectedTags,"")` to slot 3's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIIQ4Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=4,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=4,SelectedTags),""),Char(10)).Value)` |
| Visible | `4<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=4,TagOptions)))` |
| Y | `lblIIQ4Heading.Y+lblIIQ4Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIIQ4Response.DisplayMode)` |
| lblIIQ4Prompt.Y | `If(cmbIIQ4Tags.Visible,cmbIIQ4Tags.Y+cmbIIQ4Tags.Height+8,lblIIQ4Heading.Y+lblIIQ4Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=4),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordII.Q4TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordII.Q4SelectedTags,"")` to slot 4's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIIQ5Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=5,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=5,SelectedTags),""),Char(10)).Value)` |
| Visible | `5<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=5,TagOptions)))` |
| Y | `lblIIQ5Heading.Y+lblIIQ5Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIIQ5Response.DisplayMode)` |
| lblIIQ5Prompt.Y | `If(cmbIIQ5Tags.Visible,cmbIIQ5Tags.Y+cmbIIQ5Tags.Height+8,lblIIQ5Heading.Y+lblIIQ5Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=5),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordII.Q5TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordII.Q5SelectedTags,"")` to slot 5's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIIQ6Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=6,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=6,SelectedTags),""),Char(10)).Value)` |
| Visible | `6<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=6,TagOptions)))` |
| Y | `lblIIQ6Heading.Y+lblIIQ6Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIIQ6Response.DisplayMode)` |
| lblIIQ6Prompt.Y | `If(cmbIIQ6Tags.Visible,cmbIIQ6Tags.Y+cmbIIQ6Tags.Height+8,lblIIQ6Heading.Y+lblIIQ6Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=6),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordII.Q6TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordII.Q6SelectedTags,"")` to slot 6's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


### scrMDAward / frmMDAward

| New hidden card | DataField | Update |
|---|---|---|
| dcICQ1TagsSnapshot | Q1TagsSnapshot | `If(1<=varQuestionCount,LookUp(colAnswers,Slot=1,TagOptions),"")` |
| dcICQ1SelectedTags | Q1SelectedTags | `If(1<=varQuestionCount,Concat(cmbICQ1Tags.SelectedItems,Value,Char(10)),"")` |
| dcICQ2TagsSnapshot | Q2TagsSnapshot | `If(2<=varQuestionCount,LookUp(colAnswers,Slot=2,TagOptions),"")` |
| dcICQ2SelectedTags | Q2SelectedTags | `If(2<=varQuestionCount,Concat(cmbICQ2Tags.SelectedItems,Value,Char(10)),"")` |
| dcICQ3TagsSnapshot | Q3TagsSnapshot | `If(3<=varQuestionCount,LookUp(colAnswers,Slot=3,TagOptions),"")` |
| dcICQ3SelectedTags | Q3SelectedTags | `If(3<=varQuestionCount,Concat(cmbICQ3Tags.SelectedItems,Value,Char(10)),"")` |
| dcICQ4TagsSnapshot | Q4TagsSnapshot | `If(4<=varQuestionCount,LookUp(colAnswers,Slot=4,TagOptions),"")` |
| dcICQ4SelectedTags | Q4SelectedTags | `If(4<=varQuestionCount,Concat(cmbICQ4Tags.SelectedItems,Value,Char(10)),"")` |
| dcICQ5TagsSnapshot | Q5TagsSnapshot | `If(5<=varQuestionCount,LookUp(colAnswers,Slot=5,TagOptions),"")` |
| dcICQ5SelectedTags | Q5SelectedTags | `If(5<=varQuestionCount,Concat(cmbICQ5Tags.SelectedItems,Value,Char(10)),"")` |
| dcICQ6TagsSnapshot | Q6TagsSnapshot | `If(6<=varQuestionCount,LookUp(colAnswers,Slot=6,TagOptions),"")` |
| dcICQ6SelectedTags | Q6SelectedTags | `If(6<=varQuestionCount,Concat(cmbICQ6Tags.SelectedItems,Value,Char(10)),"")` |

#### cmbICQ1Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=1,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=1,SelectedTags),""),Char(10)).Value)` |
| Visible | `1<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=1,TagOptions)))` |
| Y | `lblICQ1Heading.Y+lblICQ1Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcICQ1Response.DisplayMode)` |
| lblICQ1Prompt.Y | `If(cmbICQ1Tags.Visible,cmbICQ1Tags.Y+cmbICQ1Tags.Height+8,lblICQ1Heading.Y+lblICQ1Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=1),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIC.Q1TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIC.Q1SelectedTags,"")` to slot 1's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbICQ2Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=2,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=2,SelectedTags),""),Char(10)).Value)` |
| Visible | `2<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=2,TagOptions)))` |
| Y | `lblICQ2Heading.Y+lblICQ2Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcICQ2Response.DisplayMode)` |
| lblICQ2Prompt.Y | `If(cmbICQ2Tags.Visible,cmbICQ2Tags.Y+cmbICQ2Tags.Height+8,lblICQ2Heading.Y+lblICQ2Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=2),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIC.Q2TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIC.Q2SelectedTags,"")` to slot 2's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbICQ3Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=3,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=3,SelectedTags),""),Char(10)).Value)` |
| Visible | `3<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=3,TagOptions)))` |
| Y | `lblICQ3Heading.Y+lblICQ3Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcICQ3Response.DisplayMode)` |
| lblICQ3Prompt.Y | `If(cmbICQ3Tags.Visible,cmbICQ3Tags.Y+cmbICQ3Tags.Height+8,lblICQ3Heading.Y+lblICQ3Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=3),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIC.Q3TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIC.Q3SelectedTags,"")` to slot 3's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbICQ4Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=4,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=4,SelectedTags),""),Char(10)).Value)` |
| Visible | `4<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=4,TagOptions)))` |
| Y | `lblICQ4Heading.Y+lblICQ4Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcICQ4Response.DisplayMode)` |
| lblICQ4Prompt.Y | `If(cmbICQ4Tags.Visible,cmbICQ4Tags.Y+cmbICQ4Tags.Height+8,lblICQ4Heading.Y+lblICQ4Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=4),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIC.Q4TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIC.Q4SelectedTags,"")` to slot 4's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbICQ5Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=5,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=5,SelectedTags),""),Char(10)).Value)` |
| Visible | `5<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=5,TagOptions)))` |
| Y | `lblICQ5Heading.Y+lblICQ5Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcICQ5Response.DisplayMode)` |
| lblICQ5Prompt.Y | `If(cmbICQ5Tags.Visible,cmbICQ5Tags.Y+cmbICQ5Tags.Height+8,lblICQ5Heading.Y+lblICQ5Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=5),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIC.Q5TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIC.Q5SelectedTags,"")` to slot 5's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbICQ6Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=6,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=6,SelectedTags),""),Char(10)).Value)` |
| Visible | `6<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=6,TagOptions)))` |
| Y | `lblICQ6Heading.Y+lblICQ6Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcICQ6Response.DisplayMode)` |
| lblICQ6Prompt.Y | `If(cmbICQ6Tags.Visible,cmbICQ6Tags.Y+cmbICQ6Tags.Height+8,lblICQ6Heading.Y+lblICQ6Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=6),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIC.Q6TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIC.Q6SelectedTags,"")` to slot 6's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


### scrTrendMarcherAward / frmTrendMarcherAward

| New hidden card | DataField | Update |
|---|---|---|
| dcIEQ1TagsSnapshot | Q1TagsSnapshot | `If(1<=varQuestionCount,LookUp(colAnswers,Slot=1,TagOptions),"")` |
| dcIEQ1SelectedTags | Q1SelectedTags | `If(1<=varQuestionCount,Concat(cmbIEQ1Tags.SelectedItems,Value,Char(10)),"")` |
| dcIEQ2TagsSnapshot | Q2TagsSnapshot | `If(2<=varQuestionCount,LookUp(colAnswers,Slot=2,TagOptions),"")` |
| dcIEQ2SelectedTags | Q2SelectedTags | `If(2<=varQuestionCount,Concat(cmbIEQ2Tags.SelectedItems,Value,Char(10)),"")` |
| dcIEQ3TagsSnapshot | Q3TagsSnapshot | `If(3<=varQuestionCount,LookUp(colAnswers,Slot=3,TagOptions),"")` |
| dcIEQ3SelectedTags | Q3SelectedTags | `If(3<=varQuestionCount,Concat(cmbIEQ3Tags.SelectedItems,Value,Char(10)),"")` |
| dcIEQ4TagsSnapshot | Q4TagsSnapshot | `If(4<=varQuestionCount,LookUp(colAnswers,Slot=4,TagOptions),"")` |
| dcIEQ4SelectedTags | Q4SelectedTags | `If(4<=varQuestionCount,Concat(cmbIEQ4Tags.SelectedItems,Value,Char(10)),"")` |
| dcIEQ5TagsSnapshot | Q5TagsSnapshot | `If(5<=varQuestionCount,LookUp(colAnswers,Slot=5,TagOptions),"")` |
| dcIEQ5SelectedTags | Q5SelectedTags | `If(5<=varQuestionCount,Concat(cmbIEQ5Tags.SelectedItems,Value,Char(10)),"")` |
| dcIEQ6TagsSnapshot | Q6TagsSnapshot | `If(6<=varQuestionCount,LookUp(colAnswers,Slot=6,TagOptions),"")` |
| dcIEQ6SelectedTags | Q6SelectedTags | `If(6<=varQuestionCount,Concat(cmbIEQ6Tags.SelectedItems,Value,Char(10)),"")` |

#### cmbIEQ1Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=1,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=1,SelectedTags),""),Char(10)).Value)` |
| Visible | `1<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=1,TagOptions)))` |
| Y | `lblIEQ1Heading.Y+lblIEQ1Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIEQ1Response.DisplayMode)` |
| lblIEQ1Prompt.Y | `If(cmbIEQ1Tags.Visible,cmbIEQ1Tags.Y+cmbIEQ1Tags.Height+8,lblIEQ1Heading.Y+lblIEQ1Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=1),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIE.Q1TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIE.Q1SelectedTags,"")` to slot 1's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIEQ2Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=2,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=2,SelectedTags),""),Char(10)).Value)` |
| Visible | `2<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=2,TagOptions)))` |
| Y | `lblIEQ2Heading.Y+lblIEQ2Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIEQ2Response.DisplayMode)` |
| lblIEQ2Prompt.Y | `If(cmbIEQ2Tags.Visible,cmbIEQ2Tags.Y+cmbIEQ2Tags.Height+8,lblIEQ2Heading.Y+lblIEQ2Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=2),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIE.Q2TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIE.Q2SelectedTags,"")` to slot 2's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIEQ3Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=3,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=3,SelectedTags),""),Char(10)).Value)` |
| Visible | `3<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=3,TagOptions)))` |
| Y | `lblIEQ3Heading.Y+lblIEQ3Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIEQ3Response.DisplayMode)` |
| lblIEQ3Prompt.Y | `If(cmbIEQ3Tags.Visible,cmbIEQ3Tags.Y+cmbIEQ3Tags.Height+8,lblIEQ3Heading.Y+lblIEQ3Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=3),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIE.Q3TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIE.Q3SelectedTags,"")` to slot 3's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIEQ4Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=4,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=4,SelectedTags),""),Char(10)).Value)` |
| Visible | `4<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=4,TagOptions)))` |
| Y | `lblIEQ4Heading.Y+lblIEQ4Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIEQ4Response.DisplayMode)` |
| lblIEQ4Prompt.Y | `If(cmbIEQ4Tags.Visible,cmbIEQ4Tags.Y+cmbIEQ4Tags.Height+8,lblIEQ4Heading.Y+lblIEQ4Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=4),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIE.Q4TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIE.Q4SelectedTags,"")` to slot 4's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIEQ5Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=5,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=5,SelectedTags),""),Char(10)).Value)` |
| Visible | `5<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=5,TagOptions)))` |
| Y | `lblIEQ5Heading.Y+lblIEQ5Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIEQ5Response.DisplayMode)` |
| lblIEQ5Prompt.Y | `If(cmbIEQ5Tags.Visible,cmbIEQ5Tags.Y+cmbIEQ5Tags.Height+8,lblIEQ5Heading.Y+lblIEQ5Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=5),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIE.Q5TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIE.Q5SelectedTags,"")` to slot 5's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbIEQ6Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=6,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=6,SelectedTags),""),Char(10)).Value)` |
| Visible | `6<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=6,TagOptions)))` |
| Y | `lblIEQ6Heading.Y+lblIEQ6Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcIEQ6Response.DisplayMode)` |
| lblIEQ6Prompt.Y | `If(cmbIEQ6Tags.Visible,cmbIEQ6Tags.Y+cmbIEQ6Tags.Height+8,lblIEQ6Heading.Y+lblIEQ6Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=6),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordIE.Q6TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordIE.Q6SelectedTags,"")` to slot 6's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


### scrBestInnovatorTeam / frmBestInnovatorTeam

| New hidden card | DataField | Update |
|---|---|---|
| dcTCQ1TagsSnapshot | Q1TagsSnapshot | `If(1<=varQuestionCount,LookUp(colAnswers,Slot=1,TagOptions),"")` |
| dcTCQ1SelectedTags | Q1SelectedTags | `If(1<=varQuestionCount,Concat(cmbTCQ1Tags.SelectedItems,Value,Char(10)),"")` |
| dcTCQ2TagsSnapshot | Q2TagsSnapshot | `If(2<=varQuestionCount,LookUp(colAnswers,Slot=2,TagOptions),"")` |
| dcTCQ2SelectedTags | Q2SelectedTags | `If(2<=varQuestionCount,Concat(cmbTCQ2Tags.SelectedItems,Value,Char(10)),"")` |
| dcTCQ3TagsSnapshot | Q3TagsSnapshot | `If(3<=varQuestionCount,LookUp(colAnswers,Slot=3,TagOptions),"")` |
| dcTCQ3SelectedTags | Q3SelectedTags | `If(3<=varQuestionCount,Concat(cmbTCQ3Tags.SelectedItems,Value,Char(10)),"")` |
| dcTCQ4TagsSnapshot | Q4TagsSnapshot | `If(4<=varQuestionCount,LookUp(colAnswers,Slot=4,TagOptions),"")` |
| dcTCQ4SelectedTags | Q4SelectedTags | `If(4<=varQuestionCount,Concat(cmbTCQ4Tags.SelectedItems,Value,Char(10)),"")` |
| dcTCQ5TagsSnapshot | Q5TagsSnapshot | `If(5<=varQuestionCount,LookUp(colAnswers,Slot=5,TagOptions),"")` |
| dcTCQ5SelectedTags | Q5SelectedTags | `If(5<=varQuestionCount,Concat(cmbTCQ5Tags.SelectedItems,Value,Char(10)),"")` |
| dcTCQ6TagsSnapshot | Q6TagsSnapshot | `If(6<=varQuestionCount,LookUp(colAnswers,Slot=6,TagOptions),"")` |
| dcTCQ6SelectedTags | Q6SelectedTags | `If(6<=varQuestionCount,Concat(cmbTCQ6Tags.SelectedItems,Value,Char(10)),"")` |

#### cmbTCQ1Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=1,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=1,SelectedTags),""),Char(10)).Value)` |
| Visible | `1<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=1,TagOptions)))` |
| Y | `lblTCQ1Heading.Y+lblTCQ1Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTCQ1Response.DisplayMode)` |
| lblTCQ1Prompt.Y | `If(cmbTCQ1Tags.Visible,cmbTCQ1Tags.Y+cmbTCQ1Tags.Height+8,lblTCQ1Heading.Y+lblTCQ1Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=1),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTC.Q1TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTC.Q1SelectedTags,"")` to slot 1's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTCQ2Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=2,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=2,SelectedTags),""),Char(10)).Value)` |
| Visible | `2<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=2,TagOptions)))` |
| Y | `lblTCQ2Heading.Y+lblTCQ2Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTCQ2Response.DisplayMode)` |
| lblTCQ2Prompt.Y | `If(cmbTCQ2Tags.Visible,cmbTCQ2Tags.Y+cmbTCQ2Tags.Height+8,lblTCQ2Heading.Y+lblTCQ2Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=2),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTC.Q2TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTC.Q2SelectedTags,"")` to slot 2's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTCQ3Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=3,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=3,SelectedTags),""),Char(10)).Value)` |
| Visible | `3<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=3,TagOptions)))` |
| Y | `lblTCQ3Heading.Y+lblTCQ3Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTCQ3Response.DisplayMode)` |
| lblTCQ3Prompt.Y | `If(cmbTCQ3Tags.Visible,cmbTCQ3Tags.Y+cmbTCQ3Tags.Height+8,lblTCQ3Heading.Y+lblTCQ3Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=3),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTC.Q3TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTC.Q3SelectedTags,"")` to slot 3's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTCQ4Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=4,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=4,SelectedTags),""),Char(10)).Value)` |
| Visible | `4<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=4,TagOptions)))` |
| Y | `lblTCQ4Heading.Y+lblTCQ4Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTCQ4Response.DisplayMode)` |
| lblTCQ4Prompt.Y | `If(cmbTCQ4Tags.Visible,cmbTCQ4Tags.Y+cmbTCQ4Tags.Height+8,lblTCQ4Heading.Y+lblTCQ4Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=4),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTC.Q4TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTC.Q4SelectedTags,"")` to slot 4's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTCQ5Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=5,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=5,SelectedTags),""),Char(10)).Value)` |
| Visible | `5<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=5,TagOptions)))` |
| Y | `lblTCQ5Heading.Y+lblTCQ5Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTCQ5Response.DisplayMode)` |
| lblTCQ5Prompt.Y | `If(cmbTCQ5Tags.Visible,cmbTCQ5Tags.Y+cmbTCQ5Tags.Height+8,lblTCQ5Heading.Y+lblTCQ5Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=5),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTC.Q5TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTC.Q5SelectedTags,"")` to slot 5's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTCQ6Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=6,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=6,SelectedTags),""),Char(10)).Value)` |
| Visible | `6<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=6,TagOptions)))` |
| Y | `lblTCQ6Heading.Y+lblTCQ6Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTCQ6Response.DisplayMode)` |
| lblTCQ6Prompt.Y | `If(cmbTCQ6Tags.Visible,cmbTCQ6Tags.Y+cmbTCQ6Tags.Height+8,lblTCQ6Heading.Y+lblTCQ6Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=6),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTC.Q6TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTC.Q6SelectedTags,"")` to slot 6's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


### scrMDAwardTeam / frmMDAwardTeam

| New hidden card | DataField | Update |
|---|---|---|
| dcTIQ1TagsSnapshot | Q1TagsSnapshot | `If(1<=varQuestionCount,LookUp(colAnswers,Slot=1,TagOptions),"")` |
| dcTIQ1SelectedTags | Q1SelectedTags | `If(1<=varQuestionCount,Concat(cmbTIQ1Tags.SelectedItems,Value,Char(10)),"")` |
| dcTIQ2TagsSnapshot | Q2TagsSnapshot | `If(2<=varQuestionCount,LookUp(colAnswers,Slot=2,TagOptions),"")` |
| dcTIQ2SelectedTags | Q2SelectedTags | `If(2<=varQuestionCount,Concat(cmbTIQ2Tags.SelectedItems,Value,Char(10)),"")` |
| dcTIQ3TagsSnapshot | Q3TagsSnapshot | `If(3<=varQuestionCount,LookUp(colAnswers,Slot=3,TagOptions),"")` |
| dcTIQ3SelectedTags | Q3SelectedTags | `If(3<=varQuestionCount,Concat(cmbTIQ3Tags.SelectedItems,Value,Char(10)),"")` |
| dcTIQ4TagsSnapshot | Q4TagsSnapshot | `If(4<=varQuestionCount,LookUp(colAnswers,Slot=4,TagOptions),"")` |
| dcTIQ4SelectedTags | Q4SelectedTags | `If(4<=varQuestionCount,Concat(cmbTIQ4Tags.SelectedItems,Value,Char(10)),"")` |
| dcTIQ5TagsSnapshot | Q5TagsSnapshot | `If(5<=varQuestionCount,LookUp(colAnswers,Slot=5,TagOptions),"")` |
| dcTIQ5SelectedTags | Q5SelectedTags | `If(5<=varQuestionCount,Concat(cmbTIQ5Tags.SelectedItems,Value,Char(10)),"")` |
| dcTIQ6TagsSnapshot | Q6TagsSnapshot | `If(6<=varQuestionCount,LookUp(colAnswers,Slot=6,TagOptions),"")` |
| dcTIQ6SelectedTags | Q6SelectedTags | `If(6<=varQuestionCount,Concat(cmbTIQ6Tags.SelectedItems,Value,Char(10)),"")` |

#### cmbTIQ1Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=1,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=1,SelectedTags),""),Char(10)).Value)` |
| Visible | `1<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=1,TagOptions)))` |
| Y | `lblTIQ1Heading.Y+lblTIQ1Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTIQ1Response.DisplayMode)` |
| lblTIQ1Prompt.Y | `If(cmbTIQ1Tags.Visible,cmbTIQ1Tags.Y+cmbTIQ1Tags.Height+8,lblTIQ1Heading.Y+lblTIQ1Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=1),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTI.Q1TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTI.Q1SelectedTags,"")` to slot 1's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTIQ2Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=2,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=2,SelectedTags),""),Char(10)).Value)` |
| Visible | `2<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=2,TagOptions)))` |
| Y | `lblTIQ2Heading.Y+lblTIQ2Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTIQ2Response.DisplayMode)` |
| lblTIQ2Prompt.Y | `If(cmbTIQ2Tags.Visible,cmbTIQ2Tags.Y+cmbTIQ2Tags.Height+8,lblTIQ2Heading.Y+lblTIQ2Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=2),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTI.Q2TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTI.Q2SelectedTags,"")` to slot 2's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTIQ3Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=3,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=3,SelectedTags),""),Char(10)).Value)` |
| Visible | `3<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=3,TagOptions)))` |
| Y | `lblTIQ3Heading.Y+lblTIQ3Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTIQ3Response.DisplayMode)` |
| lblTIQ3Prompt.Y | `If(cmbTIQ3Tags.Visible,cmbTIQ3Tags.Y+cmbTIQ3Tags.Height+8,lblTIQ3Heading.Y+lblTIQ3Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=3),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTI.Q3TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTI.Q3SelectedTags,"")` to slot 3's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTIQ4Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=4,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=4,SelectedTags),""),Char(10)).Value)` |
| Visible | `4<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=4,TagOptions)))` |
| Y | `lblTIQ4Heading.Y+lblTIQ4Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTIQ4Response.DisplayMode)` |
| lblTIQ4Prompt.Y | `If(cmbTIQ4Tags.Visible,cmbTIQ4Tags.Y+cmbTIQ4Tags.Height+8,lblTIQ4Heading.Y+lblTIQ4Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=4),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTI.Q4TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTI.Q4SelectedTags,"")` to slot 4's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTIQ5Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=5,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=5,SelectedTags),""),Char(10)).Value)` |
| Visible | `5<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=5,TagOptions)))` |
| Y | `lblTIQ5Heading.Y+lblTIQ5Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTIQ5Response.DisplayMode)` |
| lblTIQ5Prompt.Y | `If(cmbTIQ5Tags.Visible,cmbTIQ5Tags.Y+cmbTIQ5Tags.Height+8,lblTIQ5Heading.Y+lblTIQ5Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=5),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTI.Q5TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTI.Q5SelectedTags,"")` to slot 5's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTIQ6Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=6,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=6,SelectedTags),""),Char(10)).Value)` |
| Visible | `6<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=6,TagOptions)))` |
| Y | `lblTIQ6Heading.Y+lblTIQ6Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTIQ6Response.DisplayMode)` |
| lblTIQ6Prompt.Y | `If(cmbTIQ6Tags.Visible,cmbTIQ6Tags.Y+cmbTIQ6Tags.Height+8,lblTIQ6Heading.Y+lblTIQ6Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=6),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTI.Q6TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTI.Q6SelectedTags,"")` to slot 6's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


### scrSpecialTeamAward / frmSpecialTeamAward

| New hidden card | DataField | Update |
|---|---|---|
| dcTTQ1TagsSnapshot | Q1TagsSnapshot | `If(1<=varQuestionCount,LookUp(colAnswers,Slot=1,TagOptions),"")` |
| dcTTQ1SelectedTags | Q1SelectedTags | `If(1<=varQuestionCount,Concat(cmbTTQ1Tags.SelectedItems,Value,Char(10)),"")` |
| dcTTQ2TagsSnapshot | Q2TagsSnapshot | `If(2<=varQuestionCount,LookUp(colAnswers,Slot=2,TagOptions),"")` |
| dcTTQ2SelectedTags | Q2SelectedTags | `If(2<=varQuestionCount,Concat(cmbTTQ2Tags.SelectedItems,Value,Char(10)),"")` |
| dcTTQ3TagsSnapshot | Q3TagsSnapshot | `If(3<=varQuestionCount,LookUp(colAnswers,Slot=3,TagOptions),"")` |
| dcTTQ3SelectedTags | Q3SelectedTags | `If(3<=varQuestionCount,Concat(cmbTTQ3Tags.SelectedItems,Value,Char(10)),"")` |
| dcTTQ4TagsSnapshot | Q4TagsSnapshot | `If(4<=varQuestionCount,LookUp(colAnswers,Slot=4,TagOptions),"")` |
| dcTTQ4SelectedTags | Q4SelectedTags | `If(4<=varQuestionCount,Concat(cmbTTQ4Tags.SelectedItems,Value,Char(10)),"")` |
| dcTTQ5TagsSnapshot | Q5TagsSnapshot | `If(5<=varQuestionCount,LookUp(colAnswers,Slot=5,TagOptions),"")` |
| dcTTQ5SelectedTags | Q5SelectedTags | `If(5<=varQuestionCount,Concat(cmbTTQ5Tags.SelectedItems,Value,Char(10)),"")` |
| dcTTQ6TagsSnapshot | Q6TagsSnapshot | `If(6<=varQuestionCount,LookUp(colAnswers,Slot=6,TagOptions),"")` |
| dcTTQ6SelectedTags | Q6SelectedTags | `If(6<=varQuestionCount,Concat(cmbTTQ6Tags.SelectedItems,Value,Char(10)),"")` |

#### cmbTTQ1Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=1,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=1,SelectedTags),""),Char(10)).Value)` |
| Visible | `1<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=1,TagOptions)))` |
| Y | `lblTTQ1Heading.Y+lblTTQ1Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTTQ1Response.DisplayMode)` |
| lblTTQ1Prompt.Y | `If(cmbTTQ1Tags.Visible,cmbTTQ1Tags.Y+cmbTTQ1Tags.Height+8,lblTTQ1Heading.Y+lblTTQ1Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=1),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTT.Q1TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTT.Q1SelectedTags,"")` to slot 1's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTTQ2Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=2,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=2,SelectedTags),""),Char(10)).Value)` |
| Visible | `2<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=2,TagOptions)))` |
| Y | `lblTTQ2Heading.Y+lblTTQ2Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTTQ2Response.DisplayMode)` |
| lblTTQ2Prompt.Y | `If(cmbTTQ2Tags.Visible,cmbTTQ2Tags.Y+cmbTTQ2Tags.Height+8,lblTTQ2Heading.Y+lblTTQ2Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=2),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTT.Q2TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTT.Q2SelectedTags,"")` to slot 2's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTTQ3Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=3,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=3,SelectedTags),""),Char(10)).Value)` |
| Visible | `3<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=3,TagOptions)))` |
| Y | `lblTTQ3Heading.Y+lblTTQ3Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTTQ3Response.DisplayMode)` |
| lblTTQ3Prompt.Y | `If(cmbTTQ3Tags.Visible,cmbTTQ3Tags.Y+cmbTTQ3Tags.Height+8,lblTTQ3Heading.Y+lblTTQ3Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=3),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTT.Q3TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTT.Q3SelectedTags,"")` to slot 3's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTTQ4Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=4,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=4,SelectedTags),""),Char(10)).Value)` |
| Visible | `4<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=4,TagOptions)))` |
| Y | `lblTTQ4Heading.Y+lblTTQ4Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTTQ4Response.DisplayMode)` |
| lblTTQ4Prompt.Y | `If(cmbTTQ4Tags.Visible,cmbTTQ4Tags.Y+cmbTTQ4Tags.Height+8,lblTTQ4Heading.Y+lblTTQ4Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=4),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTT.Q4TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTT.Q4SelectedTags,"")` to slot 4's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTTQ5Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=5,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=5,SelectedTags),""),Char(10)).Value)` |
| Visible | `5<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=5,TagOptions)))` |
| Y | `lblTTQ5Heading.Y+lblTTQ5Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTTQ5Response.DisplayMode)` |
| lblTTQ5Prompt.Y | `If(cmbTTQ5Tags.Visible,cmbTTQ5Tags.Y+cmbTTQ5Tags.Height+8,lblTTQ5Heading.Y+lblTTQ5Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=5),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTT.Q5TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTT.Q5SelectedTags,"")` to slot 5's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


#### cmbTTQ6Tags

| Property | Formula |
|---|---|
| Items | `ForAll(Filter(Split(Substitute(Coalesce(LookUp(colAnswers,Slot=6,TagOptions),""),Char(13),""),Char(10)),!IsBlank(Trim(Value))),{Value:Trim(Value)})` |
| DefaultSelectedItems | `Filter(Self.Items,Value in Split(Coalesce(LookUp(colAnswers,Slot=6,SelectedTags),""),Char(10)).Value)` |
| Visible | `6<=varQuestionCount && !IsBlank(Trim(LookUp(colAnswers,Slot=6,TagOptions)))` |
| Y | `lblTTQ6Heading.Y+lblTTQ6Heading.Height+8` |
| DisplayMode | `If(varIsBusy,DisplayMode.Disabled,dcTTQ6Response.DisplayMode)` |
| lblTTQ6Prompt.Y | `If(cmbTTQ6Tags.Visible,cmbTTQ6Tags.Y+cmbTTQ6Tags.Height+8,lblTTQ6Heading.Y+lblTTQ6Heading.Height+8)` |

OnChange:

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=6),
    {SelectedTags:Concat(Self.SelectedItems,Value,Char(10))});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

In the matching saved-record open handler, add `TagOptions:Coalesce(varRecordTT.Q6TagsSnapshot,"")` and `SelectedTags:Coalesce(varRecordTT.Q6SelectedTags,"")` to slot 6's record. Retain its other fields. Do not retrieve current AwardQuestions.Tags when reopening an old nomination.


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
