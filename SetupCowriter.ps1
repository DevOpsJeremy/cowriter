[CmdletBinding()]
param (
    [string] $Scheme = 'https',
    [int] $Port = 443,
    [string] $UriHost = 'raw.githubusercontent.com',
    [string] $Repo = 'DevOpsJeremy/cowriter',
    [string] $Ref = 'main',
    [string] $Script = 'setup.ps1',
    # TODO: Remove
    [string] $Authentication = 'Bearer',
    [SecureString] $Token
)
Begin {
    # TODO: Remove
    $PSDefaultParameterValues = @{
        'Invoke-RestMethod:Authentication' = $Authentication
        'Invoke-RestMethod:Token'         = $Token
    }
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
    $encoded = ConvertTo-Base64String $script
    Start-Process (Get-Command powershell).Source @("-EncodedCommand", "$encoded", "-WindowStyle", "Minimized")
}
