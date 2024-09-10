import xml.etree.ElementTree as ET

class DfxpHandler(object):
  def __init__(self, format_handler):
    self.format_handler = format_handler
    self.xml = None
    
  def iterable(self):
    if self.xml is None:
      self._read_xml()
    
    for p in self.xml.findall('.//{http://www.w3.org/ns/ttml}p'):
      for line in self._make_write_back(p):
        yield line
        
  def _read_xml(self):
    ET.register_namespace('', 'http://www.w3.org/ns/ttml')
    self.xml = ET.fromstring(self.format_handler.read())

  def _make_write_back(self, p):
    lines = list()
    lines.append(p.text)
    
    def append_descendent_texts(node, lines):
      for child in node:
        if child.text:
          lines.append(child.text)
        lines.append(child.tail)
        append_descendent_texts(child, lines)
        
    append_descendent_texts(p, lines)
        
    for line_number, line in enumerate(lines):
      def write_back(translated):
        for output_line_number, output_line in enumerate(lines):
          if output_line_number == line_number:
            lines[output_line_number] = translated
          else:
            lines[output_line_number] = output_line
        p.text = lines[0]
        if len(lines) > 1:
          for child in p:
            p.remove(child)
          for line in lines[1:]:
            el = ET.Element('br')
            el.text = ''
            el.tail = line
            p.append(el)

      yield line, write_back
      
  def write(self):
    self.format_handler.write(ET.tostring(self.xml, encoding='unicode', xml_declaration=True))