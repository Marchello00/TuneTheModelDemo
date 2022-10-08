import tune_the_model as ttm


def get_moderator():
    return ttm.TuneTheModel.from_id(
        'dmfe5l5uq6djz42jbj8oqesm77locg6x'
    )


def moderate(moderator, text):
    return moderator.classify(text)


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


def moderate_labeled(moderator, text):
    results = moderate(moderator, text)
    return {key: prob for key, prob in zip(moderator_mapping, results)}


def pass_moderation(moderator, text):
    res = moderate_labeled(moderator, text)
    return all(
        prob < 0.1
        for label, prob in res.items()
        if label != 'Clean text'
    )
