If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(MDAward);
        Set(varRecordIC, LookUp(MDAward, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordIC.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordIC.ID) || varCategory.CategoryCode <> "IND_CUSTOMER" ||
       IsBlank(varRecordIC.QuestionSetVersion) || varRecordIC.QuestionSetVersion < 1 ||
       IsBlank(varRecordIC.QuestionCount) || varRecordIC.QuestionCount < 3 || varRecordIC.QuestionCount > 6 ||
       varRecordIC.QuestionCount <> RoundDown(varRecordIC.QuestionCount,0) ||
       IsBlank(varRecordIC.Q1PromptSnapshot) || IsBlank(varRecordIC.Q2PromptSnapshot) || IsBlank(varRecordIC.Q3PromptSnapshot) ||
       (varRecordIC.QuestionCount>=4 && IsBlank(varRecordIC.Q4PromptSnapshot)) ||
       (varRecordIC.QuestionCount>=5 && IsBlank(varRecordIC.Q5PromptSnapshot)) ||
       (varRecordIC.QuestionCount>=6 && IsBlank(varRecordIC.Q6PromptSnapshot)) ||
       !(varRecordIC.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Individual");
        Set(varNominationId, varRecordIC.ID);
        Set(varLoadedModified, varRecordIC.Modified);
        Set(varQuestionVersion, varRecordIC.QuestionSetVersion);
        Set(varQuestionCount, varRecordIC.QuestionCount);
        Set(varRole, Coalesce(varRecordIC.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordIC.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordIC.NominatedBy);
        Set(varEmployee, Coalesce(varRecordIC.NominatedEmployee, varEmptyPerson));
        Set(varPrimaryContact, varEmptyPerson);
        Set(varTeamName, "");
        Clear(colTeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordIC.Q1PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q1RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordIC.Q2PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q2RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordIC.Q3PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q3RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordIC.Q4PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q4RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordIC.Q5PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q5RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordIC.Q6PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q6RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q6Response, "")}
));
        Set(varReadOnly, varRecordIC.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordIC.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmMDAward);
        If(varReadOnly, ViewForm(frmMDAward), EditForm(frmMDAward));
        Set(varIsBusy, false);
        Navigate(scrMDAward, ScreenTransition.None)
    )
)
