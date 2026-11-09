ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTCQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTCQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTCQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTCQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTCQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTCQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDetailsComplete, DetailsValid);
Set(varResponsesComplete, ResponsesValid);
If(!DetailsValid,
    Notify("Complete nominee details, role and level before review.", NotificationType.Warning);
    Navigate(scrNomineeDetails, ScreenTransition.None),
    !ResponsesValid,
    Notify("Complete every required response before review.", NotificationType.Warning),
    Set(varDeclarationAccepted, false);
    ClearCollect(colReviewFiles, ForAll(attTC.Attachments As file, {FileName: file.Name}));
    Set(varCurrentStep, 4);
    Navigate(scrReview, ScreenTransition.None)
)
