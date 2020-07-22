r""" convert langcode str to a TMX code (langid-LOCALE).

refer to snippets-mat\langcodes-tmx-python.txt

http://www.lingoes.net/en/translator/langcode.htm
"""

from pathlib import Path
import json

# pip install langcode,
# needs marisa_trie-0.7.5-cp36-cp36m-win_amd64.whl

from langcodes import standardize_tag, closest_match

from logzero import logger

fpath = Path(__file__).parent / "lcid.json"
JDATA = json.loads(fpath.read_text("utf8"))
TMX_CODES = [elm.replace("_", "-") for elm in JDATA.values()]
# remove "zh-CHS", "zh-CHT"
TMX_CODES.pop(TMX_CODES.index("zh-CHS"))
TMX_CODES.pop(TMX_CODES.index("zh-CHT"))


def langcode_to_tmxcode(langcode: str, default="en_US") -> str:
    """ convert langcode str to a TMX code (langid-LOCALE).

    >>> langcode_to_tmxcode("zh")
    'zh-CN'
    >>> langcode_to_tmxcode("zh-CHS")
    'zh-CN'
    >>> langcode_to_tmxcode("zh-CHT")
    'zh-TW'
    >>> langcode_to_tmxcode("en")
    'en-US'
    >>> langcode_to_tmxcode("en-uk")
    'en-GB'
    >>> langcode_to_tmxcode("de")
    'de-DE'
    >>> langcode_to_tmxcode("en-ca")
    'en-CA'
    >>> langcode_to_tmxcode("pt")
    'pt-PT'
    """
    if langcode.lower() == "zh-cht":
        langcode = "zh-tw"

    if langcode.lower() == "pt":
        langcode = "pt-pt"

    lc_ = standardize_tag(langcode)

    try:
        tmxcode = closest_match(lc_, TMX_CODES)[0]
    except Exception as exc:
        logger.warning(" exc: %s, returning en-US", exc)
        tmxcode = default

    return tmxcode
