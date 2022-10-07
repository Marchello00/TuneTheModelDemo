import tune_the_model as ttm
import streamlit as st
from nltk.corpus import stopwords
import pandas as pd
import re
import random
import importlib

st.set_page_config(
        page_title="🛒 Arabic Review Analyser",
)

if 'arabic_review_classifier' not in st.session_state:
    st.session_state['arabic_review_classifier'] = ttm.TuneTheModel.from_id(
        '15c0a81bbcfe081b800c94617dc44d1f'
    )

samples = [
    # "The place is good with a general paralysis”. Breakfast is acceptable. Parking lots
    '“المكان جيد بشل  عام”. الافطار مقبول. مواقف السيارات',
    # "The coolest place”. Excellent. There is no
    '“اروع مكان”. ممتاز. لا يوجد',
    # 'Good. . I asked to have two beds in the room and they told me they could, but they couldn't
    'جيد. . طلبت ضم سريرين الغرفه واخبروني انه بامكانهم ذلك لكن لم يتمكنو من ذلك',
    # “Unpleasant smell”. Nothing, unfortunately. Unpleasant smell in the room and corridors all the time
    '“رائحة كريهة”. لاشئ للاسف. رائحة كريهة بالغرفة والممرات طول الوقت',
    # "The nut ruined the first mo breath”. . The reception staff is of poor standard and is very late in completing the transaction the value of the buffet is very high
    '“القندق خرب مو نفس اول”. . طاقم الاستقبال ضعيف المستوى ويتأخر جدا في انجاز المعاملهقيمة البوفيه عاليه جدا',
    # "Good”. Clean, calm handling is great. The restaurant and the food are public and there are no private cars in the hotel
    '“جيده”. نظافه هدوء تعامل رائع. المطعم والاكل بصفه عامه وعدم وجود سيارات خاصه بالفندق',
]

if 'ar_review_input' not in st.session_state:
    st.session_state['ar_review_input'] = random.choice(samples)


def choose(arr, prev):
    return random.choice(list(set(arr) - {prev}))


@st.cache(show_spinner=False)
def analyse_review(review):
    result = st.session_state['arabic_review_classifier'].classify(
        review
    )
    return result[0]


def main():
    st.title('Arabic Review Sentiment Analyser')

    # Of course, you can tune the neural network to solve classical problems, such as sentiment analysis
    'بالطبع ، يمكنك ضبط الشبكة العصبية لحل المشكلات الكلاسيكية ، مثل تحليل المشاعر'

    _, _, _, _, _, c6 = st.columns(6)
    if c6.button('!أعطني مثالا'):
        st.session_state['ar_review_input'] = choose(
            samples, st.session_state['ar_review_input']
        )

    inp = st.text_input(
        'ملاحظاتك', value=st.session_state['ar_review_input']
    )

    _, _, _, _, c5 = st.columns(5)
    c5.button('!تحليل ردود الفعل')

    with st.spinner("تحليل التغذية الراجعة باستخدام شبكة عصبية مضبوطة"):
        sentiment = analyse_review(inp)

    pos, neg = st.columns(2)
    pos.metric("إيجابي", f"{sentiment * 100:.1f}%")
    neg.metric("سلبي", f"{(1 - sentiment) * 100:.1f}%")


if __name__ == '__main__':
    main()
