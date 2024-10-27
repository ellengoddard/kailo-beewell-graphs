Full macro 

Sub convert_and_format_rag()
    Dim folderPath As String
    Dim fileName As String
    Dim wb As Workbook
    Dim ws As Worksheet
    Dim csvFileName As String
    
    ' Set the folder path where CSV files are stored (correctly formatted for Mac)
    folderPath = "/Users/ellengoddard/Desktop/beewell_example_graphs/rag_ratings/"
    
    ' Get the first CSV file in the folder
    fileName = Dir(folderPath & "*.csv") ' This will get all CSV files in the folder
    
    ' Loop through all CSV files in the folder
    Do While fileName <> ""
        On Error GoTo SaveError ' Start error handling
        
        ' Open the CSV file
        Debug.Print "Opening file: " & folderPath & fileName
        Set wb = Workbooks.Open(folderPath & fileName, Local:=True) ' Open as a workbook
        
        ' Change the file format from CSV to a workbook format
        If wb.FileFormat = xlCSV Then
            Debug.Print "File opened as CSV, converting to XLSM"
        Else
            Debug.Print "File opened in a different format: " & wb.FileFormat
        End If
        
        ' Apply conditional formatting to each worksheet
        For Each ws In wb.Worksheets
            ApplyConditionalFormatting ws
        Next ws
        
        ' Prepare the new file name (convert .csv to .xlsm)
        csvFileName = Replace(fileName, ".csv", ".xlsm")
        
        ' Debug message to verify save path
        Debug.Print "Saving file as: " & folderPath & csvFileName
        
        ' Check if the file already exists, delete it to avoid overwrite issues
        If Dir(folderPath & csvFileName) <> "" Then
            Debug.Print "File exists, deleting first..."
            Kill folderPath & csvFileName ' Delete the existing file if it exists
        End If
        
        ' Save the workbook as a Macro-Enabled Workbook (.xlsm)
        Debug.Print "Saving workbook..."
        wb.SaveAs folderPath & csvFileName, FileFormat:=xlOpenXMLWorkbookMacroEnabled
        
        ' Close the workbook
        Debug.Print "Closing workbook..."
        wb.Close SaveChanges:=True
        
        ' Move to the next CSV file in the folder
        fileName = Dir
    Loop
    
    MsgBox "All CSV files have been converted and formatted!", vbInformation
    Exit Sub
    
SaveError:
    MsgBox "Error saving file: " & folderPath & csvFileName & vbCrLf & Err.Description
    On Error GoTo 0 ' Reset error handling
End Sub

' Subroutine to apply conditional formatting
Sub ApplyConditionalFormatting(ws As Worksheet)
    Dim rng As Range
    Dim ruleBad As FormatCondition, ruleNeutral As FormatCondition, ruleGood As FormatCondition

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
End Sub

