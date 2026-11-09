If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(BestInnovatorIndividual);
        Set(varRecordII, LookUp(BestInnovatorIndividual, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordII.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordII.ID) || varCategory.CategoryCode <> "IND_INNOVATION" ||
       IsBlank(varRecordII.QuestionSetVersion) || varRecordII.QuestionSetVersion < 1 ||
       IsBlank(varRecordII.QuestionCount) || varRecordII.QuestionCount < 3 || varRecordII.QuestionCount > 6 ||
       varRecordII.QuestionCount <> RoundDown(varRecordII.QuestionCount,0) ||
       IsBlank(varRecordII.Q1PromptSnapshot) || IsBlank(varRecordII.Q2PromptSnapshot) || IsBlank(varRecordII.Q3PromptSnapshot) ||
       (varRecordII.QuestionCount>=4 && IsBlank(varRecordII.Q4PromptSnapshot)) ||
       (varRecordII.QuestionCount>=5 && IsBlank(varRecordII.Q5PromptSnapshot)) ||
       (varRecordII.QuestionCount>=6 && IsBlank(varRecordII.Q6PromptSnapshot)) ||
       !(varRecordII.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Individual");
        Set(varNominationId, varRecordII.ID);
        Set(varLoadedModified, varRecordII.Modified);
        Set(varQuestionVersion, varRecordII.QuestionSetVersion);
        Set(varQuestionCount, varRecordII.QuestionCount);
        Set(varRole, Coalesce(varRecordII.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordII.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordII.NominatedBy);
        Set(varEmployee, Coalesce(varRecordII.NominatedEmployee, varEmptyPerson));
        Set(varPrimaryContact, varEmptyPerson);
        Set(varTeamName, "");
        Clear(colTeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordII.Q1PromptSnapshot, ""), Required: Coalesce(varRecordII.Q1RequiredSnapshot, false), Response: Coalesce(varRecordII.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordII.Q2PromptSnapshot, ""), Required: Coalesce(varRecordII.Q2RequiredSnapshot, false), Response: Coalesce(varRecordII.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordII.Q3PromptSnapshot, ""), Required: Coalesce(varRecordII.Q3RequiredSnapshot, false), Response: Coalesce(varRecordII.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordII.Q4PromptSnapshot, ""), Required: Coalesce(varRecordII.Q4RequiredSnapshot, false), Response: Coalesce(varRecordII.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordII.Q5PromptSnapshot, ""), Required: Coalesce(varRecordII.Q5RequiredSnapshot, false), Response: Coalesce(varRecordII.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordII.Q6PromptSnapshot, ""), Required: Coalesce(varRecordII.Q6RequiredSnapshot, false), Response: Coalesce(varRecordII.Q6Response, "")}
));
        Set(varReadOnly, varRecordII.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordII.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmBestInnovatorIndividual);
        If(varReadOnly, ViewForm(frmBestInnovatorIndividual), EditForm(frmBestInnovatorIndividual));
        Set(varIsBusy, false);
        Navigate(scrBestInnovatorIndividual, ScreenTransition.None)
    )
)
