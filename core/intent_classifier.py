import tune_the_model as ttm


def get_intent_classifier():
    return ttm.TuneTheModel.from_id(
        'iuvmp2anbfujbzmetfax6jpjrz0jzbyi'
    )


def get_slot_generator():
    return ttm.TuneTheModel.from_id(
        '3wp7he0qx1577o8jsowqb00k1gcrmo3l'
    )


def classify_intent(intent_classifier, text):
    return intent_classifier.classify(text)


def generate_slots(slot_generator, text):
    return slot_generator.generate(text, temperature=0.2)[0]


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


def classify_intent_labeled(intent_classifier, text):
    result = classify_intent(intent_classifier, text)
    return {label: prob for label, prob in
            zip(intent_classifier_mapping, result)}
