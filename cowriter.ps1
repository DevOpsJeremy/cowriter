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
$PSDefaultParameterValues = @{
    'Invoke-RestMethod:Authentication' = $Authentication
    'Invoke-RestMethod:Token'         = $Token
}
$uri = [UriBuilder]::new(
    $Scheme,
    $UriHost,
    $Port,
    "$Repo/$Ref/$Script"
).Uri
irm $uri
