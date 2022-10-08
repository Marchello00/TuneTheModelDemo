import streamlit as st
import pandas as pd
import core.moderator
import core.utils
from samples.moderator import samples

st.set_page_config(
    page_title="🔞 Moderator",
)

if 'moderator' not in st.session_state:
    st.session_state['moderator'] = core.moderator.get_moderator()


if 'moderator_input' not in st.session_state:
    st.session_state['moderator_input'] = core.utils.choose(samples)


@st.cache(show_spinner=False)
def moderate(text):
    return core.moderator.moderate_labeled(st.session_state['moderator'], text)


def main():
    st.title('Moderator')

    st.header('English')

    'You can easily tune the classifier '\
        'to check whether the text contains any topics that '\
        'are undesirable for your service'

    if st.button('Give me an example!'):
        st.session_state['moderator_input'] = core.utils.choose(
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
        resutls = moderate(inp)

    st.bar_chart(data=pd.Series(resutls, name='Probability'))


if __name__ == '__main__':
    main()
