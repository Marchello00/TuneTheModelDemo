import streamlit as st
import pandas as pd
from samples.moderator_arabic import samples
import core.utils
import core.moderator_arabic

st.set_page_config(
        page_title="🔞 Arabic Moderator",
)

if 'moderator_ar' not in st.session_state:
    st.session_state['moderator_ar'] = core.moderator_arabic.get_moderator_ar()


if 'moderator_ar_input' not in st.session_state:
    st.session_state['moderator_ar_input'] = core.utils.choose(samples)


@st.cache(show_spinner=False)
def moderate_arabic(text):
    return core.moderator_arabic.moderate_arabic_labeled(
        st.session_state['moderator_ar'],
        text
    )


def main():
    st.title('Moderator')

    st.header('Arabic')

    # You can easily fine-tune the neural network to check if the text contains any undesirable topics for your service
    'يمكنك بسهولة ضبط الشبكة العصبية للتحقق مما إذا كان النص يحتوي على أي مواضيع غير مرغوب فيها لخدمتك'

    *_, right_column = st.columns(6)
    if right_column.button('!أعطني مثالا'):
        st.session_state['moderator_ar_input'] = core.utils.choose(
            samples, st.session_state['moderator_ar_input']
        )

    inp_ar = st.text_area(
        'إدخال النص', value=st.session_state['moderator_ar_input'],
        max_chars=500
    )

    if not inp_ar:
        st.error('.يجب أن يكون نص الإدخال غير فارغ')
        return

    _, right_column = st.columns([5, 1])
    right_column.button('تحقق من النص')

    with st.spinner("تحليل النص باستخدام شبكة عصبية مضبوطة"):
        results_ar = moderate_arabic(inp_ar)

    st.bar_chart(data=pd.Series(results_ar, name='الاحتمال'))


if __name__ == '__main__':
    main()
