import glob
import os

import lxml.etree as ET
import pandas as pd
import collatex
from collatex.core_functions import export_alignment_table_as_tei
from datetime import datetime

from . xml import XMLReader
from . chunks import get_chunks
from . collatex_patch import visualize_table_vertically_with_colors

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

        :param custom_xsl: Path to XSLT file used for\
        processing TEIs to return needed (plain) text
        :type custom_xsl: str

        :param char_limit: Should the number of chars of the\
        plaintext be limited?
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
            print(f"spliitng `self.file_name` did not work due to {e}")
            self.file_name = self.file


def yield_chunks(files, char_limit=True):

    """ utility function to yield chunks from a collection of files

    :param files: List of full file names / file paths to TEI/XML
    :type files: list

    :return: yields chunk dicts
    :rtype: dict:

    """
    for x in files:
        doc = CxReader(xml=x, char_limit=char_limit)
        chunks = doc.yield_chunks()
        for y in chunks:
            yield y


def chunks_to_df(files, char_limit=True):

    """ reads chunks from a list of files into a `pandas.DataFrame`

    :param files: List of full file names / file paths to TEI/XML
    :type files: list

    :return: a pandas.Dataframe with columns `id`, `chunk_nr`, `text`, and `char_count`
    :rtype: pandas.Dataframe
    """
    df = pd.DataFrame(yield_chunks(files, char_limit=char_limit))
    return df


class CxCollate():
    """ Class collate a collection of XML/TEI files and store the results
    """

    def chunk_df(self):
        return chunks_to_df(self.files, self.char_limit)

    def collate(self):
        print(f"start collating {self.file_count} Documents at {datetime.now()}\n")
        print("################################\n")
        files = []
        try:
            os.makedirs(self.output_dir)
        except Exception as e:
            print(f'{self.output_dir}: {self.output_dir} already exists')
        counter = 0
        df = self.df
        for gr in df.groupby('chunk_nr'):
            counter += 1
            start_time = datetime.now()
            print(f"start collating group {counter} at {start_time}")
            f_html = os.path.join(self.output_dir, f"out__{counter:03}.html")
            f_tei = os.path.join(self.output_dir, f"out__{counter:03}.tei")
            collation = collatex.Collation()
            cur_df = gr[1]
            for i, row in cur_df.iterrows():
                print(row['id'])
                collation.add_plain_witness(row['id'], row['text'])
            table = collatex.collate(collation)
            end_time = datetime.now()
            print(f"finished at {end_time} after {end_time - start_time}")
            print(f"saving results to {f_html} and {f_tei}")
            with open(f_html, 'w') as f:
                print(
                    visualize_table_vertically_with_colors(
                        table,
                        collation
                    ),
                    file=f
                )
            with open(f_tei, 'w') as f:
                print(
                    export_alignment_table_as_tei(
                        table,
                        indent=True
                    ),
                    file=f
                )
            files.append([f_html, f_tei])
        print("################################\n")
        print(f"finished collating {self.file_count} Documents at {datetime.now()}\n")
        print("################################\n")
        return files

    def __init__(
        self,
        glob_pattern="./fixtures/*.xml",
        glob_recursive=False,
        output_dir="./tmp",
        custom_xsl=CUSTOM_XSL,
        char_limit=True,
        chunk_size=CHUNK_SIZE,
        **kwargs
    ):

        """ initializes the class

        :param glob_pattern: a `glob.glob` pattern to retrieve a list of files
        :type glob_pattern: 'str'

        :param glob_recursive: should the glob pattern be recursive
        :type glob_recursive: bool

        :param output_dir: Location to store collation results
        :type output_dir: str

        :param custom_xsl: Path to XSLT file used for\
        processing TEIs to return needed (plain) text
        :type custom_xsl: str

        :param char_limit: Should the number of chars of the\
        plaintext be limited?
        :type custom_xsl: bool

        :param chunk_size: Size of chunks yield by `yield_chunks`
        :type custom_xsl: int

        :return: A CxReader instance
        :rtype: `acdh_collatex_utils.CxReader`
        """
        self.glob_pattern = glob_pattern
        self.glob_recursive = glob_recursive
        self.output_dir = output_dir
        self.custom_xsl = ET.parse(custom_xsl)
        self.char_limit = char_limit
        self.chunk_size = chunk_size
        self.files = glob.glob(self.glob_pattern, recursive=False)
        self.file_count = len(self.files)
        self.df = self.chunk_df()
