import os
import json
import string
from sys import platform
from pathlib import Path
from datetime import datetime

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

processor = AutoImageProcessor.from_pretrained("pittawat/vit-base-letter")
model = AutoModelForImageClassification.from_pretrained("pittawat/vit-base-letter")

LETTERS_LIST = list(string.ascii_uppercase)
SOURCE_FOLDER = Path('./competition')
LOG_FOLDER_NAME = 'logs'
STAGE = 'images'
OUTPUT_NAME = 'similarity'
START_TIME = str(datetime.now().isoformat()).replace(":", "_")


def main():
    log_folder = create_log_folder(SOURCE_FOLDER)
    teams = list_all_dirs(SOURCE_FOLDER)
    for team in teams:
        team_log = f'[{str(datetime.now().isoformat()).replace(":", "_")}] Processing - team: {team}'
        append_log(log_folder, team_log)
        path1 = Path(SOURCE_FOLDER, team)
        characters = list_characters_dirs(path1, STAGE)
        if characters is not None:
            for character in characters:
                character_log = f'[{str(datetime.now().isoformat()).replace(":", "_")}] Processing - team: {team} - character: {character}'
                append_log(log_folder, character_log)
                path2 = Path(path1, STAGE, character)
                trials = list_all_files(path2)

                output = {
                    'count': len(trials),
                    'similarityRate': 0,
                    'similarities': []
                }

                similarity_rate = 0

                if trials is not None:
                    for trial in trials:
                        trial_log = f'[{str(datetime.now().isoformat()).replace(":", "_")}] Processing - team: {team} - character: {character} - trial: {trial}'
                        append_log(log_folder, trial_log)
                        file_path = Path(path2, trial)
                        raw_result = predict(file_path, trial)
                        output['similarities'].append(raw_result)
                        target_prob = search('label', character, raw_result)
                        similarity_rate += target_prob[0]['softmax_prob']

                output['similarityRate'] = similarity_rate / len(trials)
                json_output = json.dumps(output, indent=2)
                output_path = create_output_folder(path2, OUTPUT_NAME, STAGE)
                output_file_path = Path(output_path, f'{character}.json')
                with open(output_file_path, 'w') as f:
                    f.write(json_output)


def predict(filePath, fileName):
    image = Image.open(filePath)
    image = image.convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    softmax_outputs = torch.nn.Softmax(dim=-1)(logits)

    output_list = []
    for char in LETTERS_LIST:
        target_prob = softmax_outputs[0][ord(char.upper()) - 65]
        output_list.append({
            'id': fileName,
            'label': char,
            'softmax_prob': target_prob.item()
        })
    return output_list


def search(key, val, arr):
    return [el for el in arr if el[key] == val]


def list_all_dirs(source_folder):
    for (_, dirnames, _) in os.walk(source_folder):
        temp = dirnames
        out = []
        for t in temp:
            path = Path(source_folder, t)
            if os.path.isdir(path) and not t.startswith('.') and t != LOG_FOLDER_NAME:
                out.append(t)
        return out


def list_all_files(source_folder):
    for (_, _, filenames) in os.walk(source_folder):
        return filenames


def list_characters_dirs(source_folder, stage):
    path = Path(source_folder, stage)
    characters = list_all_dirs(path)
    return characters


def create_output_folder(path, output_folder_name, stage):
    if platform == 'win32':
        root, team, folders = str(path).split('\\')[0], str(path).split('\\')[1], str(path).split('\\')[2:-1]
    else:
        root, team, folders = str(path).split('/')[0], str(path).split('/')[1], str(path).split('/')[2:-1] # skip the character folder

    output_dir = Path(root, team, output_folder_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    current_dir = Path(output_dir)
    for folder in folders:
        if folder == stage:
            continue
        current_dir = Path(current_dir, folder)
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)
    return current_dir


def create_log_folder(source_folder):
    output_dir = Path(source_folder, LOG_FOLDER_NAME)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def append_log(log_folder_path, log):
    print(log)
    log_file_path = Path(log_folder_path, f'similarity_log_{START_TIME}.txt')
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as f:
            f.write('')
    with open(log_file_path, 'a') as f:
        f.write(f'{log}\n')


if __name__ == '__main__':
    main()
