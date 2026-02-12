import arabic_reshaper
from bidi.algorithm import get_display

def ar(text):
    if any('\u0600' <= c <= '\u06FF' for c in text):
        return get_display(arabic_reshaper.reshape(text))
    return text
