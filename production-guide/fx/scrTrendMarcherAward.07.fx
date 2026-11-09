SortByColumns(
    Filter(TrendMarcherAward,
        NominatorEmail = varUserEmail,
        (varBrowseStatus = "All" || NominationStatus.Value = varBrowseStatus),
        (varBrowseId = 0 || ID = varBrowseId)
    ),
    "Modified", SortOrder.Descending
)
