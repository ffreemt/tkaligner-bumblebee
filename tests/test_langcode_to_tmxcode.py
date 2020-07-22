""" test langcode_to_tmxcode. """

from freemt_utils import langcode_to_tmxcode


def test_langcode_to_tmxcode():
    """ test langcode_to_tmxcode. """
    assert langcode_to_tmxcode("zh") == "zh-CN"
    assert langcode_to_tmxcode("zh-CHS") == "zh-CN"
    assert langcode_to_tmxcode("zh-CHT") == "zh-TW"
    assert langcode_to_tmxcode("en") == "en-US"
    assert langcode_to_tmxcode("en-uk") == "en-GB"
    assert langcode_to_tmxcode("de") == "de-DE"
    assert langcode_to_tmxcode("en-ca") == "en-CA"
