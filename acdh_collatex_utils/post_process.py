import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from bs4 import BeautifulSoup, Tag

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
