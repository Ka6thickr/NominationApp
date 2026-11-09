If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(TrendMarcherAward);
        Set(varRecordIE, LookUp(TrendMarcherAward, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordIE.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordIE.ID) || varCategory.CategoryCode <> "IND_EXCELLENCE" ||
       IsBlank(varRecordIE.QuestionSetVersion) || varRecordIE.QuestionSetVersion < 1 ||
       IsBlank(varRecordIE.QuestionCount) || varRecordIE.QuestionCount < 3 || varRecordIE.QuestionCount > 6 ||
       varRecordIE.QuestionCount <> RoundDown(varRecordIE.QuestionCount,0) ||
       IsBlank(varRecordIE.Q1PromptSnapshot) || IsBlank(varRecordIE.Q2PromptSnapshot) || IsBlank(varRecordIE.Q3PromptSnapshot) ||
       (varRecordIE.QuestionCount>=4 && IsBlank(varRecordIE.Q4PromptSnapshot)) ||
       (varRecordIE.QuestionCount>=5 && IsBlank(varRecordIE.Q5PromptSnapshot)) ||
       (varRecordIE.QuestionCount>=6 && IsBlank(varRecordIE.Q6PromptSnapshot)) ||
       !(varRecordIE.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Individual");
        Set(varNominationId, varRecordIE.ID);
        Set(varLoadedModified, varRecordIE.Modified);
        Set(varQuestionVersion, varRecordIE.QuestionSetVersion);
        Set(varQuestionCount, varRecordIE.QuestionCount);
        Set(varRole, Coalesce(varRecordIE.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordIE.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordIE.NominatedBy);
        Set(varEmployee, Coalesce(varRecordIE.NominatedEmployee, varEmptyPerson));
        Set(varPrimaryContact, varEmptyPerson);
        Set(varTeamName, "");
        Clear(colTeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordIE.Q1PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q1RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordIE.Q2PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q2RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordIE.Q3PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q3RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordIE.Q4PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q4RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordIE.Q5PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q5RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordIE.Q6PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q6RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q6Response, "")}
));
        Set(varReadOnly, varRecordIE.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordIE.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmTrendMarcherAward);
        If(varReadOnly, ViewForm(frmTrendMarcherAward), EditForm(frmTrendMarcherAward));
        Set(varIsBusy, false);
        Navigate(scrTrendMarcherAward, ScreenTransition.None)
    )
)
