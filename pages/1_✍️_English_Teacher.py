import tune_the_model as ttm
import streamlit as st
from nltk.corpus import stopwords
import re
import random
import numpy as np
import importlib
utils = importlib.import_module("0_🤖_Tune_The_Model")

st.set_page_config(
        page_title="✍️ English Teacher",
)

if 'paraphraser' not in st.session_state:
    st.session_state['paraphraser'] = ttm.TuneTheModel.from_id(
        '541fec94231711ed9937e9f0fc1f297c'
    )
paraphraser = st.session_state['paraphraser']

if 'storygen' not in st.session_state:
    st.session_state['storygen'] = ttm.TuneTheModel.from_id(
        '617e1c34211b6878000b0af4a5ca8308'
    )
storygen = st.session_state['storygen']

stop = stopwords.words('english')

samples = [
    'Hapy birfday my dear frend!',
    'Therefore, it is strongly recommended to regular treat items with disinfectants.',
    'As for me, I think that ecology it\'s not the separated part of our life, but one of the biggest parts of that.'
]

if 'eng_teacher_input' not in st.session_state:
    st.session_state['eng_teacher_input'] = random.choice(samples)


def choose(arr, prev):
    return random.choice(list(set(arr) - {prev}))


def extract_words(text):
    return re.findall(r'[a-z]+', text.lower())


@st.cache(show_spinner=False)
def improve_text(text):
    return paraphraser.generate(text, temperature=0.2)[0]


@st.cache(show_spinner=False)
def make_up_a_story(keywords):
    for _ in range(10):
        if len(keywords) > 5:
            selected_keywords = np.random.choice(
                keywords,
                size=5,
                replace=False
            )
        else:
            selected_keywords = keywords
        gens = storygen.generate(', '.join(selected_keywords), num_hypos=3)
        for story in gens:
            story = re.sub(r'([.!?])[^.!?]+$', r'\1', story)
            with st.spinner("Checking if story is not harmful using tuned classifier..."):
                if utils.pass_moderation(story):
                    return story
    return ' '.join(keywords)


def main():
    st.title('English Teacher')

    if st.button('Give me an example!'):
        st.session_state['eng_teacher_input'] = choose(
            samples, st.session_state['eng_teacher_input']
        )

    inp = st.text_area(
        'Your phrase', value=st.session_state['eng_teacher_input'],
        max_chars=250
    )

    st.button('Improve my text!')

    if utils.is_fraud(inp):
        st.warning('Your text is a bit unusual, the results may be bad')

    with st.spinner("Improving your text using tuned generator..."):
        correct = improve_text(inp)

    if correct == inp:
        st.info(
            'Your text is already pretty cool!\n'
            'Try another text with some mistakes.'
        )
        return

    st.subheader('We would suggest you to correct your text:')
    st.markdown(f'## `{correct}`')

    text_p = extract_words(inp)
    gen_p = extract_words(correct)

    new_words = list(set(gen_p) - set(text_p) - set(stop))

    if not new_words:
        st.info('There are no new words for you this time, you did well!')
        return

    '------'

    st.subheader('Some words for you to practice:')
    for word in new_words:
        st.markdown(f'## `{word}`')

    st.subheader('And cool generated story for better memorization!')
    with st.spinner("Making up a story using tuned generator..."):
        story = make_up_a_story(new_words)
    st.markdown(f'## `{story}`')


if __name__ == '__main__':
    main()
