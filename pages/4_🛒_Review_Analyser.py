import streamlit as st
import pandas as pd
import core.utils
import core.review_analyser
from samples.review_analyser import samples

st.set_page_config(
        page_title="🛒 Review Analyser",
)

if 'aspect_extractor' not in st.session_state:
    st.session_state['aspect_extractor'] = \
        core.review_analyser.get_aspect_extractor()


if 'aspect_sentiment' not in st.session_state:
    st.session_state['aspect_sentiment'] = \
        core.review_analyser.get_aspect_sentiment_classifier()


if 'review_input' not in st.session_state:
    st.session_state['review_input'] = core.utils.choose(samples)


def extract_aspects(review):
    return core.review_analyser.extract_aspects(
        st.session_state['aspect_extractor'],
        review
    )


@st.cache(show_spinner=False)
def analyse_aspect(review, aspect):
    return core.review_analyser.analyse_aspect(
        st.session_state['aspect_sentiment'],
        review,
        aspect
    )


def main():
    st.title('Review Analyser')

    st.header('Aspects extraction')

    'You can tune a generator to extract aspects from a '\
        'product review and, in addition, tune a classifier '\
        'to check whether a statement about this aspect is '\
        'positive or negative and whether it is actually present in review'

    if st.button('Give me an example!'):
        st.session_state['review_input'] = core.utils.choose(
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
