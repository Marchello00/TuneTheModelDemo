import tune_the_model as ttm
import pandas as pd
import numpy as np
import core.translate
import core.parse_html


def get_title_and_content(url):
    title, content = core.parse_html.page_parser(url)
    content = content[:5000]
    trans_title, trans_content = core.translate.translate(
        [title, content], target_language='ru'
    )
    return trans_title, trans_content, title, content


def get_keyword_classifier():
    return ttm.TuneTheModel.from_id(
        'a526dd2a846d0dce166e807b16e274a8'
    )


def get_keyword_generator():
    return ttm.TuneTheModel.from_id(
        '76e82bd661492d998c89db47c7952d3e'  # ig data
        # '86a4b73567927399679d281ab9a4ae75'  # autotargeting
    )


def get_banner_classifier():
    return ttm.TuneTheModel.from_id(
        '2e96b14e220711ed9e95b1ae88b1dbe2'
    )


def get_banner_generator():
    return ttm.TuneTheModel.from_id(
        '29f535330158d16b9d1d905a3914a079'  # autotargeting
        # '9c59c12bdfbea8275584188e54344313' ig data
    )


keyword_classifier_mapping = [
    'Accessory',
    'Alternative',
    'Broader',
    'Competitor',
    'Exact match',
    'No match'
]


def create_keyword_prompt(title, content, kw):
    return 'Загловок: ' + title +\
            '\n\nСтарница: ' + content +\
            '\n\nЗапрос: ' + kw


def classify_keyword(keyword_classifier, title, content, keyword):
    scores = keyword_classifier.classify(
        create_keyword_prompt(title, content, keyword)
    )
    result = pd.DataFrame.from_dict(
        {'Property': keyword_classifier_mapping, 'Score': scores}
    )
    return result


def create_keyword_gen_prompt(title, content):
    return 'Загловок: ' + title +\
            '\n\nСтарница: ' + content +\
            '\n\nКлючевые слова: '


def gen_keywords(
    keyword_generator, keyword_classifier,
    title, content, temp=1.1, num_hypos=18
):
    model_input = create_keyword_gen_prompt(title, content)

    result = keyword_generator.generate(
        model_input, num_hypos=num_hypos, min_tokens=4,
        max_tokens=128, temperature=temp, top_k=30
    )

    result = np.unique(result)

    result = [
        (
            keyword,
            classify_keyword(
                keyword_classifier, title, content, keyword
            )
        )
        for keyword in result
    ]

    result = sorted(
        [
            (keyword, scores)
            for keyword, scores in result
            if scores[scores['Property'] == 'No match']['Score'].iloc[0] < 0.5
        ],
        key=lambda x: -x[1][x[1]['Property'] == 'Exact match']['Score'].iloc[0]
    )

    result = [
        (
            core.translate.translate([keyword], 'en')[0],
            score
        )
        for keyword, score in result
    ]

    return result


def create_banner_prompt(page_title, page_content):
    return "Заголовок:\n" + page_title +\
            "\n\nСтраница:\n" + page_content +\
            "\n\nБаннер:\n"


def generate_banner(
    banner_generator, banner_classifier,
    title, content, temp=0.6, num_hypos=7
):
    model_input = create_banner_prompt(title, content)
    banners = banner_generator.generate(
        model_input, num_hypos=num_hypos, min_tokens=4,
        max_tokens=128, temperature=temp, top_k=30
    )

    banners = [b.replace('\\r\\n', '\n') for b in banners]
    split_banners = [b.split('\n\n', maxsplit=1) for b in banners]
    inputs = ['\n '.join(parts + [title, content[:200]])
              for parts in split_banners]
    scores = [banner_classifier.classify(i)[0] for i in inputs]

    result = []
    for s, b in sorted(zip(scores, split_banners), reverse=True):
        if len(b) == 1:
            b.append('')
        elif len(b) == 0:
            continue
        result.append(b)

    result = [core.translate.translate(banner, "en") for banner in result]

    return result
