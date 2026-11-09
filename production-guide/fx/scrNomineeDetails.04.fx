If(Len(Self.SearchText)<2,
    Blank(),
    IfError(Office365Users.SearchUserV2(
        {searchTerm:Self.SearchText,top:25,isSearchTermRequired:true}
    ).value,
        Notify("Directory search failed. Check the directory connection and try again.", NotificationType.Error);
        Blank())
)
