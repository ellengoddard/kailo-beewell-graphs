Sub SaveCSVAsXLSMAndApplyFormatting()
    Dim folderPath As String
    Dim xlsmFolderPath As String
    Dim fileName As String
    Dim wb As Workbook
    Dim newFileName As String

    ' Set the path to the folder containing CSV files
    folderPath = #filepath here <-- Adjust path if needed
    
    ' Set the path for the xlsm subfolder
    xlsmFolderPath = folderPath & "xlsm/"

    ' Create the xlsm folder if it doesn't exist
    If Dir(xlsmFolderPath, vbDirectory) = "" Then
        MkDir xlsmFolderPath
    End If
    
    ' Get the first CSV file in the folder
    fileName = Dir(folderPath & "*.csv")

    ' Loop through all CSV files in the folder
    Do While fileName <> ""
        ' Open the CSV file
        Set wb = Workbooks.Open(folderPath & fileName)
        
        ' Create the new file name with .xlsm extension in the xlsm subfolder
        newFileName = Replace(fileName, ".csv", ".xlsm")
        
        ' Save the workbook as .xlsm in the xlsm subfolder
        wb.SaveAs fileName:=xlsmFolderPath & newFileName, FileFormat:=xlOpenXMLWorkbookMacroEnabled
        
        ' Close the workbook
        wb.Close False
        
        ' Move to the next CSV file
        fileName = Dir
    Loop

    ' Apply formatting to all xlsm files in the xlsm subfolder
    fileName = Dir(xlsmFolderPath & "*.xlsm")
    
    Do While fileName <> ""
        ' Open each .xlsm file in the xlsm subfolder
        Set wb = Workbooks.Open(xlsmFolderPath & fileName)
        
        ' Apply conditional formatting to each worksheet
        Dim ws As Worksheet
        For Each ws In wb.Worksheets
            ApplyConditionalFormatting ws
        Next ws
        
        ' Save and close the workbook
        wb.Close SaveChanges:=True
        
        ' Move to the next .xlsm file
        fileName = Dir
    Loop

    MsgBox "All CSV files have been saved as .xlsm files and formatted."
End Sub

' Subroutine to apply conditional formatting
Sub ApplyConditionalFormatting(ws As Worksheet)
    Dim rng As Range
    Dim ruleBad As FormatCondition, ruleNeutral As FormatCondition
    Dim ruleGood As FormatCondition, ruleSpecial As FormatCondition

    ' Define the range to apply formatting (using UsedRange for the whole sheet)
    Set rng = ws.UsedRange
    
    ' Clear any existing conditional formatting
    rng.FormatConditions.Delete
    
    ' Apply "Bad" (Red) formatting for "Below average"
    Set ruleBad = rng.FormatConditions.Add(Type:=xlCellValue, Operator:=xlEqual, Formula1:="=""Below average""")
    ruleBad.Interior.Color = RGB(255, 199, 206)  ' Light red background
    ruleBad.Font.Color = RGB(156, 0, 6)         ' Dark red font

    ' Apply "Neutral" (Yellow) formatting for "Average"
    Set ruleNeutral = rng.FormatConditions.Add(Type:=xlCellValue, Operator:=xlEqual, Formula1:="=""Average""")
    ruleNeutral.Interior.Color = RGB(255, 235, 156) ' Light yellow background
    ruleNeutral.Font.Color = RGB(156, 101, 0)      ' Brownish yellow font

    ' Apply "Good" (Green) formatting for "Above average"
    Set ruleGood = rng.FormatConditions.Add(Type:=xlCellValue, Operator:=xlEqual, Formula1:="=""Above average""")
    ruleGood.Interior.Color = RGB(198, 239, 206)   ' Light green background
    ruleGood.Font.Color = RGB(0, 97, 0)           ' Dark green font

    ' Apply "Special" (Blue) formatting for "n<10"
    Set ruleSpecial = rng.FormatConditions.Add(Type:=xlCellValue, Operator:=xlEqual, Formula1:="=""n<10""")
    ruleSpecial.Interior.Color = RGB(220, 227, 255) ' Light blue background
    ruleSpecial.Font.Color = RGB(26, 83, 154)       ' Dark blue font
End Sub
