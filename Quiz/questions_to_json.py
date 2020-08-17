from extract_question import extract_question
import json
import os
import glob
from pathlib import Path


def write_dict_to_json(question_dict, dest_path):
    file = open(dest_path, "w+", encoding="utf-8")
    json.dump(question_dict, file)
    file.close()


def question_to_json(origin_path, dest_path):
    try:
        origin_string = open(origin_path, "r", encoding="utf-8").read()
        question_dict = extract_question(origin_string, origin_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        write_dict_to_json(question_dict, dest_path)
    except OSError as err:
        print(err)
    except SyntaxError as err:
        print("Quiz-Entry malformed: ", err)
    else:
        print(f"✅ {Path(dest_path).stem} succesfully converted.")


def questions_to_json(origin_root, dest_root):
    # Ignore files starting with a !.
    for filename in glob.iglob(origin_root + '**/**/[!!]*.txt', recursive=True):
        relative_path = os.path.relpath(os.path.dirname(filename), origin_root)
        raw_file_name = Path(filename).stem
        dest_filename = os.path.join(
            dest_root, relative_path, raw_file_name + ".json")

        question_to_json(filename, dest_filename)


origin = os.path.join(os.getcwd(), "Quiz")
dest = os.path.join(os.getcwd(), "JSON")
questions_to_json(origin, dest)
