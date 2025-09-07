param (
    $BuildDir = 'build',
    $ModuleSource = 'src/cowriter',
    $ModuleName = 'cowriter',
    $PesterConfig = 'pester.psd1',
    $ApiKey = $env:NUGET_API_KEY
)
task pre-test {
    Install-Module -Name Pester -SkipPublisherCheck -MinimumVersion 5.0.0 -Scope CurrentUser -Force
}
task pre-build {
    Remove-Item $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
    New-Item $BuildDir -ItemType Directory -Force | Out-Null
}
task clean {
    Remove-Item $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
}
task test pre-test, {
    $config = Import-PowerShellDataFile $PesterConfig
    Invoke-Pester -Configuration $config
}
task build pre-build, {
    Copy-Item $ModuleSource/$ModuleName.psd1 $BuildDir -Force
    $moduleScript = "$BuildDir/$ModuleName.psm1"
    Get-ChildItem "$ModuleSource/public" -Recurse -File -Filter '*.ps1' -Exclude '*.tests.ps1' -OutVariable functions |
        Get-Content |
        Add-Content $moduleScript -Force
    # "Export-ModuleMember -Function $($functions.BaseName -join ', ')" | Add-Content $moduleScript
    Copy-Item "$ModuleSource/files" $BuildDir -Recurse -Force
    Copy-Item README.md $BuildDir -Force
}
task publish build, {
    Publish-PSResource -Path $BuildDir -ApiKey $ApiKey
}
task . test, build
# TODO: Remove
task import build, {
    Import-Module "./$BuildDir/$ModuleName.psd1" -Force
}
task start import, {
    Cowriter
}
