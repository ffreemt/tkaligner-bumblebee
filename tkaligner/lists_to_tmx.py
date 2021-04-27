""" convert two lists to tmx

based on lxml.etree

# import tqdm  # messed up pyinstaller gooey?

df = pd.read_csv(filepath, header=None, na_filter="", encoding="gbk")
tmx = lists_to_tmx(df[0], df[1])
Path(tmx_path).write_text(tmx, "utf8")
"""

from typing import List, Optional

import lxml.etree as et
from polyglot.text import Detector

import logzero

# from logzero import logger

# from tkaligner.langcode_to_tmxcode import langcode_to_tmxcode
from langcode_to_tmxcode import langcode_to_tmxcode

logger = logzero.setup_logger(name=__file__, level=10)  # pylint: disable=invalid-name

# pylint: disable=too-many-arguments, too-many-locals, invalid-name
# fmt: off
def lists_to_tmx(
        srclist: List[str],
        tgtlist: List[str],
        srclang: Optional[str] = None,  # "en-US",
        tgtlang: Optional[str] = None,  # "zh-CN",
        encoding: Optional[str] = None,
        # method: str = "xml",
        xml_declaration: bool = True,
        pretty_print: bool = True,
        doctype: str = '<!DOCTYPE tmx SYSTEM "tmx14a.dtd">',
) -> str:
    # fmt: on
    """
    lists_to_tmx(srclist, tgtlist, srclang='en-US',
    tgtlang='zh-CN',
    encoding=None, method="xml", xml_declaration=True,
    pretty_print=False, doctype='<!DOCTYPE tmx SYSTEM "tmx14a.dtd">')

    return: bytes

    et.tostring(tostring(element_or_tree, encoding=None, method="xml",
             xml_declaration=None, pretty_print=False, with_tail=True,
             standalone=None, doctype=None,
             exclusive=False, with_comments=True, inclusive_ns_prefixes=None)
    wite out with:
    with open('test2tu.tmx','w') as fh:
   .....:     fh.write(tmx.decode())
    """

    if len(srclist) != len(tgtlist):
        logger.warning(" len(srclist) != len(tgtlist), we proceed anyway...")
        # raise Exception(" len(srclist) != len(tgtlist) ")

    if srclang is None:
        lc1 = Detector(" ".join(srclist)[:5000], quiet=True).language.code
        srclang = langcode_to_tmxcode(lc1)
    if tgtlang is None:
        lc2 = Detector(" ".join(tgtlist)[:5000], quiet=True).language.code
        tgtlang = langcode_to_tmxcode(lc2)

    if encoding is None:
        encoding = "utf-8"

    root = et.Element("tmx", attrib={"version": "1.4"})  # type: ignore

    # header =  # gen header
    et.SubElement(root, "header", attrib={"amdinlang": srclang, "srclang": srclang})  # type: ignore

    body = et.SubElement(root, "body")  # type: ignore

    # tuv_en = et.SubElement(tu, "tuv", xml:lang="en")  # 'xml:lang' gets error
    # tuv_zh = et.SubElement(tu, "tuv", xml:lang="zh")

    len0 = min(len(srclist), len(tgtlist))

    # for itrange in tqdm.trange(len0):
    for itrange in range(len0):
        tu = et.SubElement(body, "tu")  # type: ignore
        tuv_en = et.SubElement(tu, "tuv", attrib={"lang": srclang})  # type: ignore
        tuv_zh = et.SubElement(tu, "tuv", attrib={"lang": tgtlang})  # type: ignore
        # attach tuv to tree
        et.SubElement(tuv_en, "seg").text = srclist[itrange]  # type: ignore
        et.SubElement(tuv_zh, "seg").text = tgtlist[itrange]  # type: ignore

    tree = et.ElementTree(root)  # type: ignore
    treestr = et.tostring(  # type: ignore
        tree,
        encoding=encoding,
        pretty_print=pretty_print,
        xml_declaration=xml_declaration,
        doctype=doctype,
    )

    return treestr.decode()

    # return et.tostring(
    #             tree, encoding='utf-8', pretty_print=pretty_print,
    #             xml_declaration=xml_declaration, doctype=doctype)
