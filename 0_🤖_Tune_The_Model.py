import streamlit as st
import tune_the_model as ttm
import os


def main():
    st.image('img/logo.png')

    st.markdown('[Tune the Model](tunethemodel.com) allows you '
                'to create a custom text AI tailored for your application.')

    'Powered by huge pre-trained transformer language models, '\
        'Tune the Model enables you to create text AI and bring it '\
        'to production without investing in labelling large datasets, '\
        'running tons of experiments, or setting up GPU cloud.'


if __name__ == '__main__':
    ttm.set_api_key(os.environ.get('TTM_API_KEY'))
    st.set_page_config(
        page_title="🤖 Tune The Model",
    )
    main()
