function Start-Cowriter {
    [Alias('Cowriter')]
    [CmdletBinding()]
    param (
        [string] $Xaml = "$PSScriptRoot/files/xaml/cowriter.xaml",
        [string] $OllamaUrl = 'http://127.0.0.1:11434/api',
        [string] $SystemPrompt = "$PSScriptRoot/files/prompts/system.txt"
    )
    Add-Type -AssemblyName PresentationFramework

    # Load XAML
    [xml]$xaml = Get-Content -Raw -Path $Xaml
    $reader = (New-Object System.Xml.XmlNodeReader $xaml)
    $script:window = [Windows.Markup.XamlReader]::Load($reader)
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
    $chatHistory.Tag = @{ Messages = [System.Collections.ArrayList]::new() }
    [void] $chatHistory.Tag['Messages'].Add(@{
        role = 'system'
        content = [string] (Get-Content $SystemPrompt)
    })
    $script:addChatBubble = {
        param (
            [Parameter(Position=0)]
            [string] $Message,
            [ValidateSet('User','AI')]
            [string] $Type = 'User',
            [int] $CornerRadius = 10,
            [int] $Padding = 8,
            [int] $Margin = 4,
            [int] $MaxWidth = 400,
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

    $script:sendMessage = {
        if ([string]::IsNullOrWhiteSpace($script:chatInput.Text)) {
            return
        }
        $message = $script:chatInput.Text
        $script:sendButton.IsEnabled = $false
        . $script:addChatBubble -Type User -Message $message
        $script:chatInput.Clear()
        [void] $script:chatHistory.Tag['Messages'].Add(@{
            role = 'user'
            content = $message
        })
        [System.Management.Automation.PowerShell]::Create().AddScript({
            param (
                $w,
                $ch,
                $q,
                $m = 'llama3.2',
                $OllamaUrl,
                $ml
            )
            $body = @{
                model = $m
                messages = $ml
                # prompt = $q
                stream = $false
            } | ConvertTo-Json -Depth 10 -Compress
            try {
                $result = Invoke-RestMethod "$OllamaUrl/chat" -method post -body $body -ErrorAction Stop
                $message = $result.message
                $content = $message.content
            } catch {
                $content = "Error: $($_.Exception.Message)"
            }
            $w.Dispatcher.Invoke({
                $ch.AddChild(
                    [System.Windows.Controls.Border] @{
                        CornerRadius = 10
                        Padding = 8
                        Margin = 4
                        HorizontalAlignment = 'Left'
                        Background = 'LightGray'
                        MaxWidth = 400
                        Child = [System.Windows.Controls.TextBlock] @{
                            Text = $content
                            TextWrapping = 'Wrap'
                        }
                        Tag = @{
                            Type = 'AI'
                        }
                    }
                )
                [void] $ch.Tag['Messages'].Add($message)
            })
        }).AddParameters(@{
            w = $script:window
            ch = $script:chatHistory
            q = $message
            OllamaUrl = $OllamaUrl
            ml = $script:chatHistory.Tag['Messages']
        }).BeginInvoke()
    }
    $sendButton.Add_Click($sendMessage)
    $chatInput.Add_KeyDown({
        param($sender, $e)
        if ($e.Key -in [System.Windows.Input.Key]::Enter, [System.Windows.Input.Key]::Return) {
            $script:sendMessage.Invoke()
            $e.Handled = $true
        }
    })

    # Show window
    $window.ShowDialog()
}
