import json
import os
import glob
from pathlib import Path


def to_html(string):
    return string.replace("<", '&lt;').replace(">", '&gt;').replace("\n", "<br>")


def get_note_dict(question_dict, title, model_uuid):
    result = {
        "__type__": "Note",
        "data": "",
        "fields":  [""] * 11,
        "flags": 0,
        "guid": "",
        "newlyAdded": True,
        "note_model_uuid": model_uuid,
        "tags": ["BSKS_QUIZ", "automatic"]
    }
    result["fields"][0] = title
    # The question
    result["fields"][1] = to_html(question_dict["question"])
    # The type of the card (1 means multiple choice)
    result["fields"][2] = "1"

    correct_answers_indicator = ""
    answer_index = 3

    for answer in question_dict["correctAnswers"]:
        answer.replace("\n", "<br>")
        result["fields"][answer_index] = to_html(answer)
        correct_answers_indicator += "1 "
        answer_index += 1

    for answer in question_dict["wrongAnswers"]:
        answer.replace("\n", "<br>")
        result["fields"][answer_index] = to_html(answer)
        correct_answers_indicator += "0 "
        answer_index += 1

    result["fields"][8] = correct_answers_indicator

    result["guid"] = hash("".join(result["fields"]))

    return result


def get_default_deck(anki_path):
    with open(os.path.join(anki_path, "base_deck.json"), "r") as f:
        return json.load(f)


def write_deck(deck, anki_path):
    folder = os.path.join(anki_path, "import_this_folder")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "deck.json"), "w+") as f:
        json.dump(deck, f)


def convert_and_write_all(anki_path, json_path):
    base = get_default_deck(anki_path)
    model_uuid = base["note_models"][0]["crowdanki_uuid"]
    for filename in glob.iglob(json_path + '**/**/*.json', recursive=True):
        with open(filename, "r") as f:
            stem = Path(filename).stem
            question_dict = json.load(f)
            note_dict = get_note_dict(question_dict, stem, model_uuid)
            base["notes"].append(note_dict)
    write_deck(base, anki_path)


json_path = os.path.join(os.getcwd(), "Quiz", "JSON")
anki_path = os.path.join(os.getcwd(), "Quiz", "anki")
convert_and_write_all(anki_path, json_path)
