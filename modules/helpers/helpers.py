import codecs


def remove_escaped_characters(text):
    return codecs.unicode_escape_decode(text)[0]