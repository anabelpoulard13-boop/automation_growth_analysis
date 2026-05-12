# Ensight Growth Analysis
This code take the data table from different plate size and generates a color-coded table to quickly identify passing and failing wells
based on a defined threshold.

## Requirement
For this code to work, you will need : 
- Outfile from the Ensight machine in .csv format
- Upload the document on momentum computer
- Libraries : pandas, matplotlib, numpy, string, os and argparse

## Feature
- Read and automatically detects the plate size (6, 12, 24, 96, 384 well plates)
- Colors each well green if the concentration is above or equal to the threshold and red if it is below
- Outputs two lists of wells — passed and failed — for quick review
  - Modify threshold value to change the list output and color grading

## Usage
When running this script, the user must provide the filepath of the file to analyze as well as the `threshold` value to apply. After execution, the program generates a heatmap displaying the wells that passed or failed the selected threshold and exports a `.csv` file containing a list of all wells that passed. Both output files are automatically saved in a newly created folder named `results`.

## Automation on Momentum
As you run a protocol on Momentum, you will add the `.exe` file on the computer running the code and make sure to name the version you are using to avoid any confusion. The momentum site will have a designated place to add the path of the file you want to analyse in `CSV` format. This step only needs to be done once during the entire process, as the code is designed to automatically access the path of the other files you want to analyse using the argument added on momentum. Then, for each file you want to analyse, you will input the desired threshold to use for the analysis. Finally, the code will output a heatmap image and a list of the passed wells, both saved in a folder named `results`, located in the same directory as your input file.
