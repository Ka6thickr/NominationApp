Set(varUserEmail, Lower(User().Email));
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
Set(varRecordII, Defaults(Nom_IndividualInnovation));
Set(varRecordIC, Defaults(Nom_IndividualCustomer));
Set(varRecordIE, Defaults(Nom_IndividualExcellence));
Set(varRecordTC, Defaults(Nom_TeamCollaboration));
Set(varRecordTI, Defaults(Nom_TeamImpact));
Set(varRecordTT, Defaults(Nom_TeamTransformation));
