If(!varIsBusy && !varReadOnly && varCategoryComplete,
    ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtICQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtICQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtICQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtICQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtICQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtICQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
    If(CountIf(colAnswers, Len(Response) > varMaxResponseLength) > 0,
        Notify("A response exceeds the configured limit.", NotificationType.Warning),
        Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(MDAward);
        Set(varLatestIC, LookUp(MDAward, ID = varNominationId));
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
    Set(varSaveIntent, "Draft");
    SubmitForm(frmMDAward),
    Set(varIsBusy, false)
)
    )
)
