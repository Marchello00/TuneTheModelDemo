import tune_the_model as ttm


def get_arabic_review_classifier():
    return ttm.TuneTheModel.from_id(
        '15c0a81bbcfe081b800c94617dc44d1f'
    )


def analyse_review(arabic_review_classifier, review):
    result = arabic_review_classifier.classify(
        review
    )
    return result[0]
