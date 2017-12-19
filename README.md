# Defunct Interpreter

by Elijah John Shadbolt (Cresspresso)

Copyright (c) 2017    MIT Licence

Version 1.2

2017-12-19 13:56:40 +1300

## Description

This is the source code for the Defunct Interpreter, written in Python.

Defunct is a simplistic programming language based on pure Lambda Calculus.
It is terribly inefficient and slow, but it relies solely on the principles
of raw Lambda Calculus. Expressions of functions can be defined, referenced,
simplified, substituted, and executed.

## Software used during development

| Resource | Purpose |
| :--- | :--- |
| Python 3.6 | Runs the source code |
| Visual Studio Community 2017 | Text editor and IDE |
| PyInstaller 3.3 | Creates the binary .exe |

## Installation

Windows, Command Line only

1. [Click Here to Download v1.2 zip](https://github.com/Cresspresso/Defunct/releases/download/1.2/17-12-19_13-56-40_v1.2_defunct.zip), OR go to [Latest Release](https://github.com/Cresspresso/Defunct/releases/latest) and download the .zip file.

2. Unzip to somewhere memorable, like your Desktop.

3. Open the Command Prompt.

    To open the Command Prompt in Windows 10: right click Start > Command Prompt

4. Navigate to the unzipped folder by typing this command:

        cd "<your-unzipped-directory>\defunct\"

    For example, if you unzipped `17-12-19_13-56-40_v1.2_defunct.zip` to the Desktop:

        cd "C:\Users\<your-username>\Desktop\17-12-19_13-56-40_v1.2_defunct\defunct"

5. Use the following command to run `defunct.exe` on an example file:

        defunct "examples\example01.txt" -printinfo

    If installed correctly, it should come up with:

        Interpreting file at "examples/example01.txt"...
        3 :  [y x. y(y(y x))]
        ++ :  [w y x. y(w y x)]
        6 :  [y x. y(y(y(y(y(y x)))))]
        6 :  [y x. y(y(y(y(y(y x)))))]
        Finished interpreting file at "examples/example01.txt".
        No errors encountered.

    You can also get help with command-line arguments by running this command:

        defunct -help

## Licence

MIT License

Copyright (c) 2017 Elijah John Shadbolt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE


