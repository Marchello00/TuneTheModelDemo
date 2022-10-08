import tune_the_model as ttm
import numpy as np
import re
import core


def get_paraphraser():
    return ttm.TuneTheModel.from_id(
        '541fec94231711ed9937e9f0fc1f297c'
    )


def get_storygen():
    return ttm.TuneTheModel.from_id(
        # '617e1c34211b6878000b0af4a5ca8308'  # all rocstories
        '8d6ab260b4d2db23ae16a9eca582c625'  # only positive rocstories
    )


def extract_words(text):
    words = set(re.findall(r'[a-z]+', text.lower()))
    stop_words = core.utils.get_stop_words()
    bad_words = core.utils.get_bad_en_words()
    return words - stop_words - bad_words


def extract_new_words(input_text, improved_text):
    input_p = extract_words(input_text)
    improved_p = extract_words(improved_text)

    return list(improved_p - input_p)


def improve_text(paraphraser, text):
    return paraphraser.generate(text, temperature=0.2)[0]


def make_up_a_story(storygen, moderator, keywords):
    for _ in range(5):
        if len(keywords) > 5:
            selected_keywords = np.random.choice(
                keywords,
                size=5,
                replace=False
            )
        else:
            selected_keywords = keywords
        gens = storygen.generate(', '.join(selected_keywords), num_hypos=3)
        for story in gens:
            story = re.sub(r'([.!?])[^.!?]+$', r'\1', story)
            if core.moderator.pass_moderation(moderator, story):
                return story
    # All stories failed moderation, probably because of bad keywords
    return ' '.join(keywords)
