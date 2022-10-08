import streamlit as st
import core.utils
import core.spanish_question_answering
from core.constants import generation_warning
from samples.spanish_question_answering import samples

st.set_page_config(
    page_title="❓ Question Answering",
)

if 'question_gen' not in st.session_state:
    st.session_state['question_gen'] = \
        core.spanish_question_answering.get_question_gen()

if 'question_answering' not in st.session_state:
    st.session_state['question_answering'] = \
        core.spanish_question_answering.get_question_answering()


if 'answer_checker' not in st.session_state:
    st.session_state['answer_checker'] = \
        core.spanish_question_answering.get_answer_checker()


if 'qa_text' not in st.session_state:
    st.session_state['qa_text'] = core.utils.choose(samples)


def generate_question(text):
    return core.spanish_question_answering.generate_question(
        st.session_state['question_gen'],
        text
    )


@st.cache(show_spinner=False)
def answer_question(text, question):
    return core.spanish_question_answering.answer_question(
        st.session_state['question_answering'],
        text,
        question
    )


@st.cache(show_spinner=False)
def score_answer(text, question, answer):
    return core.spanish_question_answering.score_answer(
        st.session_state['answer_checker'],
        text,
        question,
        answer
    )


def main():
    st.title('Spanish Question Answering')

    'You can use both a tuned generator and a tuned classifier '\
        'to boost the quality of the entire system! '\
        'For example, You can tune a generator to answer questions, '\
        'and tune a classifier to to assess how far your answer is from '\
        'the gold one. After that You will be able to generate a lot of '\
        'different hypotheses and choose the best one!'

    if st.button('Give me example text!'):
        st.session_state['qa_text'] = core.utils.choose(
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
    real_question = st.text_input(
        'Question', value=st.session_state['qa_question'])
    st.caption(generation_warning)

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
