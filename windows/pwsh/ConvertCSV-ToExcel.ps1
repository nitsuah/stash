    Function Release-Ref ($ref)
{
    ([System.Runtime.InteropServices.Marshal]::ReleaseComObject(
    [System.__ComObject]$ref) -gt 0)
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers() 
}

    Function Convert-CSVToExcel
{
    <#   
    .SYNOPSIS  
        Converts one or more CSV files into an Excel file.
        
    .DESCRIPTION  
        Converts one or more CSV files into an Excel file. Each CSV file is imported into its own worksheet with the name of the
        file being the name of the worksheet.
        
    .PARAMETER inputfile
        Name of the CSV file being converted

    .PARAMETER output
        Name of the converted Excel file
        
    .EXAMPLE  
        Get-ChildItem *.csv | Convert-CSVToExcel -output 'report.xlsx'

    .EXAMPLE  
        Convert-CSVToExcel -inputfile 'file.csv' -output 'report.xlsx'
        
    .EXAMPLE      
        Convert-CSVToExcel -inputfile @("test1.csv","test2.csv") -output 'report.xlsx'

    .EXAMPLE 
        . .\ConvertCSV-ToExcel
        Get-ChildItem *.csv | ConvertCSV-ToExcel -output 'users.xls' 

    .NOTES
        Author: Boe Prox									      
        Date Created: 01SEPT210								      
        Last Modified:
        Author: Austin Hardy									      
        Date Modified: 20231024
    #>
    
    #Requires -version 2.0  
    [CmdletBinding(
        SupportsShouldProcess = $True,
        ConfirmImpact = 'low',
        DefaultParameterSetName = 'file'
    )]
    Param (    
        [Parameter(
        ValueFromPipeline=$True,
        Position=0,
        Mandatory=$True,
        HelpMessage="Name of CSV/s to import")]
        [ValidateNotNullOrEmpty()]
        [array]$inputfile,
        
        [Parameter(
        ValueFromPipeline=$False,
        Position=1,
        Mandatory=$True,
        HelpMessage="Name of Excel file output")]
        [ValidateNotNullOrEmpty()]
        [string]$output    
    )

    Begin {     
        # Configure regular expression to match full path of each file
        [regex]$regex = "^\w\:\\"
        
        # Create Excel Com Object
        $excel = New-Object -ComObject Excel.Application
        
        # Disable alerts
        $excel.DisplayAlerts = $False

        # Show Excel application
        $excel.Visible = $False

        # Add workbook
        $workbook = $excel.Workbooks.Add()

        # Define initial worksheet number
        $i = 1
    }

    Process {
        ForEach ($input in $inputfile) {
            # If more than one file, create another worksheet for each file
            If ($i -gt 1) {
                $workbook.Worksheets.Add() | Out-Null
            }
            
            # Use the first worksheet in the workbook (also the newest created worksheet is always 1)
            $worksheet = $workbook.Worksheets.Item(1)
            
            # Add name of CSV as worksheet name
            $worksheet.Name = "$((Get-ChildItem $input).BaseName)"

            # Open the CSV file in Excel, must be converted into complete path if not already done
            If ($regex.IsMatch($input)) {
                $tempcsv = $excel.Workbooks.Open($input) 
            }
            ElseIf ($regex.IsMatch("$($input.FullName)")) {
                $tempcsv = $excel.Workbooks.Open("$($input.FullName)") 
            }    
            Else {    
                $tempcsv = $excel.Workbooks.Open("$($pwd)\$input")      
            }
            
            $tempsheet = $tempcsv.Worksheets.Item(1)
            
            # Copy contents of the CSV file
            $tempsheet.UsedRange.Copy() | Out-Null
            
            # Paste contents of CSV into the existing workbook
            $worksheet.Paste()

            # Close temp workbook
            $tempcsv.Close()

            # Select all used cells
            $range = $worksheet.UsedRange

            # Autofit the columns
            $range.EntireColumn.Autofit() | Out-Null
            $i++
        } 
    }

    End {
        # Save spreadsheet
        $targetPath = "$pwd\$output"
        if ($PSCmdlet.ShouldProcess("Save spreadsheet to $targetPath")) {
            $workbook.SaveAs($targetPath)
        }

        Write-Host -ForegroundColor Green "File saved to $targetPath"

        # Close Excel
        if ($PSCmdlet.ShouldProcess("Quit Excel")) {
            $excel.Quit()
        }

        # Release processes for Excel
        if ($PSCmdlet.ShouldProcess("Release processes for Excel")) {
            Release-Ref $range
        }
    }
}
