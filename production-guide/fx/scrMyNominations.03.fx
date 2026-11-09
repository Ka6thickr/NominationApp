If(IsBlank(Trim(Self.Text)),
    Set(varBrowseId,0),
    If(IsNumeric(Self.Text) && Value(Self.Text)>0 && Value(Self.Text)=RoundDown(Value(Self.Text),0),
        Set(varBrowseId,Value(Self.Text)),
        Notify("Enter a positive whole item ID.",NotificationType.Warning);
        Set(varBrowseId,0); Reset(txtBrowseId)
    )
)
