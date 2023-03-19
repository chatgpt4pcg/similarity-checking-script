# Similarity Checking Script

This repository contains a script for checking the similarity of text in images using Tesseract OCR.

## Installation

To use this script, you must have <a href="https://nodejs.org/en/" target="_new">Node.js</a> and <a href="https://www.npmjs.com/" target="_new">npm</a> installed on your system.

1. Clone this repository to your local machine.
2. Navigate to the repository directory in your terminal.
3. Run `npm install` to install the necessary dependencies.

## Usage

1. Run the script using the command `npm start -s="<SOURCE_FOLDER>" -t="<TARGET_CHARACTER>`. For example, `npm start -s="./test_images" -t="I"`.
2. The script will output the recognized text and its confidence level for each image as a text file in the `output/<TARGET_CHARACTER>/` folder. Files `_log_<DATE_TIME>.txt` and `_result_<DATE_TIME>.csv` will be created inside the same folder.
