SortByColumns(
    Filter(BestInnovatorTeam,
        NominatorEmail = varUserEmail,
        (varBrowseStatus = "All" || NominationStatus.Value = varBrowseStatus),
        (varBrowseId = 0 || ID = varBrowseId)
    ),
    "Modified", SortOrder.Descending
)
