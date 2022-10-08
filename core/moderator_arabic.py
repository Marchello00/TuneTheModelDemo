import tune_the_model as ttm


def get_moderator_ar():
    return ttm.TuneTheModel.from_id(
        'ced62ff2441911eda62b531521f160a2'
    )


def moderate_arabic(moderator_ar, text):
    return moderator_ar.classify(text)


moderator_ar_mapping = [
    'الكحول',
    'نص نظيف',
    'فاحشة / إهانة',
    'الإباحية / الشبقية',
    'الجنس ولعب بنات',
    'التدخين / المخدرات',
    'البريد المزعج / كليكبيت',
    'العنف / الصدمة',
    'سلاح'
]

# moderator_ar_mapping = [
#     'Alcohol',
#     'Clean text',
#     'Obscene/Insult',
#     'Porn/Erotica',
#     'Sex Toys',
#     'Smoking/Drugs',
#     'Spam/Clickbait',
#     'Violence/Shock',
#     'Weapon'
# ]


def moderate_arabic_labeled(moderator_ar, text):
    results = moderate_arabic(moderator_ar, text)
    return {key: prob for key, prob in zip(moderator_ar_mapping, results)}
