import streamlit as st
import tune_the_model as ttm
import pandas as pd
import random

st.set_page_config(
        page_title="🔞 Moderator",
)

if 'moderator' not in st.session_state:
    st.session_state['moderator'] = ttm.TuneTheModel.from_id(
        'dmfe5l5uq6djz42jbj8oqesm77locg6x'
    )


moderator = st.session_state['moderator']
moderator_mapping = [
    'Alcohol',
    'Clean text',
    'Obscene/Insult',
    'Porn/Erotica',
    'Sex Toys',
    'Smoking/Drugs',
    'Spam/Clickbait',
    'Violence/Shock',
    'Weapon'
]

samples = [
    'Hapy birfday my dear frend!',
    'Therefore, it is strongly recommended to regular treat items with disinfectants.',
    'As for me, I think that ecology it\'s not the separated part of our life, but one of the biggest parts of that.'
]

def choose(arr, prev):
    return random.choice(list(set(arr) - {prev}))


if 'moderator_input' not in st.session_state:
    st.session_state['moderator_input'] = random.choice(samples)


@st.cache(show_spinner=False)
def moderate(text):
    return moderator.classify(text)


def main():
    st.title('Moderator')

    st.header('English')

    if st.button('Give me an example!'):
        st.session_state['moderator_input'] = choose(
            samples, st.session_state['moderator_input']
        )

    inp = st.text_area(
        'Input text for check',
        value=st.session_state['moderator_input'],
        max_chars=500
    )

    st.button('Check the text')
    if not inp:
        st.error('Input must be nonempty.')
        return

    with st.spinner("Analysing text using tuned classifier..."):
        results = moderate(inp)

    data = {key: prob for key, prob in zip(moderator_mapping, results)}
    st.bar_chart(data=pd.Series(data, name='Probability'))


if __name__ == '__main__':
    main()
