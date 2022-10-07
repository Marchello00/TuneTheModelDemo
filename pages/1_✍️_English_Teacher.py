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
        # '617e1c34211b6878000b0af4a5ca8308'  # all rocstories
        '8d6ab260b4d2db23ae16a9eca582c625'  # only positive rocstories
    )
storygen = st.session_state['storygen']

stop = stopwords.words('english')

samples = [
    'Hapy birfday my dear frend!',
    'Therefore, it is strongly recommended to regular treat items with disinfectants.',
    'As for me, I think that ecology it\'s not the separated part of our life, but one of the biggest parts of that.',
    'And never think that the best profession is where a lot of money. Many people work and feel yourself the worst with every day and afraid change this, because this stability.',
    'Nowadays you can learn it all in college after you acquire a qualification of a mason, a painter, a roofer or, for example, an electricians.',
    'People even invented a toothpaste that you can eat so you save even more time by not breakfasting at all. But there are people who just cannot stand it.',
    'If people know and remember the dangers of electric current, they will be able to protect themselves and their loved ones from its effects.'
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
    c1, c2 = st.columns([3, 1])
    c1.title('English Teacher')
    smalltalk_logl_url = 'https://static.tildacdn.com/tild3431-6362-4434-b336-393736666264/logo_smalltalk.svg'
    smalltalk_url = 'https://smalltalk2.me/'
    c2.markdown(f"[![SmallTalk]({smalltalk_logl_url})]({smalltalk_url})")

    'You can tune the model to correct the student\'s mistakes automatically!'
    'Moreover, you can automatically extract words with mistakes and make up '\
        'a story using tuned generator for better memorization!'
    st.markdown('Similar solutions based on TuneTheModel will be used '
                f'in [SmallTalk]({smalltalk_url})'
                ' - AI-powered simulator to self-practice '
                'the IELTS speaking test, job interview and '
                'everyday conversational English')

    # st.image('img/logo_smalltalk.svg')

    if st.button('Give me an example!'):
        st.session_state['eng_teacher_input'] = choose(
            samples, st.session_state['eng_teacher_input']
        )

    inp = st.text_area(
        'Your sentence', value=st.session_state['eng_teacher_input'],
        max_chars=250
    )

    st.button('Improve the text!')

    if utils.is_fraud(inp):
        st.warning('This text is a bit unusual, the results may be bad')

    with st.spinner("Improving the text using tuned generator..."):
        correct = improve_text(inp)

    if correct == inp:
        st.info(
            'The text is already pretty cool!\n'
            'Try another text with some mistakes.'
        )
        return

    st.subheader('The model suggests rewriting the text as follows:')
    st.markdown(f'## `{correct}`')

    text_p = extract_words(inp)
    gen_p = extract_words(correct)

    new_words = list(set(gen_p) - set(text_p) - set(stop))

    if not new_words:
        st.info('There are no new words in this text, you did well!')
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
