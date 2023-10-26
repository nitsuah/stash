# VBA Automation for Mouse Movements and PDF Interaction

This repository contains Visual Basic for Applications (VBA) code for automating mouse movements and interactions with PDF files.

This VBA code is intended for use in a Microsoft Access environment with Adobe Acrobat installed. The code is designed to automate the process of splitting and filtering PDF files based on a notice type. The code can be used to split a PDF file into smaller chunks, and then filter the chunks based on a notice type. The code can also be used to generate random pages for a notice type. This allows for Randomized sampling of PDF files or mailing notices for manual review.

## Contents

- `gen` - output folder
- `setup` - test folder incluiding two sample files
  - `SAMPLER_MK2.sequ` - sequence file for Adobe split & filter test
  - `test.pdf` - PDF file for Adobe split & filter test
- `source` - source code used in accdb
- `temp` - temporary folder for storing split PDF files

## Prerequisites

This VBA code is intended for use in a Microsoft Access environment with Adobe Acrobat installed. Ensure that the required environment and references are properly set up.

## Features

### Mouse Movement Functions

The VBA code includes a set of functions for simulating mouse movements and clicks. These functions provide precise control over the mouse cursor's position and actions:

- `ActionBtn()`: Simulates a mouse click at coordinates (380, 60).
- `StartBtn()`: Simulates a mouse click at coordinates (1714, 222).
- `OKBtn()`: Simulates a mouse click at coordinates (826, 659).
- `CloseBtn()`: Simulates a mouse click at coordinates (1893, 8).
- `ExitBtn()`: Simulates a mouse click at coordinates (1893, 8).
- `SearchTxt()`: Simulates a mouse click at coordinates (1797, 353).
- `ClickCurr()`: Simulates a mouse click at coordinates (905, 390).
- `ClickRmv()`: Simulates a mouse click at coordinates (1083, 360).
- `ClickTxt()`: Simulates a mouse click at coordinates (905, 326).
- `AddTxt()`: Simulates a mouse click at coordinates (1087, 321).
- `ClickOk()`: Simulates a mouse click at coordinates (987, 760).
- `SingleClick()`: Simulates a single left-click at coordinates (100, 100).
- `DoubleClick()`: Simulates a double left-click at coordinates (100, 100).
- `RightClick()`: Simulates a right-click at coordinates (200, 200).
- `FinActBtn()`: Simulates a mouse click at coordinates (1150, 580).
- `AddActBtn()`: Simulates a mouse click at coordinates (1055, 570).
- `WHEREDICLICK()`: Retrieves and displays the current mouse cursor's X and Y coordinates.

### Utility Functions

Several utility functions are included:

- `Pause(NumberOfSeconds As Variant)`: Pauses the code execution for a specified number of seconds.
- `TypeNotice()`: Types a value stored in `TempVars!NTT` using the `SendKeys` function.
- `GotPixel(seconds As Integer)`: Gets the color of the pixel at the mouse cursor's position.

### PDF Interaction

Functions for interacting with PDF files are available:

- `PDFFS()`: Opens a PDF file named "test.pdf."
- `SEQUSET()`: Opens a PDF file named "SAMPLER_MK2.sequ" and performs a series of mouse clicks.
- `OpenFWS(strAddress As String)`: Opens a PDF file using the Adobe Acrobat application.
- `NoticeChunker()`: Splits and processes PDF files into smaller chunks based on a notice type, generating random pages.
- `RandomGen(maxpgct As Integer)`: Generates random page numbers based on `maxpgct` for a notice type.
- `FindMatchingValue(intValueToFind As Integer)`: Finds a matching value in a table for random page generation.
- `UpdateST()`: Updates the search text value based on the `TypeNotice` function.

### Calibration and Initialization - form-calibration.vb

Functions for calibration and initialization:

- `NewCalibration()`: Initiates a new calibration process, inserting editor information into a "Calibre" table.
- `ResetCalibrate()`: Checks the calibration status and provides an option to reset calibration data.
- `OnCalibrate()`: Logs the calibration event.
  