# Similarity Checking Script

This repository contains a script for checking the similarity of text in images using a [fine-tuned version of `vit-base-patch16-224-in21k`](https://huggingface.co/pittawat/vit-base-letter) trained on a subset of the [port of CSV version](https://www.kaggle.com/datasets/sachinpatel21/az-handwritten-alphabets-in-csv-format) of [NIST Special Database 19](https://huggingface.co/datasets/pittawat/letter_recognition).

You can try an online demo of the model at [https://huggingface.co/spaces/pittawat/letter_recognizer](https://huggingface.co/spaces/pittawat/letter_recognizer).

## Installation

To use this script, you must have <a href="https://docs.conda.io/en/latest/" target="_new">conda</a> installed on your system.

1. Clone this repository to your local machine.
2. Navigate to the repository directory in your terminal.
3. Create the new conda environment or use an existing one by running `conda create -n chatgpt4pcg python=3.11`. Then activate the environment by running `conda activate chatgpt4pcg`.
4. Run `pip3 install -r requirements.txt` to install the necessary dependencies.
5. Run `pip3 install git+https://github.com/huggingface/transformers` to install the latest version of `transformers` from source. This is to prevent an unknown error when importing `AutoImageProcessor` from the package.

## Usage

1. Changing the variable `SOURCE_FOLDER` to your destination folder. Make sure the folder has the structure as described below.
2. Run `python3 main.py"` to start the similarity checking process.
3. The script will output the result in JSON format inside the `similarity` folder under the `SOURCE_FOLDER`. Files `similarity_log_<DATE_TIME>.txt` will be created inside `logs` folder.

Please ensure that the source folder has the following structure:

```
<SOURCE_FOLDER>
├── <TEAM_NAME>
|   ├── <STAGE>
│   │    └── <CHARACTER>
│   │       ├── <TRIAL_NUMBER>.jpg
│   │       ├── <TRIAL_NUMBER>.png
│   │       └── <TRIAL_NUMBER>.jpg
│   └── <STAGE>
│        └── <CHARACTER>
│           ├── <TRIAL_NUMBER>.png
│           ├── <TRIAL_NUMBER>.png
│           └── <TRIAL_NUMBER>.png
└── <TEAM_NAME>
    ├── <STAGE>
    │    └── <CHARACTER>
    │       ├── <TRIAL_NUMBER>.jpg
    │       ├── <TRIAL_NUMBER>.png
    │       └── <TRIAL_NUMBER>.jpg
    └── <STAGE>
         └── <CHARACTER>
            ├── <TRIAL_NUMBER>.png
            ├── <TRIAL_NUMBER>.png
            └── <TRIAL_NUMBER>.png
```
```