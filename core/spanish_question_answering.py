import tune_the_model as ttm
import numpy as np


def get_question_gen():
    return ttm.TuneTheModel.from_id(
        '1da0fd05bb47b624a909ec15d5cdfdae'
    )


def get_question_answering():
    return ttm.TuneTheModel.from_id(
        '4750baa83e6e11ed92bd37630e193abd'
    )


def get_answer_checker():
    return ttm.TuneTheModel.from_id(
        'bd4adc983e6e11ed855d6bb9c6ece3e5'
    )


def create_qa_promp(context, question):
    return context + '\n\n' + question + '\n\n\n'


def create_checker_prompt(context, question, answer):
    return create_qa_promp(context, question) + answer


def generate_question(question_gen, text):
    return question_gen.generate(text)[0]


def answer_question(question_answering, text, question):
    answers = question_answering.generate(
        create_qa_promp(text, question), num_hypos=8, temperature=0.8
    )
    return np.unique(answers)


def score_answer(answer_checker, text, question, answer):
    return answer_checker.classify(
        create_checker_prompt(text, question, answer)
    )[0]
