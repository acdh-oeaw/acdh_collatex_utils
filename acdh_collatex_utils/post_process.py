import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader

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

XHTML_DUMMY_STRING = """
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title></title>
    </head>
    <body>
        <div id="collationTableDiv">
            <table id="collationTable">
                <thead/>
                <tbody/>
            </table>
        </div>
    </body>
</html>
"""


def make_html_table_file(files, match_class="white"):
    """ merges splitted collation tables into singel (X)HTML file """

    rows = []
    for x in files:
        doc = TeiReader(x)
        for r in doc.any_xpath('.//TR')[1:]:
            rows.append(r)
    html_dummy = TeiReader(XHTML_DUMMY_STRING)
    t_head = html_dummy.any_xpath('.//thead')[0]
    t_body = html_dummy.any_xpath('.//tbody')[0]
    t_hrow = ET.Element('tr')
    t_head.append(t_hrow)
    for x in doc.any_xpath('.//TR[1]//TH'):
        t_h = ET.Element('th')
        t_hrow.append(t_h)
        t_h.attrib['scope'] = 'col'
        t_h.text = x.text.split('___')[1]
    t_h = ET.Element('th')
    t_hrow.append(t_h)
    t_h.attrib['scope'] = 'col'
    t_h.text = 'differs'

    for x in rows:
        row = ET.Element('tr')
        t_body.append(row)
        for cell in x.xpath('.//TD'):
            td = ET.Element('td')
            try:
                td.text = cell.text
            except AttributeError:
                td.text = ''
            row.append(td)
        if cell.attrib['bgcolor'] == match_class:
            td = ET.Element('td')
            td.text = 'differs'
        else:
            td = ET.Element('td')
            td.text = 'same'
        row.append(td)
    return html_dummy


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
