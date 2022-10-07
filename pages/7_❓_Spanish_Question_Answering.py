import streamlit as st
import tune_the_model as ttm
import pandas as pd
import numpy as np
import random

st.set_page_config(
        page_title="❓ Question Answering",
)

if 'question_gen' not in st.session_state:
    st.session_state['question_gen'] = ttm.TuneTheModel.from_id(
        '1da0fd05bb47b624a909ec15d5cdfdae'
    )

if 'question_answering' not in st.session_state:
    st.session_state['question_answering'] = ttm.TuneTheModel.from_id(
        '4750baa83e6e11ed92bd37630e193abd'
    )


if 'answer_checker' not in st.session_state:
    st.session_state['answer_checker'] = ttm.TuneTheModel.from_id(
        'bd4adc983e6e11ed855d6bb9c6ece3e5'
    )


question_gen = st.session_state['question_gen']
answer_checker = st.session_state['answer_checker']
question_answering = st.session_state['question_answering']


samples = [
    'El 6 de febrero de 2016, un día antes de su actuación en el super bowl, Beyoncé lanzó un nuevo single exclusivamente en el servicio de streaming de música Marea llamado formación.',
    'La temporada diez es la primera en incluir audiciones en línea donde los concursantes podrían presentar una audición de vídeo de 40 segundos a través de Myspace. Karen Rodríguez fue una de esas audicionante y llegó a las rondas finales.',
    'A partir de 2010/2011, hauptschulen se fusionaron con realschulen y gesamtschulen para formar un nuevo tipo de escuela integral en los estados alemanes de Berlín y Hamburgo, llamado stadtteilschule en Hamburgo y sekundärschule en Berlín (ver: Educación en Berlín, educación en Hamburgo).'
]


def choose(arr, prev):
    return random.choice(list(set(arr) - {prev}))


if 'qa_text' not in st.session_state:
    st.session_state['qa_text'] = random.choice(samples)


def create_qa_promp(context, question):
    return context + '\n\n' + question + '\n\n\n'


def create_checker_prompt(context, question, answer):
    return create_qa_promp(context, question) + answer


def generate_question(text):
    return question_gen.generate(text)[0]


@st.cache(show_spinner=False)
def answer_question(text, question):
    answers = question_answering.generate(
        create_qa_promp(text, question), num_hypos=8, temperature=0.8
    )
    return np.unique(answers)


@st.cache(show_spinner=False)
def score_answer(text, question, answer):
    return answer_checker.classify(
        create_checker_prompt(text, question, answer)
    )[0]


def main():
    st.title('Spanish Question Answering')

    'You can use both a tuned generator and a tuned classifier '\
        'to boost the quality of the entire system! '\
        'For example, You can tune a generator to answer questions, '\
        'and tune a classifier to to assess how far your answer is from '\
        'the gold one. After that You will be able to generate a lot of '\
        'different hypotheses and choose the best one!'

    if st.button('Give me example text!'):
        st.session_state['qa_text'] = choose(
            samples, st.session_state['qa_text']
        )
        st.session_state.pop('qa_question')

    text = st.text_area(
        'Main text',
        value=st.session_state['qa_text'],
        max_chars=500
    )

    if not text:
        st.error('Text must be nonempty.')
        return

    if st.button('Generate question') or\
        'qa_question' not in st.session_state:
        with st.spinner("Generating question using tuned generator..."):
            st.session_state['qa_question'] = generate_question(text)

    st.subheader('Question')
    real_question = st.text_input('Question', value=st.session_state['qa_question'])

    st.button('Generate an answer!')

    with st.spinner('Generating answer using tuned generator...'):
        answers = answer_question(text, real_question)

    pbar = st.progress(0)
    '-----'
    for i, ans in enumerate(answers):
        with st.spinner('Estimating answer quality using tuned classifier...'):
            score = score_answer(text, real_question, ans)

        st.markdown(f'## `{ans}`')
        st.write(f'${score*100:.1f}\%$ match')
        pbar.progress((i + 1) / len(answers))
        '-----'


if __name__ == '__main__':
    main()
