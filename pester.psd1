@{
    Run = @{
        Throw = $true
        Exit = $true
    }
    TestResult = @{
        # TODO: Enable
        Enabled = $false # $true
        OutputFormat = 'JUnitXml'
        StackTraceVerbosity = 'None'
    }
    Output = @{
        Verbosity = 'Detailed'
        CIFormat = 'GithubActions'
    }
}
