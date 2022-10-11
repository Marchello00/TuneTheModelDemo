import streamlit as st
import core.utils
import core.constants
import core.generate_advertisement
from samples.generate_advertisement import samples

st.set_page_config(
        page_title="📈 Generate Advertisement",
)

if 'keyword_classifier' not in st.session_state:
    st.session_state['keyword_classifier'] =\
        core.generate_advertisement.get_keyword_classifier()

if 'keyword_generator' not in st.session_state:
    st.session_state['keyword_generator'] =\
        core.generate_advertisement.get_keyword_generator()

if 'banner_classifier' not in st.session_state:
    st.session_state['banner_classifier'] =\
        core.generate_advertisement.get_banner_classifier()

if 'banner_generator' not in st.session_state:
    st.session_state['banner_generator'] =\
        core.generate_advertisement.get_banner_generator()

if 'adgen_input' not in st.session_state:
    st.session_state['adgen_input'] = core.utils.choose(samples)


def gen_keywords(title, content, temp):
    return core.generate_advertisement.gen_keywords(
        st.session_state['keyword_generator'],
        st.session_state['keyword_classifier'],
        title,
        content,
        temp
    )


def gen_banners(title, content, temp):
    return core.generate_advertisement.generate_banner(
        st.session_state['banner_generator'],
        st.session_state['banner_classifier'],
        title,
        content,
        temp
    )


def process(url, keywords_temp, banner_temp):
    try:
        title, content, orig_title, orig_content =\
            core.generate_advertisement.get_title_and_content(url)
    except Exception:
        st.error('An error occurred while downloading data from the site. '
                 'Make sure the address is correct '
                 '(for example, \"https://www.northstardubai.com /\"), '
                 ' or try generation for another site.')
        return
    if not title and not content:
        st.error('Unfortunately, it was not possible to extract '
                 'the text from the page. '
                 'Please try generating for another site.')
        return
    ex = st.expander('Site content')
    ex.write(orig_title)
    ex.write(orig_content)

    if len(title) + len(content) < 200:
        st.warning('Attention! Very little text was '
                   'extracted from the page - the '
                   'results may be of poor quality.')

    '--------'

    tmp = st.columns(2)
    tmp[0].header('Banners:')
    tmp[1].header('Keywords:')
    '--------'
    c1, c2 = st.columns(2)
    with c1:
        with st.spinner("Generating banners..."):
            st.session_state["banners"] = gen_banners(
                title, content, banner_temp
            )

        for h, t in st.session_state["banners"]:
            st.subheader(h)
            st.write(t)

            '--------'

    with c2:
        with st.spinner("Generating keywords..."):
            keywords = gen_keywords(title, content, keywords_temp)
            st.session_state["keywords"] = keywords

        for t in st.session_state["keywords"]:
            ex = st.expander(t[0])
            ex.bar_chart(t[1], x='Property', y='Score')
    '--------'
    st.caption(core.constants.generation_warning)


def main():
    st.title('Generate Advertisement')

    'You can tune the model to generate great advertisement '\
        'by the content of the website! Also you can tune generator '\
        'to make up search queries for your page!'

    if st.button('Give me an example!'):
        st.session_state['adgen_input'] = core.utils.choose(
            samples, st.session_state['adgen_input']
        )
    url = st.text_input('URL', value=st.session_state['adgen_input'])
    button_load_data = st.button("Generate!")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader('Banner generation parameters')
        banner_temp = st.slider(
            'Creativity', 0.01, 2.1, value=0.6,
            key='banner_temp',
            help="With a decrease in creativity, correctness grows, "
            "with an increase in creativity, diversity grows"
        )
    with c2:
        st.subheader('Keyword generation parameters')
        keywords_temp = st.slider(
            'Creativity', 0.01, 2.1, value=1.1,
            key='kw_temp',
            help="With a decrease in creativity, correctness grows, "
            "with an increase in creativity, diversity grows"
        )

    process(url, keywords_temp, banner_temp)


if __name__ == '__main__':
    main()
