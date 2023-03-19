# Similarity Checking Script

This repository contains a script for checking the similarity of text in images using Tesseract OCR.

## Installation

To use this script, you must have <a href="https://nodejs.org/en/" target="_new">Node.js</a> and <a href="https://www.npmjs.com/" target="_new">npm</a> installed on your system.

1. Clone this repository to your local machine.
2. Navigate to the repository directory in your terminal.
3. Run `npm install` to install the necessary dependencies.

## Usage

1. Run the script using the command `npm start -s="<SOURCE_FOLDER>"`. For example, `npm start -s="./test_images"`.
2. The script will output the recognized text and its confidence level for each image as a text file in the `similarity/<TARGET_CHARACTER>/<TRIAL_NUMBER>/`, which has the same structure as the source folder.. Files `_log_<DATE_TIME>.txt` and `_result_<DATE_TIME>.csv` will be created inside the same folder.

Please ensure that the source folder has the following structure:

```
<SOURCE_FOLDER>
├── <TARGET_CHARACTER>
│   ├── <TRIAL_NUMBER>
│   │   ├── <FILE_NAME>.jpg
│   │   ├── <FILE_NAME>.png
│   │   └── <FILE_NAME>.jpg
│   ├── <TRIAL_NUMBER>
│   │   ├── <FILE_NAME>.png
│   │   ├── <FILE_NAME>.png
│   │   └── <FILE_NAME>.png
│   └── <TRIAL_NUMBER>
│       ├── <FILE_NAME>.png
│       ├── <FILE_NAME>.png
│       └── <FILE_NAME>.jpg
└── <TARGET_CHARACTER>
    ├── <TRIAL_NUMBER>
    │   ├── <FILE_NAME>.png
    │   ├── <FILE_NAME>.png
    │   └── <FILE_NAME>.png
    ├── <TRIAL_NUMBER>
    │   ├── <FILE_NAME>.png
    │   ├── <FILE_NAME>.jpg
    │   └── <FILE_NAME>.png
    └── <TRIAL_NUMBER>
        ├── <FILE_NAME>.png
        ├── <FILE_NAME>.jpeg
        └── <FILE_NAME>.png
```