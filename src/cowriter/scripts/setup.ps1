[CmdletBinding()]
param (
    [uri] $OllamaDownloadUrl = 'https://github.com/ollama/ollama/releases/latest/download/OllamaSetup.exe'
)
Begin {
    # Add the Windows Presentation Foundation framework for the window
    Add-Type -Assembly PresentationFramework
    $script:appName = 'Cowriter'

    #region Functions
    function Get-RemoteFileSize {
        [CmdletBinding()]
        param (
            [uri] $Uri
        )
        $response = Invoke-WebRequest -Uri $Uri -Method Head
        return [int] ($response.Headers["Content-Length"] | Select-Object -First 1)
    }
    function Build-Window {
        [CmdletBinding()]
        param (
            [int] $MinFontSize = 8,
            [int] $MaxFontSize = 30
        )

        #region Functions
        #endregion Functions

        #region Scripts
        $script:setPageContent = {
            param (
                [int] $Page
            )
            $pageHash = $script:pages[$Page]
            $script:titleBar.Text = $pageHash['Title']
            $script:pageContent.Content = $pageHash['Content']
        }
        $script:setPage = {
            param (
                [switch] $Next,
                [switch] $Previous
            )
            $currentPage = $script:content.Tag['Page']
            $minimum = 0
            $maximum = $script:pages.Count - 1
            if ($Next) {
                $newPage = $currentPage + 1
                if ($newPage -gt $maximum) {
                    return
                }
            }
            if ($Previous) {
                $newPage = $currentPage - 1
                if ($newPage -lt $minimum) {
                    return
                }
            }
            & $script:setPageContent -Page $newPage
            $script:content.Tag['Page'] = $newPage
            if ($newPage -eq $minimum) {
                $script:backButton.IsEnabled = $false
            } else {
                $script:backButton.IsEnabled = $true
            }
            if ($newPage -eq $maximum) {
                $script:nextButton.Content = "Finish"
                $script:nextButton.Add_Click($script:closeWindowEH)
            } else {
                $script:nextButton.Content = "Next"
                $script:nextButton.Remove_Click($script:closeWindowEH)
            }
        }
        $script:closeWindow = { $script:window.Close() }
        $script:closeWindowEH = [Windows.RoutedEventHandler] $closeWindow
        #endregion Scripts

        # Create the window
        $script:window = [Window] @{
            Title = "${script:appName} Setup"
            Width = 700
            Height = 500
            WindowStartupLocation = "CenterScreen"
            Topmost = $true
            FontSize = 16
            Tag = @{
                MinFontSize = $MinFontSize
                MaxFontSize = $MaxFontSize
            }
        }
        $window.Add_Loaded({ $window.Topmost = $false })

        #region Main Content
        # Grids for the main area + navigation buttons
        $grid = [Grid]::new()
        # Page
        $row1 = [RowDefinition]::new()
        # Navigation buttons
        $row2 = [RowDefinition] @{ Height = 50 }
        [void] $grid.RowDefinitions.Add($row1)
        [void] $grid.RowDefinitions.Add($row2)

        $script:content = [StackPanel] @{
            Margin = "5"
            Orientation = "Vertical"
            Tag = @{
                Page = 0
            }
        }
        [Grid]::SetRow($content, 0)
        [void] $grid.Children.Add($content)

        # Title bar
        # Displays the title for each individual page
        $script:titleBar = [TextBlock] @{
            FontSize = 20
            FontWeight = "Bold"
            Margin = '10,5,0,5'
            Height = 40
        }
        [void] $content.Children.Add($titleBar)

        # Main content area
        # This will update as the user navigates through the wizard
        $script:pageContent = [ContentControl]::new()
        [void] $content.Children.Add($pageContent)

        # Pages
        # This is the structure of each page in the wizard
        
        # Introduction page
        $introduction = @{
            Title = 'Introduction'
            Content = [TextBlock] @{
                Text = "Welcome to the ${script:appName} Setup Wizard.`n`nThis wizard will guide you through the installation of ${script:appName} and its dependencies."
                TextWrapping = "Wrap"
                Margin = 10
            }
        }

        # Dependencies page
        $script:dependenciesPage = [StackPanel] @{
            Margin = 10
            Orientation = "Vertical"
            VerticalAlignment = "Stretch"
            Tag = @{
                OutstandingDependencies = @()
            }
        }

        $script:moduleName = $script:appName
        $script:checkModule = {
            # Check that the Cowriter module (this) is installed
            $module = Get-Module -Name $script:moduleName -ListAvailable
            if (-not $module) {
                return $false
            }
            return $true
        }
        $script:installModule = {
            Install-Module -Name $script:moduleName -Scope CurrentUser -Force -AllowClobber
        }
        $script:checkOllama = {
            # Check that `ollama.exe` is found and in $PATH
            $ollama = Get-Command 'ollama' -ErrorAction SilentlyContinue
            if (-not $ollama) {
                return $false
            }
            return $true
        }
        $script:installOllama = {
            $tmp = [IO.Path]::GetTempPath()
            $output = [IO.Path]::Combine($tmp, 'ollamaSetup.exe')
            Invoke-WebRequest -Uri $OllamaDownloadUrl -OutFile $output
            & $output /SILENT
        }
        $script:checkModel = {
            $ollama = Get-Command 'ollama' -ErrorAction SilentlyContinue
            if (-not $ollama) {
                return $false
            }
            # List models
            try {
                $models = (Invoke-RestMethod http://127.0.0.1:11434/api/tags -ErrorAction Stop).models
            } catch {
                return $false
            }
            if ($models.Count -lt 1) {
                return $false
            }
            return $true
        }
        $script:installModel = {
            $ollama = Get-Command 'ollama' -ErrorAction SilentlyContinue
            if (-not $ollama) {
                throw "Ollama is not installed. Cannot install model."
            }
            # Pull the model - `ollama pull llama3.2`
            & $ollama.Source pull llama3.2
        }
        $script:depHash = [Ordered] @{
            module = @{
                Name = $script:moduleName
                CheckScript = $script:checkModule
                InstallScript = $script:installModule
            }
            ollama = @{
                Name = 'Ollama'
                CheckScript = $script:checkOllama
                InstallScript = $script:installOllama
            }
            model = @{
                Name = 'AI Model'
                CheckScript = $script:checkModel
                InstallScript = $script:installOllama
            }
        }
        # Check if we've already checked for dependencies
        # if we have, don't check again
        $script:dependenciesChecked = $false
        $script:checkDependencies = {
            if ($script:dependenciesChecked) {
                return
            }
            $script:satisfiedDependenciesList.Items.Clear()
            $script:unsatisfiedDependenciesList.Items.Clear()
            $depStatus = @{}
            foreach ($dependency in $script:depHash.GetEnumerator()) {
                $depStatus[$dependency.Key] = & $dependency.Value['CheckScript']
            }
            foreach ($dependency in $depStatus.GetEnumerator()) {
                switch ($dependency.Value) {
                    $true {
                        $script:satisfiedDependenciesList.Items.Add($script:depHash[$dependency.Key]['Name'])
                    }
                    $false {
                        $script:dependenciesPage.Tag['OutstandingDependencies'] += $dependency.Key
                        $script:unsatisfiedDependenciesList.Items.Add($script:depHash[$dependency.Key]['Name'])
                    }
                }
            }
            if ($script:satisfiedDependenciesList.Items.Count -gt 0) {
                $script:satisfiedDependencies.Visibility = "Visible"
            }
            if ($script:unsatisfiedDependenciesList.Items.Count -gt 0) {
                $script:unsatisfiedDependencies.Visibility = "Visible"
            }
            $script:dependenciesChecked = $true
        }
        # Check the dependencies at launch to save processing time
        $dependenciesPage.Add_Loaded({ . $script:checkDependencies })

        # Dependencies already installed/satisfied
        $script:satisfiedDependencies = [StackPanel] @{
            # Hide by default. This is unhidden if dependencies are found to be installed
            Visibility = "Hidden"
        }
        [void] $satisfiedDependencies.Children.Add([TextBlock] @{
            Text = "The following dependencies are already installed"
            FontWeight = "Bold"
        })
        $script:satisfiedDependenciesList = [ListBox]::new()
        [void] $satisfiedDependencies.Children.Add($satisfiedDependenciesList)
        
        # Dependencies not yet installed/satisfied
        $script:unsatisfiedDependencies = [StackPanel] @{
            Margin = "0,30,0,0"
            # Hide by default. This is unhidden if dependencies are found to not be installed
            Visibility = "Hidden"
        }
        [void] $unsatisfiedDependencies.Children.Add([TextBlock] @{
            Text = "The following dependencies will be installed"
            FontWeight = "Bold"
        })
        $script:unsatisfiedDependenciesList = [ListBox]::new()
        [void] $unsatisfiedDependencies.Children.Add($unsatisfiedDependenciesList)

        # Assemble dependencies page
        [void] $dependenciesPage.Children.Add($satisfiedDependencies)
        [void] $dependenciesPage.Children.Add($unsatisfiedDependencies)
        $dependencies = @{
            Title = 'Dependencies'
            Content = $dependenciesPage
        }
        
        # Installation page
        $installingPage = [StackPanel] @{
            Margin = 10
            Orientation = "Vertical"
            VerticalAlignment = "Stretch"
        }
        $script:installingPageTitle = [TextBlock] @{
            FontSize = 18
            FontWeight = "Bold"
            # Margin = '10,5,0,5'
            Height = 30
        }
        $script:installingPageBody = [StackPanel]::new()
        [void] $installingPage.Children.Add($installingPageTitle)
        [void] $installingPage.Children.Add($installingPageBody)
        $installing = @{
            Title = 'Installing'
            Content = $installingPage
        }

        # Complete page
        $script:completePage = [StackPanel] @{
            Margin = 10
            Orientation = "Vertical"
            VerticalAlignment = "Stretch"
        }
        [void] $completePage.Children.Add([TextBlock] @{
            Text = "Installation is complete!`n`nYou can now start using ${script:appName}."
            TextWrapping = "Wrap"
            Margin = 10
        })
        [void] $completePage.Children.Add([CheckBox] @{
            Content = "Launch ${script:appName}"
            Margin = "60,30,30,0"
        })

        $complete = @{
            Title = 'Complete'
            Content = $completePage
        }

        $script:pages = @(
            $introduction,
            $dependencies,
            $installing,
            $complete
        )

        # Bottom navigation buttons
        $navGrid = [Grid]::new()
        $navCol1 = [ColumnDefinition]::new()
        $navCol2 = [ColumnDefinition]::new()
        [void] $navGrid.ColumnDefinitions.Add($navCol1)
        [void] $navGrid.ColumnDefinitions.Add($navCol2)
        [void] [Grid]::SetRow($navGrid, 1)
        [void] $grid.Children.Add($navGrid)

        # Zoom panel
        $zoomPanel = [StackPanel] @{
            Orientation = "Horizontal"
            HorizontalAlignment = "Left"
            Margin = "10,10,0,10"
        }
        [void] [Grid]::SetColumn($zoomPanel, 0)
        [void] $navGrid.Children.Add($zoomPanel)
        $zoomOutButton = [Button] @{
            Content = "-"
            Width = 30
            Margin = "10,0,0,0"
        }
        $zoomOutButton.Add_Click({
            if ($script:window.FontSize -gt $script:window.Tag['MinFontSize']) {
                $script:window.FontSize -= 2
            }
        })
        [void] $zoomPanel.Children.Add($zoomOutButton)

        $zoomInButton = [Button] @{
            Content = "+"
            Width = 30
            Margin = "5,0,0,0"
        }
        $zoomInButton.Add_Click({
            if ($script:window.FontSize -lt $script:window.Tag['MaxFontSize']) {
                $script:window.FontSize += 2
            }
        })
        [void] $zoomPanel.Children.Add($zoomInButton)

        # Button panel (back, next, cancel)
        $buttonPanel = [StackPanel] @{
            Orientation = "Horizontal"
            HorizontalAlignment = "Right"
            Margin = "0,10,10,10"
        }
        [void] [Grid]::SetColumn($buttonPanel, 1)
        [void] $navGrid.Children.Add($buttonPanel)

        $script:backButton = [Button] @{
            Content = "Back"
            Width = 80
            Margin = "0,0,10,0"
            IsEnabled = $false
        }
        $backButton.Add_Click({ . $script:setPage -Previous })
        [void] $buttonPanel.Children.Add($backButton)

        $script:nextButton = [Button] @{
            Content = "Next"
            Width = 80
            Margin = "0,0,10,0"
        }
        $nextButton.Add_Click({ . $script:setPage -Next })
        [void] $buttonPanel.Children.Add($nextButton)

        $cancelButton = [Button] @{
            Content = "Cancel"
            Width = 80
            Margin = "0,0,10,0"
        }
        [void] $cancelButton.Add_Click($closeWindow)
        [void] $buttonPanel.Children.Add($cancelButton)
        #endregion Main Content

        # Set the first page content to start
        . $setPageContent -Page 0
        $window.Content = $grid
        return $window
    }
    #endregion Functions
    
}
Process {
    $window = Build-Window
    $window.ShowDialog()
}
