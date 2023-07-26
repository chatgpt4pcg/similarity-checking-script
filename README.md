# Similarity Checking Script

This repository contains a script for checking the similarity of text in images using a [fine-tuned version of `vit-base-patch16-224-in21k`](https://huggingface.co/pittawat/vit-base-letter) trained on a subset of the [port of CSV version](https://www.kaggle.com/datasets/sachinpatel21/az-handwritten-alphabets-in-csv-format) of [NIST Special Database 19](https://huggingface.co/datasets/pittawat/letter_recognition).

You can try an online demo of the model at [https://huggingface.co/spaces/pittawat/letter_recognizer](https://huggingface.co/spaces/pittawat/letter_recognizer).

## Installation

To use this script, you must have <a href="https://docs.conda.io/en/latest/" target="_new">conda</a> installed on your system.

1. Clone this repository to your local machine.
2. Navigate to the repository directory in your terminal.
3. Create the new conda environment or use an existing one by running `conda create -n chatgpt4pcg python=3.11`. Then activate the environment by running `conda activate chatgpt4pcg`.
4. Run `pip3 install -r requirements.txt` to install the necessary dependencies.

## Usage

1. Run `python3 main.py -s "<SOURCE_FOLDER>"` to start the similarity checking process. For example, `python3 main.py -s "./competition"`. In some cases, you may need to run `python main.py -s "./competition"` (`python` without `3`) instead.
2. The script will output the result in JSON format inside the `similarity` folder under the `<SOURCE_FOLDER>/<TEAM_FOLDER>/<CHARACTER>/similarity`. Files `similarity_log_<DATE_TIME>.txt` will be created inside `logs` folder.

Please note that `<STAGE>` can be `raw`, `intermediate`, `levels`, `images`, `stability`, or `similarity`. `<CHARACTER>` can be `A`, `B`, `C`, ..., `Z`.

Please ensure that the source folder has the following structure:

```
<SOURCE_FOLDER>
├── <TEAM_NAME>
|   ├── <STAGE>
│   │    └── <CHARACTER>
│   │       ├── <TRIAL_NUMBER>.jpg
│   │       ├── <TRIAL_NUMBER>.jpg
│   │       └── <TRIAL_NUMBER>.png
│   └── <STAGE>
│        └── <CHARACTER>
│           ├── <TRIAL_NUMBER>.txt
│           ├── <TRIAL_NUMBER>.txt
│           └── <TRIAL_NUMBER>.txt
└── <TEAM_NAME>
    ├── <STAGE>
    │    └── <CHARACTER>
    │       ├── <TRIAL_NUMBER>.jpg
    │       ├── <TRIAL_NUMBER>.png
    │       └── <TRIAL_NUMBER>.jpg
    └── <STAGE>
         └── <CHARACTER>
            ├── <TRIAL_NUMBER>.txt
            ├── <TRIAL_NUMBER>.txt
            └── <TRIAL_NUMBER>.txt
```

For example,

```
competition
├── team1
|   ├── images
│   │    └── I
│   │       ├── team1_I_1.jpg
│   │       ├── team1_I_2.jpg
│   │       └── team1_I_3.png
│   └── intermediate
│        └── I
│           ├── team1_I_1.txt
│           ├── team1_I_2.txt
│           └── team1_I_3.txt
└── team2
    ├── images
    │    └── A
    │       ├── team2_A_1.jpg
    │       ├── team2_A_2.png
    │       └── team2_A_3.jpg
    └── raw
         └── B
            ├── team2_B_1.txt
            ├── team2_B_2.txt
            └── team2_B_3.txt
```

## Contributing

If you would like to contribute to this project, please fork this repository and submit a pull request. Please ensure that your code is well documented and that you have tested your code before submitting a pull request.

## Bug Reporting

If you find any bugs, please submit an issue on this repository.