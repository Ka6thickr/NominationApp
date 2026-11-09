Set(varRecordII, frmBestInnovatorIndividual.LastSubmit);
Set(varNominationId, varRecordII.ID);
Set(varLoadedModified, varRecordII.Modified);
EditForm(frmBestInnovatorIndividual);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordII,
            Patch(BestInnovatorIndividual, varRecordII,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordII.Modified);
        Set(varSubmittedOn, varRecordII.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmBestInnovatorIndividual);
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
