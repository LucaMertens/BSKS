import json
import os
import glob
from pathlib import Path
import uuid


def to_html(string):
    return string.replace("<", '&lt;').replace(">", '&gt;').replace("\n", "<br>")


def get_note_dict(question_dict, title, model_uuid):
    result = {
        "__type__": "Note",
        "fields":  [""] * 11,
        "guid": "",
        "note_model_uuid": model_uuid,
        "tags": ["BSKS_QUIZ", "automatic"]
    }
    result["fields"][0] = to_html(title)
    # The question
    result["fields"][1] = to_html(question_dict["question"])
    # The type of the card (1 means multiple choice)
    result["fields"][2] = "1"

    correct_answers_indicator = ""
    answer_index = 3

    for answer in question_dict["correctAnswers"]:
        result["fields"][answer_index] = to_html(answer)
        correct_answers_indicator += "1 "
        answer_index += 1

    for answer in question_dict["wrongAnswers"]:
        result["fields"][answer_index] = to_html(answer)
        correct_answers_indicator += "0 "
        answer_index += 1

    result["fields"][8] = correct_answers_indicator

    result["guid"] = str(uuid.uuid3(
        uuid.NAMESPACE_X500, "".join(result["fields"])))

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
    note_count = 0
    for filename in glob.iglob(json_path + '**/**/*.json', recursive=True):
        note_count += 1
        with open(filename, "r") as f:
            stem = Path(filename).stem
            question_dict = json.load(f)
            note_dict = get_note_dict(question_dict, stem, model_uuid)
            base["notes"].append(note_dict)
    write_deck(base, anki_path)
    print(f"Wrote {note_count} notes to the deck.")


json_path = os.path.join(os.getcwd(), "Quiz", "JSON")
anki_path = os.path.join(os.getcwd(), "Quiz", "anki")
convert_and_write_all(anki_path, json_path)
