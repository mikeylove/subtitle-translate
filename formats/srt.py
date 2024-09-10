import srt
from html.parser import HTMLParser

class SrtHandler:
  def __init__(self, format_handler):
    self.format_handler = format_handler
    self.subtitles = list()

  def write(self):
    self.format_handler.write(self._to_srt())

  def _to_srt(self):
    return srt.compose(self.subtitles)

  def iterable(self):
    if not self.subtitles:
      self._read_subtitles()
      
    for i, subtitle in enumerate(self.subtitles):
      for line in self._make_write_back(i, subtitle):
        yield line

  def _read_subtitles(self):
    self.subtitles = list(srt.parse(self.format_handler.read()))
      
  def _make_write_back(self, i, subtitle):
    lines = subtitle.content.split('\n')
    for line_number, line in enumerate(lines):
      parser = SrtHTMLParser()
      parser.feed(line)
      input_string = "".join(parser.fed)
      parser.close()

      def write_back(translated):
        for output_line_number, output_line in enumerate(lines):
          if output_line_number == line_number:
            lines[output_line_number] = parser.unwrap(translated)
          else:
            lines[output_line_number] = output_line
          self.subtitles[i].content = '\n'.join(lines)

      yield input_string, write_back

class SrtHTMLParser(HTMLParser):
  def __init__(self):
    super().__init__()
    self.reset()
    self.fed = []
    self.tag_stack = []

  def handle_starttag(self, tag, attrs):
    if len(self.fed) > 0: return
    
    self.tag_stack.append((tag, attrs))
    
  def handle_data(self, data):
    self.fed.append(data)
    
  def unwrap(self, new_text):
    open_tags = ''
    for tag, attrs in self.tag_stack:
      if len(attrs) > 0:
        attrs_text = ' '.join([f'{k}="{v}"' for k, v in attrs])
        tag_text = f'<{tag} {attrs_text}>'
      else:
        tag_text = f'<{tag}>'
      open_tags += tag_text
      
    close_tags = ''
    for tag, _ in self.tag_stack[::-1]:
      close_tags += f'</{tag}>'  
    
    return f'{open_tags}{new_text}{close_tags}'
