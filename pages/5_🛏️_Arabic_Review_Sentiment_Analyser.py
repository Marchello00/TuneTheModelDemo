import streamlit as st
import core.utils
import core.arabic_review_analyser
from samples.arabic_review_analyser import samples

st.set_page_config(
        page_title="🛒 Arabic Review Analyser",
)

if 'arabic_review_classifier' not in st.session_state:
    st.session_state['arabic_review_classifier'] = \
        core.arabic_review_analyser.get_arabic_review_classifier()


if 'ar_review_input' not in st.session_state:
    st.session_state['ar_review_input'] = core.utils.choose(samples)


@st.cache(show_spinner=False)
def analyse_review(review):
    return core.arabic_review_analyser.analyse_review(
        st.session_state['arabic_review_classifier'],
        review
    )


def main():
    st.title('Arabic Review Sentiment Analyser')

    # Of course, you can tune the neural network to solve classical problems, such as sentiment analysis
    'بالطبع ، يمكنك ضبط الشبكة العصبية لحل المشكلات الكلاسيكية ، مثل تحليل المشاعر'

    _, _, _, _, _, c6 = st.columns(6)
    if c6.button('!أعطني مثالا'):
        st.session_state['ar_review_input'] = core.utils.choose(
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
