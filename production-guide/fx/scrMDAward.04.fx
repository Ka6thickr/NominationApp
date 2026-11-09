Set(varRecordIC, frmMDAward.LastSubmit);
Set(varNominationId, varRecordIC.ID);
Set(varLoadedModified, varRecordIC.Modified);
EditForm(frmMDAward);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordIC,
            Patch(MDAward, varRecordIC,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordIC.Modified);
        Set(varSubmittedOn, varRecordIC.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmMDAward);
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
