import tune_the_model as ttm


def get_aspect_extractor():
    return ttm.TuneTheModel.from_id(
        '144ad1e9a353cbbe7c3ef2cc88b9b267'
    )


def get_aspect_sentiment_classifier():
    return ttm.TuneTheModel.from_id(
        '585b68935afbc2b11af34ed7234dfe84'
    )


def create_aspect_sent_prompt(review, aspect):
    return review + '\nAspect: ' + aspect + '\nQuality: '


def extract_aspects(aspect_extractor, review):
    aspects = aspect_extractor.generate(
        review, num_hypos=20, temperature=1.2
    )
    return list(set(aspects))


aspect_label_mapping = {
    0: 'Absent',
    1: 'Negative',
    2: 'Neutral',
    3: 'Positive'
}


def analyse_aspect(aspect_sentiment_classifier, review, aspect):
    result = aspect_sentiment_classifier.classify(
        create_aspect_sent_prompt(review, aspect)
    )
    return dict(zip(aspect_label_mapping.values(), result))
