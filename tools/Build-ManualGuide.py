"""Generate the six explicit manual Canvas recipes; does not contact Power Apps."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'documentation' / 'manual-build'
OUT.mkdir(parents=True, exist_ok=True)
ROWS = [
    ('IND_INNOVATION', 'II', 'IndividualInnovation', False),
    ('IND_CUSTOMER', 'IC', 'IndividualCustomer', False),
    ('IND_EXCELLENCE', 'IE', 'IndividualExcellence', False),
    ('TEAM_COLLAB', 'TC', 'TeamCollaboration', True),
    ('TEAM_IMPACT', 'TI', 'TeamImpact', True),
    ('TEAM_TRANSFORM', 'TT', 'TeamTransformation', True),
]
SOURCE_IDS = {code: f'Nom_{suffix}' for code, prefix, suffix, team in ROWS}

def write(name, content):
    (OUT / name).write_text(content.strip() + '\n', encoding='utf-8')

def expand(template, row):
    code, prefix, suffix, team = row
    for key, value in {'CODE': code, 'P': prefix, 'SUFFIX': suffix,
                       'DS': SOURCE_IDS[code], 'TYPE': 'Team' if team else 'Individual'}.items():
        template = template.replace('@' + key + '@', value)
    return template

def route():
    return 'Switch(varCategory.CategoryCode,\n' + ',\n'.join(
        f'    "{c}", Navigate(scr{s}, ScreenTransition.None)' for c, p, s, t in ROWS
    ) + ',\n    Notify("This category has no configured form.", NotificationType.Error)\n)'

def snapshots(prefix, record=False):
    return 'Table(\n' + ',\n'.join(
        (f'    {{Slot: {n}, Prompt: Coalesce(varRecord{prefix}.Q{n}PromptSnapshot, ""), '
         f'Required: Coalesce(varRecord{prefix}.Q{n}RequiredSnapshot, false), '
         f'Response: Coalesce(varRecord{prefix}.Q{n}Response, "")}}') if record else
        (f'    {{Slot: {n}, Prompt: LookUp(colAnswers, Slot = {n}, Prompt), '
         f'Required: LookUp(colAnswers, Slot = {n}, Required), '
         f'Response: txt{prefix}Q{n}.Text}}')
        for n in range(1, 7)
    ) + '\n)'

PREFLIGHT = '''Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(@DS@);
        Set(varLatest@P@, LookUp(@DS@, ID = varNominationId));
        If(IsBlank(varLatest@P@.ID) ||
           varLatest@P@.NominationStatus.Value <> "Draft" ||
           varLatest@P@.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "@INTENT@");
    SubmitForm(frm@SUFFIX@),
    Set(varIsBusy, false)
)'''

ON_SUCCESS = '''Set(varRecord@P@, frm@SUFFIX@.LastSubmit);
Set(varNominationId, varRecord@P@.ID);
Set(varLoadedModified, varRecord@P@.Modified);
EditForm(frm@SUFFIX@);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecord@P@,
            Patch(@DS@, varRecord@P@,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecord@P@.Modified);
        Set(varSubmittedOn, varRecord@P@.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frm@SUFFIX@);
        Navigate(scrConfirmation, ScreenTransition.None);
        true,
        Set(varIsBusy, false);
        Set(varSubmissionComplete, false);
        Set(varSaveIntent, "Draft");
        Notify("Your draft save succeeded, but submission was not confirmed. Check My nominations before retrying. Your existing item ID is retained.", NotificationType.Error);
        false
    ),
    Set(varIsBusy, false);
    Notify("Draft saved. Reference: " & varCategory.CategoryCode & "-" & Text(varNominationId, "000000"), NotificationType.Success)
)'''

OPEN = '''If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(@DS@);
        Set(varRecord@P@, LookUp(@DS@, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecord@P@.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecord@P@.ID) || varCategory.CategoryCode <> "@CODE@" ||
       IsBlank(varRecord@P@.QuestionSetVersion) || varRecord@P@.QuestionSetVersion < 1 ||
       IsBlank(varRecord@P@.QuestionCount) || varRecord@P@.QuestionCount < 3 || varRecord@P@.QuestionCount > 6 ||
       varRecord@P@.QuestionCount <> RoundDown(varRecord@P@.QuestionCount,0) ||
       IsBlank(varRecord@P@.Q1PromptSnapshot) || IsBlank(varRecord@P@.Q2PromptSnapshot) || IsBlank(varRecord@P@.Q3PromptSnapshot) ||
       (varRecord@P@.QuestionCount>=4 && IsBlank(varRecord@P@.Q4PromptSnapshot)) ||
       (varRecord@P@.QuestionCount>=5 && IsBlank(varRecord@P@.Q5PromptSnapshot)) ||
       (varRecord@P@.QuestionCount>=6 && IsBlank(varRecord@P@.Q6PromptSnapshot)) ||
       !(varRecord@P@.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "@TYPE@");
        Set(varNominationId, varRecord@P@.ID);
        Set(varLoadedModified, varRecord@P@.Modified);
        Set(varQuestionVersion, varRecord@P@.QuestionSetVersion);
        Set(varQuestionCount, varRecord@P@.QuestionCount);
        Set(varRole, Coalesce(varRecord@P@.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecord@P@.EmployeeLevel.Value, ""));
        Set(varNominator, varRecord@P@.NominatedBy);
        @IDENTITY@
        ClearCollect(colAnswers, @ANSWERS@);
        Set(varReadOnly, varRecord@P@.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecord@P@.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frm@SUFFIX@);
        If(varReadOnly, ViewForm(frm@SUFFIX@), EditForm(frm@SUFFIX@));
        Set(varIsBusy, false);
        Navigate(scr@SUFFIX@, ScreenTransition.None)
    )
)'''

submit_branches = []
mapping = ['| Code | Screen / form | Source | Prefix |', '|---|---|---|---|']
for row in ROWS:
    code, p, s, team = row
    ds = SOURCE_IDS[code]
    mapping.append(f'| `{code}` | `scr{s}` / `frm{s}` | `{ds}` | `{p}` |')
    update_rows = [
        ('Title', 'Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)'),
        ('Category', '{Id: varCategory.ID, Value: varCategory.Title}'),
        ('QuestionSetVersion', 'varQuestionVersion'), ('QuestionCount', 'varQuestionCount'),
        ('NominatedBy', 'varNominator'), ('NominatorEmail', 'varUserEmail'),
        ('EmployeeRole', 'Trim(varRole)'),
        ('EmployeeLevel', f'If(IsBlank(varLevel), Blank(), LookUp(Choices({ds}.EmployeeLevel), Value = varLevel))'),
        ('NominationStatus', '{Value: "Draft"}'), ('DeclarationAccepted', 'false'), ('SubmittedOn', 'Blank()'),
    ]
    if team:
        update_rows += [('TeamName', 'Trim(varTeamName)'),
                        ('TeamPrimaryContact', 'If(IsBlank(varPrimaryContact.Claims), Blank(), varPrimaryContact)'),
                        ('TeamMembers', 'colTeamMembers')]
        identity = '''Set(varTeamName, Coalesce(varRecord@P@.TeamName, ""));
        Set(varPrimaryContact, Coalesce(varRecord@P@.TeamPrimaryContact, varEmptyPerson));
        Set(varEmployee, varEmptyPerson);
        ClearCollect(colTeamMembers, varRecord@P@.TeamMembers);'''
    else:
        update_rows += [('NominatedEmployee', 'If(IsBlank(varEmployee.Claims), Blank(), varEmployee)')]
        identity = '''Set(varEmployee, Coalesce(varRecord@P@.NominatedEmployee, varEmptyPerson));
        Set(varPrimaryContact, varEmptyPerson);
        Set(varTeamName, "");
        Clear(colTeamMembers);'''
    for n in range(1, 7):
        update_rows += [(f'Q{n}PromptSnapshot', f'LookUp(colAnswers, Slot = {n}, Prompt)'),
                        (f'Q{n}RequiredSnapshot', f'LookUp(colAnswers, Slot = {n}, Required)'),
                        (f'Q{n}Response', f'If({n} <= varQuestionCount, txt{p}Q{n}.Text, "")')]
    updates = '| SharePoint DataField / card | Update formula |\n|---|---|\n' + '\n'.join(
        f'| `{field}` / `dc{p}{field}` | `{formula}` |' for field, formula in update_rows
    )
    updates += f'\n| Native Attachments / `dc{p}Attachments` | `att{p}.Attachments` |'

    capture = f'ClearCollect(colCapturedAnswers, {snapshots(p)});\nClearCollect(colAnswers, colCapturedAnswers);'
    review = capture + f'''
Set(varDetailsComplete, DetailsValid);
Set(varResponsesComplete, ResponsesValid);
If(!DetailsValid,
    Notify("Complete nominee details, role and level before review.", NotificationType.Warning);
    Navigate(scrNomineeDetails, ScreenTransition.None),
    !ResponsesValid,
    Notify("Complete every required response before review.", NotificationType.Warning),
    Set(varDeclarationAccepted, false);
    ClearCollect(colReviewFiles, ForAll(att{p}.Attachments As file, {{FileName: file.Name}}));
    Set(varCurrentStep, 4);
    Navigate(scrReview, ScreenTransition.None)
)'''
    save = expand(PREFLIGHT.replace('@INTENT@', 'Draft'), row)
    save = f'''If(!varIsBusy && !varReadOnly && varCategoryComplete,
    {capture}
    If(CountIf(colAnswers, Len(Response) > varMaxResponseLength) > 0,
        Notify("A response exceeds the configured limit.", NotificationType.Warning),
        {save}
    )
)'''
    submit_branches.append(f'    "{code}",\n' + expand(PREFLIGHT.replace('@INTENT@', 'Submit'), row))
    items = f'''SortByColumns(
    Filter({ds},
        NominatorEmail = varUserEmail,
        (varBrowseStatus = "All" || NominationStatus.Value = varBrowseStatus),
        (varBrowseId = 0 || ID = varBrowseId)
    ),
    "Modified", SortOrder.Descending
)'''
    open_formula = expand(OPEN.replace('@IDENTITY@', identity).replace('@ANSWERS@', snapshots(p, True)), row)
    text = f'''# {code} — complete typed form recipe

Read `README.md` and `01-Screens-and-Layout.md` first. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

## Controls to create

Screen `scr{s}`; Edit form `frm{s}`; saved-record variable `varRecord{p}`; latest-record variable `varLatest{p}`. Create six response text inputs `txt{p}Q1` … `txt{p}Q6` in the corresponding response cards, and keep native attachment input `att{p}` inside `dc{p}Attachments`.

Form DataSource = `{ds}`; Item = `varRecord{p}`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dc{p}Q1Response` … `dc{p}Q6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

## scr{s}.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

## All card Update properties

{updates}

All cards except Q1–Q6 Response and Attachments: Visible = `false`, Height = `0`, Required = `false`. Set form-card DisplayMode to `Parent.DisplayMode`. Set each child editor DisplayMode to its card's DisplayMode, and disable it while varIsBusy. Hidden metadata's Update properties still participate in SubmitForm.

Keep native attachment Items = `Parent.Default` when directly inside its data card, and retain the generated attachment DataField (often `"{{Attachments}}"`). Do not type a guessed DataField. Preserve the other generated attachment properties, including MaxAttachments/MaxAttachmentSize, until an approved policy is chosen. Appending files does not save them until SubmitForm completes.

## btn{p}SaveDraft.OnSelect

```powerfx
{save}
```

## btn{p}Review.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

```powerfx
{review}
```

`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

## frm{s}.OnSuccess

```powerfx
{expand(ON_SUCCESS, row)}
```

## frm{s}.OnFailure

```powerfx
Set(varIsBusy, false);
Set(varSubmissionComplete, false);
Set(varHasChanges, true);
Notify("Save was not confirmed. Your inputs are retained. If the connection timed out, check My nominations before retrying because the server may have saved the item.", NotificationType.Error)
```

## Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

```powerfx
{capture}
Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1);
Navigate(scrNomineeDetails, ScreenTransition.None)
```

## My nominations gallery galMine{p}

Visible = `varBrowseCode = "{code}"`. Items:

```powerfx
{items}
```

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.{'TeamName' if team else 'NominatedEmployee.DisplayName'}` in native labels. Reference Text = `"{code}-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
{open_formula}
```

Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

## Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.
'''
    text += '\n## Question control properties\n\nInsert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to Theme.Heading, body/counter Color to Theme.Muted. All labels wrap. Use the common input styling from the layout guide.\n'
    for n in range(1, 7):
        base = f'{p}Q{n}'
        text += f'''
### Slot {n}

| Control / property | Formula or value |
|---|---|
| `dc{base}Response.Visible` | `{n} <= varQuestionCount` |
| `dc{base}Response.X` / Y | `0` / `{n-1}` |
| `dc{base}Response.Width` | `Parent.Width` |
| `dc{base}Response.Height` | `If(Self.Visible, cnt{base}.Height + 18, 0)` |
| `cnt{base}` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cnt{base}.Height` | `lbl{base}Counter.Y + lbl{base}Counter.Height + 14` |
| `lbl{base}Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lbl{base}Heading.Text` | `With({{p:LookUp(colAnswers,Slot={n},Prompt)}},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion {n}")) & If(LookUp(colAnswers,Slot={n},Required)," *","")` |
| `lbl{base}Prompt` | X `22`; Y `lbl{base}Heading.Y+lbl{base}Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lbl{base}Prompt.Text` | `With({{p:LookUp(colAnswers,Slot={n},Prompt)}},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txt{base}` | X `22`; Y `lbl{base}Prompt.Y+lbl{base}Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txt{base}.Default` | `LookUp(colAnswers,Slot={n},Response)` |
| `txt{base}.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txt{base}.DelayOutput` | `false` |
| `txt{base}.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dc{base}Response.DisplayMode)` |
| `txt{base}.AccessibleLabel` | `LookUp(colAnswers,Slot={n},Prompt) & If(LookUp(colAnswers,Slot={n},Required),". Required", ". Optional")` |
| `lbl{base}Counter` | X `22`; Y `txt{base}.Y+txt{base}.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lbl{base}Counter.Text` | `Text(Len(txt{base}.Text)) & " / " & Text(varMaxResponseLength)` |

`txt{base}.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot={n}), {{Response:Self.Text}});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```
'''
    write(f'Form-{code}.md', text)

write('Form-Mapping.md', '# Fixed category routing\n\n' + '\n'.join(mapping))
write('Navigate-Active-Form.fx', route())
write('Review.Submit.OnSelect.fx', '''If(!varIsBusy && !varReadOnly,
    If(!DetailsValid || !ResponsesValid || !varCategoryComplete || !varDeclarationAccepted,
        Notify("Review the required information and accept the declaration before submitting.", NotificationType.Warning),
        Switch(varCategory.CategoryCode,
''' + ',\n'.join(submit_branches) + ''',
            Notify("The selected category has no configured form.", NotificationType.Error)
        )
    )
)''')

write('App.Formulas.fx', '''Theme = {
    Brand: "Contoso", AppTitle: "Employee & Team Recognition Awards",
    PrimaryHex: "#0f6cbd", SuccessHex: "#107c10", BorderHex: "#d8dee7",
    MutedHex: "#667085", PaleHex: "#eff6fc",
    Primary: ColorValue("#0f6cbd"), PrimaryHover: ColorValue("#0b5a9e"),
    Heading: ColorValue("#17253f"), Body: ColorValue("#27364f"),
    Muted: ColorValue("#667085"), Border: ColorValue("#d8dee7"),
    SoftBorder: ColorValue("#e8ebf0"), Page: ColorValue("#f4f6f8"),
    Surface: ColorValue("#ffffff"), Pale: ColorValue("#eff6fc"),
    Success: ColorValue("#107c10"), SuccessPale: ColorValue("#f1faf1"),
    Error: ColorValue("#c50f1f")
};
LevelOptions = Switch(varCategory.CategoryCode,
    "IND_CUSTOMER",Choices(Nom_IndividualCustomer.EmployeeLevel),
    "IND_EXCELLENCE",Choices(Nom_IndividualExcellence.EmployeeLevel),
    "TEAM_COLLAB",Choices(Nom_TeamCollaboration.EmployeeLevel),
    "TEAM_IMPACT",Choices(Nom_TeamImpact.EmployeeLevel),
    "TEAM_TRANSFORM",Choices(Nom_TeamTransformation.EmployeeLevel),
    Choices(Nom_IndividualInnovation.EmployeeLevel)
);
DetailsValid =
    If(varAwardType = "Individual",
        !IsBlank(varEmployee.Claims),
        !IsBlank(Trim(varTeamName)) && !IsBlank(varPrimaryContact.Claims)
    ) && !IsBlank(Trim(varRole)) && !IsBlank(varLevel) &&
    CountIf(LevelOptions,Value=varLevel)>0;
ResponsesValid =
    varQuestionCount >= 3 && varQuestionCount <= 6 &&
    CountIf(colAnswers, Slot <= varQuestionCount &&
        ((Required && IsBlank(Trim(Substitute(Substitute(Substitute(Response,Char(10)," "),Char(13)," "),Char(9)," ")))) || Len(Response) > varMaxResponseLength)
    ) = 0;
NomineeDisplay = If(varAwardType = "Individual", varEmployee.DisplayName, varTeamName);
NominationReference = If(IsBlank(varNominationId), "Not saved yet",
    varCategory.CategoryCode & "-" & Text(varNominationId, "000000"));
''')

write('App.OnStart.fx', '''Set(varUserEmail, Lower(User().Email));
Set(varMaxResponseLength, 2000);
Set(varEmptyPerson, {
    '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
    Claims: "", DisplayName: "", Email: "", Department: "", JobTitle: "", Picture: ""
});
Set(varSignedInPerson, {
    '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
    Claims: "i:0#.f|membership|" & varUserEmail,
    DisplayName: User().FullName, Email: varUserEmail,
    Department: "", JobTitle: "", Picture: ""
});
ClearCollect(colQuestionAdminIds, {ObjectId: "00000000-0000-0000-0000-000000000000"});
Set(varCanManageQuestions, Lower(Text(User().EntraObjectId)) in colQuestionAdminIds.ObjectId);
Set(varIsBusy, false);
Set(varReadOnly, false);
Set(varHasChanges, false);
Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1);
Set(varDetailsComplete, false);
Set(varCategoryComplete, false);
Set(varResponsesComplete, false);
Set(varSubmissionComplete, false);
Set(varAwardType, "Individual");
Set(varEmployee, varEmptyPerson);
Set(varPrimaryContact, varEmptyPerson);
Set(varNominator, varSignedInPerson);
Set(varTeamName, "");
Set(varRole, "");
Set(varLevel, "");
Set(varCategory, Defaults(AwardCategories));
Set(varPendingCategory, Defaults(AwardCategories));
Set(varNominationId, Blank());
Set(varLoadedModified, Blank());
Set(varSubmittedOn, Blank());
Set(varQuestionVersion, 0);
Set(varQuestionCount, 0);
Set(varSaveIntent, "Draft");
Set(varShowCategoryChangeDialog, false);
Set(varShowExitDialog, false);
Set(varShowAdminDiscard, false);
Set(varExitAction, "");
Set(varBrowseCode, "IND_INNOVATION");
Set(varBrowseType, "Individual");
Set(varBrowseStatus, "All");
Set(varBrowseId, 0);
ClearCollect(colTeamMembers, varEmptyPerson); Clear(colTeamMembers);
ClearCollect(colAnswers, ForAll(Sequence(6) As n,
    {Slot: n.Value, Prompt: "", Required: false, Response: ""}));
ClearCollect(colCapturedAnswers, colAnswers);
ClearCollect(colReviewFiles, {FileName: ""}); Clear(colReviewFiles);
ClearCollect(colCandidateQuestions, Defaults(AwardQuestions)); Clear(colCandidateQuestions);
ClearCollect(colCategoryOptions, Defaults(AwardCategories)); Clear(colCategoryOptions);
ClearCollect(colAdminCategories, Defaults(AwardCategories)); Clear(colAdminCategories);
ClearCollect(colAdminSource, Defaults(AwardQuestions)); Clear(colAdminSource);
ClearCollect(colAdminQuestions,
    {Slot: 1, Title: "", QuestionText: "", GuidanceText: "", IsRequired: true});
Clear(colAdminQuestions);
ClearCollect(colPublishErrors, {Slot: 0, Message: ""}); Clear(colPublishErrors);
Set(varAdminCategory, Defaults(AwardCategories));
Set(varAdminBaseVersion, 0);
Set(varAdminNewVersion, 0);
Set(varAdminSourceVersion, 0);
Set(varAdminDirty, false);
Set(varAdminLoadOK, false);
''' + '\n'.join(f'Set(varRecord{p}, Defaults({SOURCE_IDS[c]}));' for c,p,s,t in ROWS))

write('NewNomination.OnSelect.fx', '''Set(varAwardType, "Individual");
Set(varEmployee, varEmptyPerson);
Set(varPrimaryContact, varEmptyPerson);
Set(varNominator, varSignedInPerson);
Set(varTeamName, ""); Set(varRole, ""); Set(varLevel, "");
Clear(colTeamMembers);
Set(varCategory, Defaults(AwardCategories));
Set(varPendingCategory, Defaults(AwardCategories));
Set(varNominationId, Blank()); Set(varLoadedModified, Blank()); Set(varSubmittedOn, Blank());
Set(varQuestionVersion, 0); Set(varQuestionCount, 0);
Set(varReadOnly, false); Set(varIsBusy, false); Set(varHasChanges, false);
Set(varSaveIntent, "Draft"); Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1); Set(varDetailsComplete, false); Set(varCategoryComplete, false);
Set(varResponsesComplete, false); Set(varSubmissionComplete, false);
Set(varShowExitDialog, false); Set(varShowCategoryChangeDialog, false);
ClearCollect(colAnswers, ForAll(Sequence(6) As n,
    {Slot: n.Value, Prompt: "", Required: false, Response: ""}));
Clear(colReviewFiles);
''' + '\n'.join(f'Set(varRecord{p}, Defaults({SOURCE_IDS[c]}));\nResetForm(frm{s});\nNewForm(frm{s});' for c,p,s,t in ROWS) + '''
Navigate(scrNomineeDetails, ScreenTransition.None)
''')

write('Category.Load.OnSelect.fx', '''If(!varIsBusy,
    If(varCategoryComplete && varPendingCategory.ID = varCategory.ID,
        ''' + route() + ''',
        Set(varIsBusy, true);
        Set(varLoadOK, true);
        IfError(
            Refresh(AwardCategories);
            Set(varCandidateCategory, LookUp(AwardCategories, ID = varPendingCategory.ID));
            Refresh(AwardQuestions);
            ClearCollect(colCandidateQuestions,
                SortByColumns(Filter(AwardQuestions,
                    Category.Id = varCandidateCategory.ID,
                    QuestionSetVersion = varCandidateCategory.PublishedQuestionVersion
                ), "DisplayOrder", SortOrder.Ascending)
            );
            true,
            Set(varLoadOK, false); false
        );
        If(!varLoadOK || IsBlank(varCandidateCategory.ID) || !varCandidateCategory.IsActive ||
           varCandidateCategory.AwardType.Value <> varAwardType ||
           Switch(varCandidateCategory.CategoryCode,
             "IND_INNOVATION", "Individual", "IND_CUSTOMER", "Individual", "IND_EXCELLENCE", "Individual",
             "TEAM_COLLAB", "Team", "TEAM_IMPACT", "Team", "TEAM_TRANSFORM", "Team", "") <> varAwardType ||
           Coalesce(varCandidateCategory.PublishedQuestionVersion, 0) < 1 ||
           CountRows(colCandidateQuestions) < 3 || CountRows(colCandidateQuestions) > 6 ||
           CountRows(Distinct(colCandidateQuestions, DisplayOrder)) <> CountRows(colCandidateQuestions) ||
           CountIf(colCandidateQuestions,
               DisplayOrder < 1 || DisplayOrder > CountRows(colCandidateQuestions) ||
               DisplayOrder <> RoundDown(DisplayOrder, 0) ||
               QuestionKey.Value <> "Q" & Text(DisplayOrder) ||
               ConfigurationKey <> varCandidateCategory.CategoryCode & "-V" & Text(QuestionSetVersion) & "-" & QuestionKey.Value ||
               IsBlank(Trim(Title)) || Char(10) in Title ||
               IsBlank(Trim(Substitute(Substitute(Substitute(QuestionText,Char(10)," "),Char(13)," "),Char(9)," ")))
           ) > 0,
            Set(varIsBusy, false);
            Notify("This category does not have a valid published set of 3–6 questions. Contact the configuration manager.", NotificationType.Error),
            Set(varCategory, varCandidateCategory);
            Set(varQuestionVersion, varCandidateCategory.PublishedQuestionVersion);
            Set(varQuestionCount, CountRows(colCandidateQuestions));
            ClearCollect(colAnswers,
                ForAll(Sequence(6) As n,
                    With({q: LookUp(colCandidateQuestions, DisplayOrder = n.Value)},
                        {Slot: n.Value,
                         Prompt: If(n.Value <= varQuestionCount,
                             q.Title & Char(10) & q.QuestionText &
                             If(IsBlank(q.GuidanceText), "", Char(10) & Char(10) & "Guidance: " & q.GuidanceText), ""),
                         Required: If(n.Value <= varQuestionCount, q.IsRequired, false),
                         Response: ""}
                    )
                )
            );
            Set(varCategoryComplete, true);
            Set(varResponsesComplete, false);
            Set(varDeclarationAccepted, false);
            Set(varHasChanges, true);
            Set(varShowCategoryChangeDialog, false);
''' + '\n'.join(f'            ResetForm(frm{s}); NewForm(frm{s});' for c,p,s,t in ROWS) + '''
            Set(varIsBusy, false);
            Set(varCurrentStep, 3);
            ''' + route() + '''
        )
    )
)''')

write('Details.Continue.OnSelect.fx', '''Set(varTeamName, txtTeamName.Text);
Set(varRole, txtRole.Text);
Set(varLevel, Coalesce(cmbLevel.Selected.Value, ""));
Set(varDetailsComplete, DetailsValid);
Set(varDeclarationAccepted, false);
If(varCategoryComplete,
    ''' + route() + ''',
    Set(varCurrentStep, 2);
    Navigate(scrCategorySelection, ScreenTransition.None)
)''')

write('Admin.LoadCopy.OnSelect.fx', '''If(varCanManageQuestions && !varIsBusy,
    Set(varIsBusy, true);
    Set(varAdminLoadOK, true);
    IfError(
        Refresh(AwardCategories); Refresh(AwardQuestions);
        Set(varAdminCategory, LookUp(AwardCategories, ID = cmbAdminCategory.Selected.ID));
        Set(varAdminBaseVersion, Coalesce(varAdminCategory.PublishedQuestionVersion, 0));
        Set(varAdminHighestVersion,
            Coalesce(First(SortByColumns(
                Filter(AwardQuestions, Category.Id = varAdminCategory.ID),
                "QuestionSetVersion", SortOrder.Descending
            )).QuestionSetVersion, 0)
        );
        Set(varAdminNewVersion, varAdminHighestVersion + 1);
        Set(varAdminSourceVersion, If(varAdminBaseVersion > 0, varAdminBaseVersion, varAdminHighestVersion));
        ClearCollect(colAdminSource, SortByColumns(Filter(AwardQuestions,
            Category.Id = varAdminCategory.ID, QuestionSetVersion = varAdminSourceVersion
        ), "DisplayOrder", SortOrder.Ascending));
        If(CountRows(colAdminSource) = 0,
            ClearCollect(colAdminQuestions, ForAll(Sequence(3) As n,
                {Slot: n.Value, Title: "", QuestionText: "", GuidanceText: "", IsRequired: true})),
            ClearCollect(colAdminQuestions, ForAll(colAdminSource As q,
                {Slot: q.DisplayOrder, Title: q.Title, QuestionText: q.QuestionText,
                 GuidanceText: Coalesce(q.GuidanceText, ""), IsRequired: q.IsRequired}))
        );
        Set(varAdminDirty, false);
        true,
        Set(varAdminLoadOK, false);
        Notify("Unable to load the configuration. Nothing has been published.", NotificationType.Error);
        false
    );
    Set(varIsBusy, false)
)''')

write('Admin.Publish.OnSelect.fx', '''If(varCanManageQuestions && varAdminLoadOK && !varIsBusy,
    ClearCollect(colAdminEdits, ForAll(galAdminQuestions.AllItems As row,
        {Slot: row.Slot, Title: row.txtAdminTitle.Text,
         QuestionText: row.txtAdminQuestion.Text, GuidanceText: row.txtAdminGuidance.Text,
         IsRequired: row.chkAdminRequired.Value}));
    ForAll(colAdminEdits As edit,
        Patch(colAdminQuestions, LookUp(colAdminQuestions, Slot = edit.Slot),
            {Title: edit.Title, QuestionText: edit.QuestionText,
             GuidanceText: edit.GuidanceText, IsRequired: edit.IsRequired}));
    If(IsBlank(varAdminCategory.ID) || varAdminNewVersion <= varAdminBaseVersion ||
       CountRows(colAdminQuestions) < 3 || CountRows(colAdminQuestions) > 6 ||
       CountRows(Distinct(colAdminQuestions, Slot)) <> CountRows(colAdminQuestions) ||
       CountIf(colAdminQuestions,
           Slot < 1 || Slot > CountRows(colAdminQuestions) || Slot <> RoundDown(Slot, 0) ||
           IsBlank(Trim(Title)) || Len(Title) > 255 || Char(10) in Title ||
           IsBlank(Trim(Substitute(Substitute(Substitute(QuestionText,Char(10)," "),Char(13)," "),Char(9)," ")))
       ) > 0,
        Notify("Supply 3–6 ordered questions, each with a one-line title and question text.", NotificationType.Warning),
        Set(varIsBusy, true);
        Clear(colPublishErrors);
        Set(varPublishOK, true);
        IfError(
            Refresh(AwardCategories);
            Set(varAdminLatestCategory, LookUp(AwardCategories, ID = varAdminCategory.ID));
            If(Coalesce(varAdminLatestCategory.PublishedQuestionVersion, 0) <> varAdminBaseVersion,
                Set(varPublishOK, false);
                Notify("Another version has been published. Reload before making further changes.", NotificationType.Error)
            );
            true,
            Set(varPublishOK, false); false
        );
        If(varPublishOK,
            IfError(
                ForAll(colAdminQuestions As q,
                    With({keyText: varAdminCategory.CategoryCode & "-V" & Text(varAdminNewVersion) & "-Q" & Text(q.Slot)},
                        IfError(
                            With({existing: LookUp(AwardQuestions, ConfigurationKey = keyText)},
                                If(IsBlank(existing.ID),
                                    Patch(AwardQuestions, Defaults(AwardQuestions),
                                        {Title: q.Title,
                                         Category: {Id: varAdminCategory.ID, Value: varAdminCategory.Title},
                                         QuestionSetVersion: varAdminNewVersion,
                                         QuestionKey: {Value: "Q" & Text(q.Slot)},
                                         QuestionText: q.QuestionText, GuidanceText: q.GuidanceText,
                                         DisplayOrder: q.Slot, IsRequired: q.IsRequired,
                                         ConfigurationKey: keyText}
                                    ); true,
                                    existing.Category.Id = varAdminCategory.ID &&
                                    existing.QuestionSetVersion = varAdminNewVersion &&
                                    existing.QuestionKey.Value = "Q" & Text(q.Slot) &&
                                    existing.Title = q.Title && existing.QuestionText = q.QuestionText &&
                                    Coalesce(existing.GuidanceText, "") = q.GuidanceText &&
                                    existing.IsRequired = q.IsRequired && existing.DisplayOrder = q.Slot,
                                    true,
                                    Collect(colPublishErrors, {Slot: q.Slot, Message: "This version/key already contains different content. Allocate a new version."}); false
                                )
                            ),
                            Collect(colPublishErrors, {Slot: q.Slot, Message: "Question save failed. Publication was not completed."}); false
                        )
                    )
                ); true,
                Set(varPublishOK, false); false
            );
            If(CountRows(colPublishErrors) > 0, Set(varPublishOK, false));
            If(varPublishOK,
                IfError(
                    Refresh(AwardQuestions);
                    ClearCollect(colAdminSaved,
                        Filter(AwardQuestions, Category.Id = varAdminCategory.ID,
                            QuestionSetVersion = varAdminNewVersion));
                    If(CountRows(colAdminSaved) <> CountRows(colAdminQuestions) ||
                       CountIf(colAdminQuestions As q,
                           With({saved: LookUp(colAdminSaved, QuestionKey.Value = "Q" & Text(q.Slot))},
                               IsBlank(saved.ID) || saved.DisplayOrder <> q.Slot ||
                               saved.Title <> q.Title || saved.QuestionText <> q.QuestionText ||
                               Coalesce(saved.GuidanceText, "") <> q.GuidanceText || saved.IsRequired <> q.IsRequired ||
                               saved.ConfigurationKey <> varAdminCategory.CategoryCode & "-V" & Text(varAdminNewVersion) & "-Q" & Text(q.Slot)
                           )
                       ) > 0,
                        Set(varPublishOK, false)
                    ); true,
                    Set(varPublishOK, false); false
                )
            );
            If(varPublishOK,
                IfError(
                    Refresh(AwardCategories);
                    Set(varAdminLatestCategory, LookUp(AwardCategories, ID = varAdminCategory.ID));
                    If(Coalesce(varAdminLatestCategory.PublishedQuestionVersion, 0) <> varAdminBaseVersion,
                        Set(varPublishOK, false),
                        Set(varAdminCategory, Patch(AwardCategories, varAdminLatestCategory,
                            {PublishedQuestionVersion: varAdminNewVersion, IsActive: true}));
                        Set(varAdminBaseVersion, varAdminNewVersion);
                        Set(varAdminDirty, false)
                    ); true,
                    Set(varPublishOK, false); false
                )
            )
        );
        Set(varIsBusy, false);
        If(varPublishOK,
            Notify("Question version " & Text(varAdminNewVersion) & " published and category activated.", NotificationType.Success),
            Notify("Publication was not confirmed. Refresh the category pointer before retrying; retained question rows must not be deleted or overwritten.", NotificationType.Error)
        )
    )
)''')

review_layout = '''# Six expanding review question blocks

Create these six manual containers directly in the review page content container, after `cntReviewDetails`. They display the complete current prompts and responses. Use no input controls and no fixed-line clipping. All labels use Segoe UI and wrap. Each container Fill = Theme.Surface, BorderColor = Theme.Border, BorderThickness = 1, corner radii = 8. The formula for its Height refers only to its children, not its parent Height, avoiding a layout cycle.

For the first container use X = `cntReviewDetails.X`, Width = `cntReviewDetails.Width`. Use that same X/Width for the remaining five. `cntReviewDetails` must have its explicit Height from the main review guide.
'''
for n in range(1, 7):
    previous = 'cntReviewDetails' if n == 1 else f'cntReviewQ{n-1}'
    review_layout += f'''
## Review slot {n}

| Control / property | Value |
|---|---|
| `cntReviewQ{n}.Y` | `{previous}.Y+{previous}.Height+If({n}<=varQuestionCount,18,0)` |
| `cntReviewQ{n}.Visible` | `{n}<=varQuestionCount` |
| `cntReviewQ{n}.Height` | `If(Self.Visible,lblReviewAnswer{n}.Y+lblReviewAnswer{n}.Height+24,0)` |
| `lblReviewHeading{n}` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({{p:LookUp(colAnswers,Slot={n},Prompt)}},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion {n}"))` |
| `lblReviewPrompt{n}` | X `28`; Y `lblReviewHeading{n}.Y+lblReviewHeading{n}.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({{p:LookUp(colAnswers,Slot={n},Prompt)}},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer{n}` | X `28`; Y `lblReviewPrompt{n}.Y+lblReviewPrompt{n}.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({{a:LookUp(colAnswers,Slot={n},Response)}},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |
'''
review_layout += '\nPlace `cntReviewEvidence.Y` at `cntReviewQ6.Y+cntReviewQ6.Height+18`. Hidden trailing question containers have zero Height and add no gap.\n'
write('Review-Question-Controls.md', review_layout)

print(f'Generated {len(ROWS)} typed form recipes and shared formula files in {OUT}')
