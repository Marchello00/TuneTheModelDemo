import tune_the_model as ttm
import streamlit as st
from nltk.corpus import stopwords
import pandas as pd
import re
import random
import importlib

st.set_page_config(
        page_title="🛒 Review Analyser",
)

if 'aspect_extractor' not in st.session_state:
    st.session_state['aspect_extractor'] = ttm.TuneTheModel.from_id(
        '144ad1e9a353cbbe7c3ef2cc88b9b267'
    )

if 'aspect_sentiment' not in st.session_state:
    st.session_state['aspect_sentiment'] = ttm.TuneTheModel.from_id(
        '585b68935afbc2b11af34ed7234dfe84'
    )
aspect_label_mapping = {
    0: 'Absent',
    1: 'Negative',
    2: 'Neutral',
    3: 'Positive'
}


samples = [
    'The media could not be loaded. This is really nice. If it lasts, that will be awesome. Super quiet motor, and good air movement. Nice color too. Thought the blades were metal, but are plastic... but that’s okay.',
    'Therefore, it is strongly recommended to regular treat items with disinfectants.',
    'As for me, I think that ecology it\'s not the separated part of our life, but one of the biggest parts of that.'
]

if 'review_input' not in st.session_state:
    st.session_state['review_input'] = random.choice(samples)


def choose(arr, prev):
    return random.choice(list(set(arr) - {prev}))


def create_aspect_sent_prompt(review, aspect):
    return review + '\nAspect: ' + aspect + '\nQuality: '


@st.cache(show_spinner=False)
def extract_aspects(review):
    aspects = st.session_state['aspect_extractor'].generate(
        review, num_hypos=20, temperature=1.2
    )
    return list(set(aspects))


@st.cache(show_spinner=False)
def analyse_aspect(review, aspect):
    result = st.session_state['aspect_sentiment'].classify(
        create_aspect_sent_prompt(review, aspect)
    )
    return dict(zip(aspect_label_mapping.values(), result))


def main():
    st.title('Review Analyser')

    st.header('Aspects extraction')

    if st.button('Give me an example!'):
        st.session_state['review_input'] = choose(
            samples, st.session_state['review_input']
        )

    inp = st.text_area(
        'Your review', value=st.session_state['review_input'],
        max_chars=500
    )

    st.button('Analyse review!')

    st.subheader('Aspects, that may present in review:')

    with st.spinner("Extracting aspects using tuned generator..."):
        aspects = extract_aspects(inp)

    with st.spinner("Analysing aspects using tuned classifier..."):
        pbar = st.progress(0)

        aspect_col, sent_col = st.columns(2)

        for i, aspect in enumerate(aspects):
            sentiment_probs = analyse_aspect(inp, aspect)

            with st.expander(aspect):
                df = pd.DataFrame.from_dict(
                    sentiment_probs,
                    orient="index",
                    columns=['Probability']
                )
                st.bar_chart(df)

            pbar.progress((i + 1) / len(aspects))


if __name__ == '__main__':
    main()
