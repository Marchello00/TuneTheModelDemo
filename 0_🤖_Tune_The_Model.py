import streamlit as st
import tune_the_model as ttm
import os
import string

import nltk
nltk.download("stopwords")
nltk.download("words")
from nltk.corpus import words

nltk.download("stopwords")
nltk.download("words")

if 'moderator' not in st.session_state:
    st.session_state['moderator'] = ttm.TuneTheModel.from_id(
        'dmfe5l5uq6djz42jbj8oqesm77locg6x'
    )

if 'fraud' not in st.session_state:
    st.session_state['fraud'] = ttm.TuneTheModel.from_id(
        'e6db68a7494d204405414ec9bb1b615f'
    )

if 'all_en_words' not in st.session_state:
    st.session_state['all_en_words'] = set(words.words())


@st.cache(show_spinner=False)
def is_fraud(text):
    if 'all_en_words' not in st.session_state:
        st.session_state['all_en_words'] = set(words.words())
    
    text = text.translate(str.maketrans('', '', string.punctuation))
    good_words = 0
    total = 0
    for word in text.split():
        good_words += word in st.session_state['all_en_words']
        total += 1
    share = good_words / total
    return share < 0.2


@st.cache(show_spinner=False)
def pass_moderation(text):
    if 'moderator' not in st.session_state:
        st.session_state['moderator'] = ttm.TuneTheModel.from_id(
            'dmfe5l5uq6djz42jbj8oqesm77locg6x'
        )

    res = st.session_state['moderator'].classify(text)
    return all(
        prob < 0.1
        for i, prob in enumerate(res)
        if i != 1  # skip clean text
    )


# @st.cache(show_spinner=False)
def vanila_gen(text):
    return ttm.generate(text)[0]


def main():
    # st.title('Tune The Model')
    st.image('img/logo.png')

    st.markdown('[Tune the Model](tunethemodel.com) allows you '
                'to create a custom text AI tailored for your application.')

    'Powered by huge pre-trained transformer language models, '\
        'Tune the Model enables you to create text AI and bring it '\
        'to production without investing in labelling large datasets, '\
        'running tons of experiments, or setting up GPU cloud.'

#     st.header("Few-shot samples")

#     'Some tasks may be solved with just a few samples. You can pass '\
#         'several examples to the model input, and it will try to find '\
#         'the answer for the last query by continuing your text.'

#     prompts = {
#         "Email generator": """Command: Thank Sid for the gift cards
# Email: Hey Sid, Thank you so much for the gift cards. I really appreciate it. I hope to see you soon. Best, Aidan.


# Command: Invoice Nicole $500 for financial modeling
# Email: Dear Nicole, This is my invoice for $500 for the financial modeling. It was a pleasure to work with you. Sincerely, Dustin.


# Command: Tell Kiyan that they made it to the next round
# Email: Hey Kiyan, You've moved forward to the next round of interviews. The team is looking forward to seeing you again. Sincerely, Nora.


# Command: Ask Adrien for a coffee chat
# Email: Hey Adrien, Long time no see! Let's catch up and grab coffee. What's your schedule look like? Regards, Amr


# Command: Tell Robert to keep up the good work
# Email: """,
#         "Topic extractor": """Text: We often read about children who have betrayed their parents in acts of selfishness or even in times of Civil War. But what would be the worst way for a parent to betray their own child?


# Topics: family, children, betrayal

# -------------------

# Text: Classical economics states that money constitutes of four chief functions: medium, measure, standards and store. Money used in this form eliminates the inefficiencies associated with the traditional barter system, for instance double coincidence of wants. In this context, money can be viewed as a unit that is used to measure the worth of deferred payment. From this perspective, money as a unit of account is a key requirement during the making of agreements that entail debt or future payments.


# Topics: money, economics

# -------------------

# Text: Ginger is native to Southern Asia and was later cultivated in Ancient China as a food source and medicine. Over time, ginger cultivation spread to India, from there it was carried to the Middle East as part of the spice trade. As crusaders returned home to Europe from the Middle East, they brought spices with them, including cinnamon, pepper and ginger.

# Topics: """,
#         "Simple generator": "Powered by huge pre-trained transformer language models, Tune the Model enables you to create text AI and bring it to production without investing in labelling large datasets, running tons of experiments, or setting up GPU cloud."
#     }

#     tabs = st.tabs(list(prompts))

#     for tab, (tab_name, prompt) in zip(tabs, prompts.items()):
#         with tab:
#             inp = st.text_area(
#                 "Type text, and model will try to continue it",
#                 value=prompt,
#                 max_chars=2000,
#                 height=200,
#             )

#             if not inp:
#                 st.error("Input text cannot be empty")
#                 return

#             st.subheader('Generated continuation')

#             with st.spinner("Generating continuation using tune..."):
#                 result = vanila_gen(inp)
#                 if tab_name == "Topic extractor":
#                     try:
#                         result = result.split('\n\n')[0]
#                     except Exception:
#                         pass
#             st.write(result)


if __name__ == '__main__':
    ttm.set_api_key(os.environ.get('TTM_API_KEY'))
    st.set_page_config(
        page_title="🤖 Tune The Model",
    )
    main()
