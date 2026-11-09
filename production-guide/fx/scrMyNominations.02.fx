Set(varBrowseType,"Individual");
Set(varBrowseCode,First(Filter(colBrowseCategories,AwardType.Value="Individual")).CategoryCode);
Set(varBrowseId,0); Reset(txtBrowseId)
