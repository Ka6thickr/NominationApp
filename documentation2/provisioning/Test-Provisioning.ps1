#requires -Version 7.4
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'Provision-NominationLists.ps1') -ValidateOnly | Out-Null

function Assert-True([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}

Assert-True ($schema.Count -eq 8) 'Eight lists must be defined.'
Assert-True ($codes.Count -eq 6) 'Six separate nomination lists must be defined.'
$testListId = [guid]'11111111-1111-1111-1111-111111111111'
foreach ($code in $codes) {
    $fields = $schema[$code]
    foreach ($slot in 1..6) {
        foreach ($suffix in @('PromptSnapshot','RequiredSnapshot','Response')) {
            Assert-True (@($fields | Where-Object Name -EQ "Q${slot}${suffix}").Count -eq 1) "Missing slot $slot/$suffix in $code"
        }
    }
    foreach ($definition in $fields) {
        Assert-True (-not $definition.Required) "Draft field must be optional at list level: $code/$($definition.Name)"
        [xml]$xml = ConvertTo-FieldXml $definition $testListId
        Assert-True ($xml.Field.GetAttribute('Name') -ceq $definition.Name) 'Internal field name was changed.'
        if ($definition.Type -eq 'Note') {
            Assert-True ($xml.Field.GetAttribute('RichText') -eq 'FALSE') 'Prompts/responses must be plain text.'
            Assert-True ($xml.Field.GetAttribute('AppendOnly') -eq 'FALSE') 'Append-only must be off.'
        }
        if ($definition.Type -eq 'Lookup') {
            Assert-True ([guid]$xml.Field.GetAttribute('List') -eq $testListId) 'Lookup must use the current environment category list ID.'
        }
    }
    $statusField = $fields | Where-Object Name -EQ NominationStatus
    Assert-True ($statusField.Default -eq 'Draft') 'Nomination status must default to Draft.'
    if ($code.StartsWith('TEAM_')) {
        $members = $fields | Where-Object Name -EQ TeamMembers
        [xml]$membersXml = ConvertTo-FieldXml $members $testListId
        Assert-True ($membersXml.Field.Type -eq 'UserMulti' -and $membersXml.Field.Mult -eq 'TRUE') 'TeamMembers must support multiple people.'
        Assert-True (@($fields | Where-Object Name -EQ NominatedEmployee).Count -eq 0) 'Team schema must not include individual-only fields.'
    } else {
        Assert-True (@($fields | Where-Object Name -EQ TeamName).Count -eq 0) 'Individual schema must not include team-only fields.'
    }
    Assert-True (@($fields | Where-Object { $_.Name -match '(?i)tag|evidencelink' }).Count -eq 0) 'Deferred/unapproved columns must not be added.'
}
[xml]$escaped = ConvertTo-FieldXml (New-FieldDefinition SyntheticChoice Choice @{Choices=@('Research & Development','<Example>')}) $testListId
Assert-True ($escaped.Field.CHOICES.CHOICE[0] -ceq 'Research & Development') 'Choice XML must round-trip ampersands.'
Assert-True ($escaped.Field.CHOICES.CHOICE[1] -ceq '<Example>') 'Choice XML must round-trip angle brackets.'
$publicationBlocked = $false
try { & (Join-Path $PSScriptRoot 'Provision-NominationLists.ps1') -ValidateOnly -PublishSeed | Out-Null }
catch { $publicationBlocked = $_.Exception.Message -like 'Approve seed content*' }
Assert-True $publicationBlocked 'Unapproved seed publication must be blocked before connecting.'
'PASS: fixed schema, draft fields, Q1-Q6 slots, environment lookup binding, choice XML escaping, and unapproved publication guard.'
