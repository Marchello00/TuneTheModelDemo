import tune_the_model as ttm


def vanila_gen(text):
    return ttm.generate(text)[0]
