param (
    $BuildDir = 'build',
    $ModuleSource = 'src/cowriter',
    $ModuleName = 'cowriter'
)
task prepare clean, {
    Install-Module -Name Pester -SkipPublisherCheck -MinimumVersion 5.0.0
    New-Item $BuildDir -ItemType Directory -Force | Out-Null
}
task test prepare, {
    Invoke-Pester . -Output Detailed
}
task build prepare, {
    Copy-Item $ModuleSource/$ModuleName.psd1 $BuildDir -Force
    $moduleScript = "$BuildDir/$ModuleName.psm1"
    Get-ChildItem $ModuleSource -Recurse -File -Filter '*.ps1' -Exclude '*.tests.ps1' |
        Get-Content |
        Add-Content $moduleScript -Force
    Copy-Item "$ModuleSource/files" $BuildDir -Recurse -Force
}
task clean {
    Remove-Item build -Recurse -Force -ErrorAction SilentlyContinue
}
