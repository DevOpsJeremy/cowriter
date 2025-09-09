[CmdletBinding()]
param (
    [string] $Scheme = 'https',
    [int] $Port = 443,
    [string] $UriHost = 'raw.githubusercontent.com',
    [string] $Repo = 'DevOpsJeremy/cowriter',
    [string] $Ref = 'main',
    [string] $Script = 'src/cowriter/scripts/setup.ps1'
)
Begin {
    #region Functions
    function ConvertTo-Base64String {
        [CmdletBinding()]
        param (
            [string] $InputString
        )
        $bytes = [System.Text.Encoding]::Unicode.GetBytes($InputString)
        return [System.Convert]::ToBase64String($bytes)
    }
    #endregion Functions
}
Process {
    $uri = [UriBuilder]::new(
        $Scheme,
        $UriHost,
        $Port,
        "$Repo/$Ref/$Script"
    ).Uri
    $script = Invoke-RestMethod $uri -ErrorAction Stop
    if (-not $?) {
        exit 1
    }
    $encoded = ConvertTo-Base64String $script
    return $encoded
    # echo "Start-Process (Get-Command powershell).Source @(-EncodedCommand, $encoded, -WindowStyle, Hidden)"
    # Start-Process (Get-Command powershell).Source @("-EncodedCommand", "$encoded", "-WindowStyle", "Hidden")
}
