import getopt
import json
import os
import string
import sys
from datetime import datetime
from pathlib import Path

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

device = torch.device("cpu")
if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")

MODEL_NAME = 'pittawat/vit-base-uppercase-english-characters'
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME).to(device)

LETTERS_LIST = list(string.ascii_uppercase)
RESULT_FOLDER_NAME = 'result'
LOG_FOLDER_NAME = 'logs'
INPUT_STAGE = 'images'
CURRENT_STAGE = 'similarity'
START_TIME = str(datetime.now().isoformat()).replace(":", "_").replace("/", "_")


def main(argv):
    opts, args = getopt.getopt(argv, "s:", ["source="])
    if opts is None:
        print('Please provide source folder')
        sys.exit(2)

    source_folder = ''
    for opt, arg in opts:
        if opt in ("-s", "--source"):
            source_folder = Path(arg)
            print(f'Source folder: {source_folder}')

    log_folder = create_log_folder(source_folder)
    teams = list_all_dirs(source_folder)
    for team in teams:
        team_log = f'[{str(datetime.now().isoformat())}] Processing - team: {team}'
        append_log(str(log_folder), team_log)
        path1 = Path(source_folder, team)
        characters = list_characters_dirs(str(path1), INPUT_STAGE)
        if characters is not None:
            for character in characters:
                character_log = f'[{str(datetime.now().isoformat())}] Processing - team: {team} - character: {character}'
                append_log(str(log_folder), character_log)
                path2 = Path(path1, INPUT_STAGE, character)
                trials = list_all_files(str(path2))

                output = {
                    'count': len(trials),
                    'similarityRate': 0,
                    'trials': [],
                    'similarities': []
                }

                similarity_rate = 0

                if trials is not None:
                    for trial in trials:
                        trial_log = (f'[{str(datetime.now().isoformat())}] Processing - team: {team} - character: '
                                     f'{character} - trial: {trial}')
                        append_log(str(log_folder), trial_log)
                        file_path = Path(path2, trial)
                        raw_result = predict(str(file_path), trial)
                        output['similarities'].append({
                            'id': trial,
                            'raws': raw_result
                        })
                        target_prob = search('label', character, raw_result)
                        output['trials'].append({
                            'id': trial,
                            'label': character,
                            'similarity': target_prob[0]['softmax_prob']
                        })
                        similarity_rate += target_prob[0]['softmax_prob']

                output['similarityRate'] = similarity_rate / len(trials)
                json_output = json.dumps(output, indent=2)
                output_path = create_output_folder(str(path2), CURRENT_STAGE, INPUT_STAGE)
                output_file_path = Path(output_path, f'{character}.json')
                with open(output_file_path, 'w') as f:
                    f.write(json_output)


def predict(file_path: str, file_name: str):
    image = Image.open(file_path)
    image = image.convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    outputs = model(**inputs)
    logits = outputs.logits
    softmax_outputs = torch.nn.Softmax(dim=-1)(logits)

    output_list = []
    for char in LETTERS_LIST:
        target_prob = softmax_outputs[0][ord(char.upper()) - 65]
        output_list.append({
            'id': file_name,
            'label': char,
            'softmax_prob': target_prob.item()
        })
    return output_list


def search(key, val, arr):
    return [el for el in arr if el[key] == val]


def list_all_dirs(source_folder: str):
    for (_, dirnames, _) in os.walk(source_folder):
        temp = dirnames
        out = []
        for t in temp:
            path = Path(source_folder, t)
            if os.path.isdir(path) and not t.startswith('.') and t != LOG_FOLDER_NAME and t != RESULT_FOLDER_NAME:
                out.append(t)
        return out


def list_all_files(source_folder: str):
    for (_, _, filenames) in os.walk(source_folder):
        temp = []
        for filename in filenames:
            if not filename.endswith('_raw.png'):
                temp.append(filename)
        return temp


def list_characters_dirs(source_folder: str, stage: str):
    path = Path(source_folder, stage)
    characters = list_all_dirs(str(path))
    return characters


def create_output_folder(path: str, output_folder_name: str, stage: str):
    if sys.platform == 'win32':
        root, team, stage_folder = "\\".join(str(path).split('\\')[0:-3]), str(path).split('\\')[-3], str(path).split(
            '\\')[-2:-1]
    else:
        root, team, stage_folder = "/".join(str(path).split('/')[0:-3]), str(path).split('/')[-3], str(path).split('/')[
                                                                                                   -2:-1]

    output_dir = Path(root, team, output_folder_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    current_dir = Path(output_dir)
    for folder in stage_folder:
        if folder == stage:
            continue
        current_dir = Path(current_dir, folder)
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)
    return current_dir


def create_log_folder(source_folder: str):
    output_dir = Path(source_folder, LOG_FOLDER_NAME)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def append_log(log_folder_path: str, log: str):
    print(log)
    log_file_path = Path(log_folder_path, f'similarity_log_{START_TIME}.txt')
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as f:
            f.write('')
    with open(log_file_path, 'a') as f:
        f.write(f'{log}\n')


if __name__ == '__main__':
    main(sys.argv[1:])
