function Start-Cowriter {
    [Alias('Cowriter')]
    [CmdletBinding()]
    param (
        [string] $Xaml = "$PSScriptRoot/files/xaml/cowriter.xaml",
        [uri] $OllamaUrl = 'http://127.0.0.1:11434'
    )
    Add-Type -AssemblyName PresentationFramework

    # Load XAML
    [xml]$xaml = Get-Content -Raw -Path $Xaml
    $reader = (New-Object System.Xml.XmlNodeReader $xaml)
    $window = [Windows.Markup.XamlReader]::Load($reader)
    $mainText = $window.FindName("MainText")
    $lineNumbers = $window.FindName("LineNumbers")

    # Logic for the text lines
    $lines_loaded = {
        $visibleLines = [Math]::Ceiling($mainText.ViewportHeight / $mainText.FontSize)
        $totalLines = [Math]::Max($mainText.LineCount, $visibleLines)
        $nums = ""
        for ($i=1; $i -le $totalLines; $i++) { $nums += "$i`n" }
        $lineNumbers.Text = $nums
    }
    $lines_textChanged = {
        $visibleLines = [Math]::Ceiling($mainText.ViewportHeight / $mainText.FontSize)
        $totalLines = [Math]::Max($mainText.LineCount, $visibleLines)
        $textLines = $mainText.Text -split "`n"
        $nums = ""
        for ($i=1; $i -le $totalLines; $i++) { $nums += "$i`n" }
        $lineNumbers.Text = $nums
    }
    $mainText.Add_Loaded($lines_loaded)
    $mainText.Add_TextChanged($lines_textChanged)

    # Logic for the formatting buttons
    $boldButton = $window.FindName("BoldButton")
    $italicButton = $window.FindName("ItalicButton")
    $underlineButton = $window.FindName("UnderlineButton")
    $bulletButton = $window.FindName("BulletButton")
    $numberButton = $window.FindName("NumberButton")

    # Bold
    $boldButton.Add_Click({
        $mainText.Selection.ApplyPropertyValue([System.Windows.Documents.Inline]::FontWeightProperty, [System.Windows.FontWeights]::Bold)
    })
    # Italic
    $italicButton.Add_Click({
        $mainText.Selection.ApplyPropertyValue([System.Windows.Documents.Inline]::FontStyleProperty, [System.Windows.FontStyles]::Italic)
    })

    # Underline
    $underlineButton.Add_Click({
        $mainText.Selection.ApplyPropertyValue([System.Windows.Documents.Inline]::TextDecorationsProperty, [System.Windows.TextDecorations]::Underline)
    })

    $script:chatInput = $window.FindName('ChatInput')
    $script:sendButton = $window.FindName('SendButton')
    $sendButton.Add_Loaded({
        $this.IsEnabled = $false
    })
    $chatInput.Add_TextChanged({
        $script:sendButton.IsEnabled = -not [string]::IsNullOrWhiteSpace($script:chatInput.Text)
    })

    $script:chatHistory = $window.FindName('ChatHistory')
    $script:addChatBubble = {
        param (
            [Parameter(Position=0)]
            [string] $Message,
            [ValidateSet('User','AI')]
            [string] $Type = 'User',
            [int] $CornerRadius = 10,
            [int] $Padding = 8,
            [int] $Margin = 4,
            [int] $MaxWidth = 200,
            [System.Windows.TextWrapping] $TextWrapping = 'Wrap',
            $ChatHistory = $script:chatHistory
        )
        $Background = switch ($Type) {
            'User' { 'LightBlue' }
            'AI'   { 'LightGray' }
        }
        [System.Windows.HorizontalAlignment] $HorizontalAlignment = switch ($Type) {
            'User' { 'Right' }
            'AI'   { 'Left' }
        }
        $ChatHistory.AddChild(
            [System.Windows.Controls.Border] @{
                CornerRadius = $CornerRadius
                Padding = $Padding
                Margin = $Margin
                HorizontalAlignment = $HorizontalAlignment
                Background = $Background
                MaxWidth = $MaxWidth
                Child = [System.Windows.Controls.TextBlock] @{
                    Text = $Message
                    TextWrapping = $TextWrapping
                }
                Tag = @{
                    Type = $Type
                }
            }
        )
    }
    $script:addUserBubble = {
        param ($Message)
        . $script:addChatBubble -Message $Message
    }
    $script:addAIBubble = {
        param ($Message)
        . $script:addChatBubble -Message $Message -Background LightGray -HorizontalAlignment Left
    }
    $sendButton.Add_Click({
        if ([string]::IsNullOrWhiteSpace($script:chatInput.Text)) {
            return
        }
        . $script:addChatBubble -Type User -Message $script:chatInput.Text
        $script:chatInput.Clear()
        start-sleep -sec 10
        . $script:addChatBubble -Type AI -Message 'This is a placeholder response from the AI.' -ChatHistory $script:chatHistory
    })
    $chatInput.Add_KeyDown({
        param($sender, $e)
        if ($e.Key -eq [System.Windows.Input.Key]::Enter) {
            # Your action here, e.g. send message
            [System.Windows.MessageBox]::Show("Enter pressed!")
            $e.Handled = $true  # Optional: prevents beep or further processing
        }
    })

    # Show window
    $window.ShowDialog()
}
