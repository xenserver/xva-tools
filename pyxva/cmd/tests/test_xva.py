import unittest
import os

from mock import MagicMock, patch
from pyxva.cmd import xva


class TestXVAUpdate(unittest.TestCase):

    OVA_XML = "data/ova.xml"

    @patch("pyxva.cmd.xva.extract_xva")
    def setUp(self, mock_extract):

        ova_xml_path = "%s/%s" % (
            os.path.dirname(os.path.realpath(__file__)),
            self.OVA_XML
        )
        with open(ova_xml_path, 'r') as fh:
            ova_data = fh.read()

        mtar = MagicMock()
        mock_extract.return_value = (mtar, ova_data)
        self.xva = xva.open_xva(mtar)

    def test_update_product_version(self):
        self.xva.set_version("product_version", "5.5")
        vrec = self.xva.version()
        self.assertEqual(vrec["product_version"], "5.5")

    def test_update_xapi_minor(self):
        self.xva.set_version("xapi_minor", "2.3")
        vrec = self.xva.version()
        self.assertEqual(vrec["xapi_minor"], "2.3")
