Set(varRecordIE, frmTrendMarcherAward.LastSubmit);
Set(varNominationId, varRecordIE.ID);
Set(varLoadedModified, varRecordIE.Modified);
EditForm(frmTrendMarcherAward);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordIE,
            Patch(TrendMarcherAward, varRecordIE,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordIE.Modified);
        Set(varSubmittedOn, varRecordIE.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmTrendMarcherAward);
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
