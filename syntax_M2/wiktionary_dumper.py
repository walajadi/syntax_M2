
import xml.etree.ElementTree as ET
tree = ET.parse('/home/slim/Git/syntax_M2/suffixes_xml.php')
root = tree.getroot()
print root.tag
for suffixe in root.iter("a") :
	suff = suffixe.get('title')
	print suff