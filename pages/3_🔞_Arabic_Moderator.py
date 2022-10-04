import streamlit as st
import tune_the_model as ttm
import pandas as pd
import random

st.set_page_config(
        page_title="🔞 Arabic Moderator",
)

if 'moderator_ar' not in st.session_state:
    st.session_state['moderator_ar'] = ttm.TuneTheModel.from_id(
        'ced62ff2441911eda62b531521f160a2'
    )

moderator_ar = st.session_state['moderator_ar']

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


samples_ar = [
    'Text',
    'Sample text'
]


def choose(arr, prev):
    return random.choice(list(set(arr) - {prev}))


if 'moderator_ar_input' not in st.session_state:
    st.session_state['moderator_ar_input'] = random.choice(samples_ar)


@st.cache(show_spinner=False)
def moderate_arabic(text):
    return moderator_ar.classify(text)


def main():
    st.title('Moderator')

    st.header('Arabic')

    *_, right_column = st.columns(6)
    if right_column.button('!أعطني مثالا'):
        st.session_state['moderator_ar_input'] = choose(
            samples_ar, st.session_state['moderator_ar_input']
        )
        st.session_state['moderate_ar_sampled'] = True

    inp_ar = st.text_area(
        'إدخال النص', value=st.session_state['moderator_ar_input'],
        max_chars=500
    )

    if not inp_ar:
        st.error('.يجب أن يكون نص الإدخال غير فارغ')
        return

    *_, right_column = st.columns(5)
    right_column.button('تحقق من النص')

    with st.spinner("تحليل النص باستخدام شبكة عصبية مضبوطة"):
        results_ar = moderate_arabic(inp_ar)

    data_ar = {key: prob for key, prob in zip(
        moderator_ar_mapping, results_ar
    )}
    st.bar_chart(data=pd.Series(data_ar, name='الاحتمال'))
    st.session_state['moderate_ar_sampled'] = False


if __name__ == '__main__':
    main()
