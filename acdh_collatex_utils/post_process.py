import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader


def merge_tei_fragments(files):
    """ takes a list of files (fullpaths) and retuns a singel tei:ab element.etree node"""
    full_doc = ET.Element("{http://www.tei-c.org/ns/1.0}ab", nsmap={None: "http://www.tei-c.org/ns/1.0"})
    for x in sorted(files):
        doc = TeiReader(x)
        for rdg in doc.any_xpath('.//tei:rdg'):
            old_ids = rdg.attrib['wit'].split()
            new_ids = " ".join([f"#{x[7:]}" for x in old_ids])
            rdg.attrib['wit'] = new_ids
        for node in doc.any_xpath('./*'):
            full_doc.append(node)
    return full_doc
