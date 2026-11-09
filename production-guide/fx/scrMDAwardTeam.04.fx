Set(varRecordTI, frmMDAwardTeam.LastSubmit);
Set(varNominationId, varRecordTI.ID);
Set(varLoadedModified, varRecordTI.Modified);
EditForm(frmMDAwardTeam);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordTI,
            Patch(MDAwardTeam, varRecordTI,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordTI.Modified);
        Set(varSubmittedOn, varRecordTI.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmMDAwardTeam);
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
)
