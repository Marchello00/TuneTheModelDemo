import streamlit as st
import tune_the_model as ttm
import pandas as pd
import numpy as np
import random

st.set_page_config(
        page_title="💬 Intent Classifier",
)

if 'intent_classifier' not in st.session_state:
    st.session_state['intent_classifier'] = ttm.TuneTheModel.from_id(
        'iuvmp2anbfujbzmetfax6jpjrz0jzbyi'
    )


if 'slot_generator' not in st.session_state:
    st.session_state['slot_generator'] = ttm.TuneTheModel.from_id(
        '3wp7he0qx1577o8jsowqb00k1gcrmo3l'
    )


intent_classifier = st.session_state['intent_classifier']
intent_classifier_mapping = [
    'alarm_query', 'alarm_remove', 'alarm_set',
    'audio_volume_down', 'audio_volume_mute', 'audio_volume_other',
    'audio_volume_up', 'calendar_query', 'calendar_remove',
    'calendar_set', 'cooking_query', 'cooking_recipe',
    'datetime_convert', 'datetime_query', 'email_addcontact',
    'email_query', 'email_querycontact', 'email_sendemail',
    'general_greet', 'general_joke', 'general_quirky', 'iot_cleaning',
    'iot_coffee', 'iot_hue_lightchange', 'iot_hue_lightdim',
    'iot_hue_lightoff', 'iot_hue_lighton', 'iot_hue_lightup',
    'iot_wemo_off', 'iot_wemo_on', 'lists_createoradd', 'lists_query',
    'lists_remove', 'music_dislikeness', 'music_likeness', 'music_query',
    'music_settings', 'news_query', 'play_audiobook', 'play_game',
    'play_music', 'play_podcasts', 'play_radio', 'qa_currency',
    'qa_definition', 'qa_factoid', 'qa_maths', 'qa_stock',
    'recommendation_events', 'recommendation_locations',
    'recommendation_movies', 'social_post', 'social_query', 'takeaway_order',
    'takeaway_query', 'transport_query', 'transport_taxi', 'transport_ticket',
    'transport_traffic', 'weather_query'
]

slot_generator = st.session_state['slot_generator']


def prettify_label(text):
    return ' '.join([t.capitalize() for t in text.split('_')])


samples = [
    # 'wake me up at five am this week',
    'i like senatra songs',
    'what\'s the time in australia',
    'set lights brightness higher',
    'could you order sushi for tonight dinner',
    'what\'s the week\'s forecast',
    'play it again please',
    'can they do delivery',
    'tell me some business news',
    'play my rock playlist',
    'should i bring an umbrella tomorrow',
    'i can barely hear you'
]


def choose(arr, prev):
    return random.choice(list(set(arr) - {prev}))


if 'intent_input' not in st.session_state:
    st.session_state['intent_input'] = random.choice(samples)


@st.cache(show_spinner=False)
def classify_intent(text):
    return intent_classifier.classify(text)


@st.cache(show_spinner=False)
def generate_slots(text):
    return slot_generator.generate(text, temperature=0.2)[0]


def main():
    st.title('Intent Classifier')

    'You can build a complex system using tuned '\
        'models as components. For example, '\
        'you can classify user intentions '\
        'for your chatbot!'

    if st.button('Give me an example!'):
        st.session_state['intent_input'] = choose(
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
        prettify_label(intent_classifier_mapping[np.argmax(results)])
    ):
        data = [
            {'Intent': prettify_label(key), 'Probability': prob}
            for key, prob in zip(intent_classifier_mapping, results)
        ]
        data = sorted(data, key=lambda t: t['Probability'])[::-1][:10]
        st.bar_chart(data=pd.DataFrame(data), x='Intent', y='Probability')

    st.subheader('Slots, found in utterance')

    with st.spinner("Searching for entities using tuned generator..."):
        result = generate_slots(inp)

    st.markdown(f'## `{result}`')


if __name__ == '__main__':
    main()
