# Similarity Checking Script

This repository contains a script for checking the similarity of text in images using Tesseract OCR.

## Installation

To use this script, you must have <a href="https://nodejs.org/en/" target="_new">Node.js</a> and <a href="https://www.npmjs.com/" target="_new">npm</a> installed on your system.

1. Clone this repository to your local machine.
2. Navigate to the repository directory in your terminal.
3. Run `npm install` to install the necessary dependencies.

## Usage

1. Place the images to be analyzed in the `test_images` folder. Create one if not present.
2. Run the script using the command `npm start`.
3. The script will output the recognized text and its confidence level for each image as a text file in the `output` folder.
