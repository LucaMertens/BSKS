import re


def extract_question(input, filename):
    question_dict = {"question": "", "wrongAnswers": [], "correctAnswers": []}
    question_pattern = r"\s*((?:.|\n)+?)(?=(?:\n\s*?){3})"
    wrong_answer_pattern = r"\[ ?\]\s*((?:\n|.)+?)\s*(?=(?:\[(?: ?|X)\])|\Z)"
    correct_answer_pattern = r"\[X\]\s*((?:\n|.)+?)\s*(?=(?:\[(?: ?|X)\])|\Z)"

    # Seperate the string into its different parts.
    question = re.search(question_pattern, input)

    if (not question):
        raise SyntaxError("No question found in file: " + filename)
    if (re.search(wrong_answer_pattern, input, re.IGNORECASE) is None):
        raise SyntaxError(
            "Found a question, but no wrong answers for: " + filename)
    if (re.search(correct_answer_pattern, input, re.IGNORECASE) is None):
        raise SyntaxError(
            "Found a question, but no correct answers for: " + filename)

    wrong_answers = re.finditer(wrong_answer_pattern, input, re.IGNORECASE)
    correct_answers = re.finditer(correct_answer_pattern, input, re.IGNORECASE)

    # Save the different parts in the dict.
    question_dict["question"] = question.group()

    for match in wrong_answers:
        answer = match.group(1)
        question_dict["wrongAnswers"].append(answer)

    for match in correct_answers:
        answer = match.group(1)
        question_dict["correctAnswers"].append(answer)

    return question_dict
