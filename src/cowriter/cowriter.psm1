Get-ChildItem -Path "$PSScriptRoot" -Recurse -File -Filter '*.ps1' -Exclude '*.tests.ps1' | ForEach-Object {
    . $_.FullName
}
Get-ChildItem -Path "$PSScriptRoot/public" -Recurse -File -Filter '*.ps1' -Exclude '*.tests.ps1' | ForEach-Object {
    Export-ModuleMember -Function $_.Basename
}
