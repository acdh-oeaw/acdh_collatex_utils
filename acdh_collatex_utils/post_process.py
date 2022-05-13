import os
import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from bs4 import BeautifulSoup, Tag


LEM_XSL = os.path.join(
    os.path.dirname(__file__),
    "xslt",
    "lem.xsl"
)


TEI_DUMMY_STRING = """
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Title</title>
         </titleStmt>
         <publicationStmt>
            <p>Publication Information</p>
         </publicationStmt>
         <sourceDesc>
            <listWit/>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
         <ab/>
      </body>
  </text>
</TEI>
"""


def merge_html_fragments(files):
    """ merges splitted collation tables into single (X)HTML file

    :param files: A list of absolute file paths

    :return: a beautiful soup object providing an html-table
    """

    tr = []
    for x in sorted(files):
        with open(x, 'r') as f:
            soup = BeautifulSoup(f, "html.parser")
            for row in soup.find_all('tr'):
                tr.append(row)
    new_soup = BeautifulSoup()
    table = Tag(new_soup, name="table")
    new_soup.append(table)
    for x in tr:
        table.append(x)
    return new_soup


def merge_tei_fragments(files):
    """ takes a list of files (fullpaths) and retuns a single tei:ab element.etree node"""
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


def make_full_tei_doc(input_file):
    """ takes the rusult of merged collated tei fragments\
        and returns a valid TEI document as TeiReader object"""
    tei_dummy = TeiReader(TEI_DUMMY_STRING)
    crit_app = TeiReader(input_file)
    body = tei_dummy.any_xpath('.//tei:ab')[0]
    list_wit_node = tei_dummy.any_xpath('.//tei:listWit')[0]
    wit_set = set()

    for rdg in crit_app.any_xpath('.//tei:rdg/@wit'):
        for w in rdg.split():
            wit_set.add(w[1:])

    for x in list(sorted(wit_set)):
        w_node = ET.Element("{http://www.tei-c.org/ns/1.0}witness", nsmap={None: "http://www.tei-c.org/ns/1.0"})
        w_node.attrib['{http://www.w3.org/XML/1998/namespace}id'] = x
        w_node.text = x
        list_wit_node.append(w_node)
    for x in crit_app.any_xpath('./*'):
        body.append(x)
    return tei_dummy


def make_positive_app(input_file):
    """ transform negativ apparat into positive one
    :param input_file: A TEI/XML file with listWit and app elements

    :return: A TeiReader instance
    """
    doc = TeiReader(input_file)
    wit_ids = set(doc.any_xpath('.//tei:witness/@xml:id'))
    for x in doc.any_xpath('.//tei:app'):
        cur_wit_ids = set()
        for wit in x.xpath('./*'):
            for w in wit.attrib['wit'].split(' '):
                cur_wit_ids.add(w[1:])
        missing = list(wit_ids.difference(cur_wit_ids))
        if missing:
            rdg = ET.Element('{http://www.tei-c.org/ns/1.0}rdg')
            rdg.attrib['wit'] = " ".join([f"#{x}" for x in missing])
            x.append(rdg)
    return doc


def define_readings(input_file, rdg_wit_id, lem_xsl=LEM_XSL):
    """ transforms tei:rdg[@weit='rdg_wit_id'] into tei:lem

    :param input_file: XML/TEI file with tei:app
    :param rdg_wit_id: the xml:id of the witness for the lemma
    :param lem_xsl: The XSLT doing the transformation

    :return: the output of the transformation
    """
    with open(lem_xsl, 'r', encoding='utf-8') as f:
        proper_xsl = f.read().replace('!!!REPLACEME!!!', rdg_wit_id)
    input_doc = TeiReader(input_file)
    xsl_doc = TeiReader(proper_xsl)
    transform = ET.XSLT(xsl_doc.tree)
    out = transform(input_doc.tree)
    return out
