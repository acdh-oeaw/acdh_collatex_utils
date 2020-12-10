import time
import datetime
import requests
import lxml.etree as ET


class XMLReader():

    """ Class to parse, preprocess and save XML/TEI

    :param xml: An XML Document, either a File Path, an URL to an XML or an XML string
    :type xml: str

    :return: A XMLReader instance
    :rtype: `xml.XMLReader`

    """

    def __init__(self, xml=None):

        """ initializes the class

        :param xml: An XML Document, either a File Path, an URL to an XML or an XML string
        :type xml: str

        :return: A XMLReader instance
        :rtype: `xml.XMLReader`

        """
        self.ns_tei = {'tei': "http://www.tei-c.org/ns/1.0"}
        self.ns_xml = {'xml': "http://www.w3.org/XML/1998/namespace"}
        self.ns_tcf = {'tcf': "http://www.dspin.de/data/textcorpus"}
        self.nsmap = {
            'tei': "http://www.tei-c.org/ns/1.0",
            'xml': "http://www.w3.org/XML/1998/namespace",
            'tcf': "http://www.dspin.de/data/textcorpus"
        }
        self.file = xml
        try:
            self.original = ET.parse(self.file)
        except Exception as e:
            try:
                self.original = ET.fromstring(self.file.encode('utf8'))
            except Exception as e:
                r = requests.get(self.file)
                self.original = ET.fromstring(r.text)
        try:
            self.tree = ET.parse(self.file)
        except Exception as e:
            try:
                self.tree = ET.fromstring(self.file.encode('utf8'))
            except Exception as e:
                r = requests.get(self.file)
                self.tree = ET.fromstring(r.text)
        except Exception as e:
            self.parsed_file = "parsing didn't work"

    def return_byte_like_object(self):
        """ returns current doc as byte like object"""

        return ET.tostring(self.tree, encoding="utf-8")

    def return_string(self):

        """
        returns current doc as string

        :rtype: str

        """
        return self.return_byte_like_object().decode('utf-8')

    def tree_to_file(self, file=None):
        """
        saves current tree to file

        :param file: A filename/location to save the current doc
        :type file: str

        :return: The save-location
        :rtype: str

        """
        if file:
            pass
        else:
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
            file = "{}.xml".format(timestamp)

        with open(file, 'wb') as f:
            f.write(ET.tostring(self.tree, encoding="UTF-8"))
        return file
