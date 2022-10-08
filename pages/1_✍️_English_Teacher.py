import streamlit as st
import core.english_teacher
import core.utils
import core.moderator
from core.constants import generation_warning
from samples.english_teacher import samples

st.set_page_config(
        page_title="✍️ English Teacher",
)

if 'paraphraser' not in st.session_state:
    st.session_state['paraphraser'] = core.english_teacher.get_paraphraser()

if 'storygen' not in st.session_state:
    st.session_state['storygen'] = core.english_teacher.get_storygen()

if 'eng_teacher_input' not in st.session_state:
    st.session_state['eng_teacher_input'] = core.utils.choose(samples)

if 'moderator' not in st.session_state:
    st.session_state['moderator'] = core.moderator.get_moderator()


def improve_text(text):
    return core.english_teacher.improve_text(
        st.session_state['paraphraser'], text
    )


def make_up_a_story(keywords):
    return core.english_teacher.make_up_a_story(
        st.session_state['storygen'],
        st.session_state['moderator'],
        keywords
    )


def main():
    c1, c2 = st.columns([3, 1])
    c1.title('English Teacher')
    smalltalk_logl_url = \
        'https://static.tildacdn.com/tild3431-6362-4434-b336-393736666264/logo_smalltalk.svg'
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

    if st.button('Give me an example!'):
        st.session_state['eng_teacher_input'] = core.utils.choose(
            samples, st.session_state['eng_teacher_input']
        )

    inp = st.text_area(
        'Your sentence', value=st.session_state['eng_teacher_input'],
        max_chars=250
    )

    st.button('Improve the text!')

    if core.utils.is_fraud(inp):
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

    new_words = core.english_teacher.extract_new_words(inp, correct)

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
    st.caption(generation_warning)

    if story == ' '.join(new_words):
        st.warning('Sorry, we couldn\'t create a good story, probably some of the new words caused unwanted content.')


if __name__ == '__main__':
    main()
