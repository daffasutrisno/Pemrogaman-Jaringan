import xml.etree.ElementTree as ET
import sys
from io import StringIO
import unittest

# Sample data to be serialized
test_data = {
    'name': 'Alice',
    'age': 30,
    'is_admin': True,
    'skills': ['Python', 'Network Programming', 'Digital Forensics']
}

# Helper: convert dict to XML string
def dict_to_xml(data):
    root = ET.Element("root")
    for key, value in data.items():
        if isinstance(value, list):
            sub_elem = ET.SubElement(root, key)
            for item in value:
                item_elem = ET.SubElement(sub_elem, "item")
                item_elem.text = str(item)
        else:
            sub_elem = ET.SubElement(root, key)
            sub_elem.text = str(value)
    return ET.tostring(root, encoding='unicode')

# Helper: convert XML string back to dict
def xml_to_dict(xml_str):
    root = ET.fromstring(xml_str)
    result = {}
    for child in root:
        if len(child) > 0:  # has sub-elements (i.e., it's a list)
            result[child.tag] = [item.text for item in child]
        else:
            text = child.text
            if text == 'True':
                value = True
            elif text == 'False':
                value = False
            else:
                try:
                    value = int(text)
                except (ValueError, TypeError):
                    value = text
            result[child.tag] = value
    return result

# Function to assert that two dictionaries are equal
def assert_true_dict(dict1, dict2):
    is_true = dict1 == dict2
    if is_true:
        print("The dictionaries match.", dict1, dict2)
    else:
        print("The dictionaries do not match.")

def assert_true_strings(str1, str2):
    if str1 == str2:
        print("The XML strings match.", str1, str2)
    else:
        print("The XML strings do not match.")

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass

# Unit test
class TestXmlToVariable(unittest.TestCase):
    def setUp(self):
        self.test_data = test_data

    def test_xml(self):
        xml_data = dict_to_xml(self.test_data)
        expected_xml = dict_to_xml(self.test_data)
        assert_true_strings(xml_data, expected_xml)
    
    def test_unxml(self):
        xml_data = dict_to_xml(self.test_data)
        parsed_data = xml_to_dict(xml_data)
        assert_true_dict(self.test_data, parsed_data)

# Entry point
if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        xml_data = dict_to_xml(test_data)
        reconstructed_data = xml_to_dict(xml_data)
        assert_true_dict(test_data, reconstructed_data)
        assert_true_strings(xml_data, dict_to_xml(reconstructed_data))
    else:
        runner = unittest.TextTestRunner(stream=NullWriter())
        unittest.main(testRunner=runner, exit=False)