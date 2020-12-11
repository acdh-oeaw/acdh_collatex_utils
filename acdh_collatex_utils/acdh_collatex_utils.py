import os

import lxml.etree as ET
from . xml import XMLReader
from . chunks import get_chunks

CUSTOM_XSL = os.path.join(
    os.path.dirname(__file__),
    "xslt",
    "only_text.xsl"
)

CHUNK_SIZE = 2000


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

    def yield_chunks(self):

        """ yields chunks of the object's plain text

        :return:  yields dicts like `{"id": "example_text.txt", "chunk_nr": "001", "text": "text of chunk", "char_count": 13}`
        :rtype: dict
        """
        return get_chunks(self.plain_text, self.chunk_size, self.file_name)

    def __init__(
        self,
        custom_xsl=CUSTOM_XSL,
        char_limit=True,
        chunk_size=CHUNK_SIZE,
        **kwargs
    ):

        """ initializes the class

        :param custom_xsl: Path to XSLT file used for processing TEIs to return needed (plain) text
        :type custom_xsl: str

        :param char_limit: Should the number of chars of the plaintext be limited?
        :type custom_xsl: bool

        :param chunk_size: Size of chunks yield by `yield_chunks`
        :type custom_xsl: int

        :return: A CxReader instance
        :rtype: `acdh_collatex_utils.CxReader`

        """
        super().__init__(**kwargs)
        self.custom_xsl = ET.parse(custom_xsl)
        self.char_limit = char_limit
        self.chunk_size = chunk_size
        self.cur_doc = self.preprocess()
        self.plain_text = self.plain_text()
        self.collatex_wit = (self.file, self.plain_text)
        self.plaint_text_len = len(self.plain_text)
        try:
            self.file_name = os.path.split(self.file)[1]
        except Exception as e:
            self.file_name = self.file


def yield_chunks(files):
    """ utility function to yield chunks from a collection of files

    :param files: List of full file names / file paths to TEI/XML
    :type files: list

    :return: yields chunk dicts
    :rtype: dict:

    """
    for x in files:
        doc = CxReader(xml=x)
        chunks = doc.yield_chunks()
        for y in chunks:
            yield y
