import streamlit as st
import pandas as pd
import core.utils
import core.intent_classifier
from samples.intent_classifier import samples

st.set_page_config(
        page_title="💬 Intent Classifier",
)

if 'intent_classifier' not in st.session_state:
    st.session_state['intent_classifier'] = \
        core.intent_classifier.get_intent_classifier()


if 'slot_generator' not in st.session_state:
    st.session_state['slot_generator'] = \
        core.intent_classifier.get_slot_generator()


def prettify_label(text):
    return ' '.join([t.capitalize() for t in text.split('_')])


if 'intent_input' not in st.session_state:
    st.session_state['intent_input'] = core.utils.choose(samples)


@st.cache(show_spinner=False)
def classify_intent(text):
    return core.intent_classifier.classify_intent_labeled(
        st.session_state['intent_classifier'],
        text
    )


@st.cache(show_spinner=False)
def generate_slots(text):
    return core.intent_classifier.generate_slots(
        st.session_state['slot_generator'],
        text
    )


def main():
    st.title('Intent Classifier')

    'You can build a complex system using tuned '\
        'models as components. For example, '\
        'you can classify user intentions '\
        'for your chatbot!'

    if st.button('Give me an example!'):
        st.session_state['intent_input'] = core.utils.choose(
            samples, st.session_state['intent_input']
        )

    inp = st.text_area(
        'Input utterance',
        value=st.session_state['intent_input'],
        max_chars=150
    )

    st.button('Detect intent')
    if not inp:
        st.error('Input must be nonempty.')
        return

    with st.spinner("Analysing text using tuned classifier..."):
        results = classify_intent(inp)

    st.subheader('Intent')
    with st.expander(
        prettify_label(max(list(results.items()), key=lambda x: x[1])[0])
    ):
        data = [
            {'Intent': prettify_label(key), 'Probability': prob}
            for key, prob in results.items()
        ]
        data = sorted(data, key=lambda t: t['Probability'])[::-1][:10]
        st.bar_chart(data=pd.DataFrame(data), x='Intent', y='Probability')

    st.subheader('Slots, found in utterance')

    with st.spinner("Searching for entities using tuned generator..."):
        result = generate_slots(inp)

    st.markdown(f'## `{result}`')


if __name__ == '__main__':
    main()
