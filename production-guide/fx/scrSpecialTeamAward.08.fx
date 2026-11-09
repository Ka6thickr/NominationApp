If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(SpecialTeamAward);
        Set(varRecordTT, LookUp(SpecialTeamAward, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordTT.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordTT.ID) || varCategory.CategoryCode <> "TEAM_TRANSFORM" ||
       IsBlank(varRecordTT.QuestionSetVersion) || varRecordTT.QuestionSetVersion < 1 ||
       IsBlank(varRecordTT.QuestionCount) || varRecordTT.QuestionCount < 3 || varRecordTT.QuestionCount > 6 ||
       varRecordTT.QuestionCount <> RoundDown(varRecordTT.QuestionCount,0) ||
       IsBlank(varRecordTT.Q1PromptSnapshot) || IsBlank(varRecordTT.Q2PromptSnapshot) || IsBlank(varRecordTT.Q3PromptSnapshot) ||
       (varRecordTT.QuestionCount>=4 && IsBlank(varRecordTT.Q4PromptSnapshot)) ||
       (varRecordTT.QuestionCount>=5 && IsBlank(varRecordTT.Q5PromptSnapshot)) ||
       (varRecordTT.QuestionCount>=6 && IsBlank(varRecordTT.Q6PromptSnapshot)) ||
       !(varRecordTT.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Team");
        Set(varNominationId, varRecordTT.ID);
        Set(varLoadedModified, varRecordTT.Modified);
        Set(varQuestionVersion, varRecordTT.QuestionSetVersion);
        Set(varQuestionCount, varRecordTT.QuestionCount);
        Set(varRole, Coalesce(varRecordTT.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordTT.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordTT.NominatedBy);
        Set(varTeamName, Coalesce(varRecordTT.TeamName, ""));
        Set(varPrimaryContact, Coalesce(varRecordTT.TeamPrimaryContact, varEmptyPerson));
        Set(varEmployee, varEmptyPerson);
        ClearCollect(colTeamMembers, varRecordTT.TeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordTT.Q1PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q1RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordTT.Q2PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q2RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordTT.Q3PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q3RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordTT.Q4PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q4RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordTT.Q5PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q5RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordTT.Q6PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q6RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q6Response, "")}
));
        Set(varReadOnly, varRecordTT.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordTT.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmSpecialTeamAward);
        If(varReadOnly, ViewForm(frmSpecialTeamAward), EditForm(frmSpecialTeamAward));
        Set(varIsBusy, false);
        Navigate(scrSpecialTeamAward, ScreenTransition.None)
    )
)
