If(!varIsBusy && !varReadOnly,
    If(!DetailsValid || !ResponsesValid || !varCategoryComplete || !varDeclarationAccepted,
        Notify("Review the required information and accept the declaration before submitting.", NotificationType.Warning),
        Switch(varCategory.CategoryCode,
    "IND_INNOVATION",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(Nom_IndividualInnovation);
        Set(varLatestII, LookUp(Nom_IndividualInnovation, ID = varNominationId));
        If(IsBlank(varLatestII.ID) ||
           varLatestII.NominationStatus.Value <> "Draft" ||
           varLatestII.Modified <> varLoadedModified,
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
    Set(varSaveIntent, "Submit");
    SubmitForm(frmIndividualInnovation),
    Set(varIsBusy, false)
),
    "IND_CUSTOMER",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(Nom_IndividualCustomer);
        Set(varLatestIC, LookUp(Nom_IndividualCustomer, ID = varNominationId));
        If(IsBlank(varLatestIC.ID) ||
           varLatestIC.NominationStatus.Value <> "Draft" ||
           varLatestIC.Modified <> varLoadedModified,
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
    Set(varSaveIntent, "Submit");
    SubmitForm(frmIndividualCustomer),
    Set(varIsBusy, false)
),
    "IND_EXCELLENCE",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(Nom_IndividualExcellence);
        Set(varLatestIE, LookUp(Nom_IndividualExcellence, ID = varNominationId));
        If(IsBlank(varLatestIE.ID) ||
           varLatestIE.NominationStatus.Value <> "Draft" ||
           varLatestIE.Modified <> varLoadedModified,
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
    Set(varSaveIntent, "Submit");
    SubmitForm(frmIndividualExcellence),
    Set(varIsBusy, false)
),
    "TEAM_COLLAB",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(Nom_TeamCollaboration);
        Set(varLatestTC, LookUp(Nom_TeamCollaboration, ID = varNominationId));
        If(IsBlank(varLatestTC.ID) ||
           varLatestTC.NominationStatus.Value <> "Draft" ||
           varLatestTC.Modified <> varLoadedModified,
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
    Set(varSaveIntent, "Submit");
    SubmitForm(frmTeamCollaboration),
    Set(varIsBusy, false)
),
    "TEAM_IMPACT",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(Nom_TeamImpact);
        Set(varLatestTI, LookUp(Nom_TeamImpact, ID = varNominationId));
        If(IsBlank(varLatestTI.ID) ||
           varLatestTI.NominationStatus.Value <> "Draft" ||
           varLatestTI.Modified <> varLoadedModified,
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
    Set(varSaveIntent, "Submit");
    SubmitForm(frmTeamImpact),
    Set(varIsBusy, false)
),
    "TEAM_TRANSFORM",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(Nom_TeamTransformation);
        Set(varLatestTT, LookUp(Nom_TeamTransformation, ID = varNominationId));
        If(IsBlank(varLatestTT.ID) ||
           varLatestTT.NominationStatus.Value <> "Draft" ||
           varLatestTT.Modified <> varLoadedModified,
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
    Set(varSaveIntent, "Submit");
    SubmitForm(frmTeamTransformation),
    Set(varIsBusy, false)
),
            Notify("The selected category has no configured form.", NotificationType.Error)
        )
    )
)
