import os

import lxml.etree as ET
from . xml import XMLReader

CUSTOM_XSL = os.path.join(
    os.path.dirname(__file__),
    "xslt",
    "only_text.xsl"
)


class CxReader(XMLReader):

    """ Class to parse and preprocess XML/TEI files for CollateX
    """

    def preprocess(self):

        """
        preprocessing like e.g. removing of obstrusive inline tags `<tei:lb break="no"/>`

        :return: A cleaned lxml.ElementTree
        """
        transform = ET.XSLT(self.custom_xsl)
        new = transform(self.tree)
        return new

    def plain_text(self):

        """ fetches plain text of processed XML/TEI doc

        :return: The processed XML/TEIs plain text
        :rtype: str

        """
        cur_doc = self.cur_doc
        plain_text = " ".join(cur_doc.xpath('.//tei:body//tei:p//text()', namespaces=self.nsmap))
        if self.char_limit:
            return plain_text[:5000]
        return plain_text

    def __init__(
        self,
        custom_xsl=CUSTOM_XSL,
        char_limit=True,
        **kwargs
    ):

        """ initializes the class

        :param custom_xsl: Path to XSLT file used for processing TEIs to return needed (plain) text
        :type custom_xsl: str

        :param char_limit: Should the number of chars of the plaintext be limited?
        :type custom_xsl: bool

        :return: A CxReader instance
        :rtype: `acdh_collatex_utils.CxReader`

        """
        super().__init__(**kwargs)
        self.custom_xsl = ET.parse(custom_xsl)
        self.char_limit = char_limit
        self.cur_doc = self.preprocess()
        self.plain_text = self.plain_text()
        self.collatex_wit = (self.file, self.plain_text)
        self.plaint_text_len = len(self.plain_text)
