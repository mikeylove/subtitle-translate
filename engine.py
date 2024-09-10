import translators as ts

class TranslationEngine:
  def __init__(self, key, handler):
    self.key = key
    self.handler = handler
    
  def translate(self, text):
    return self.handler(text)
  
def _translators_google(text, from_lang, to_lang):
  return ts.translate_text(text, 'google', from_language=from_lang, to_language=to_lang)

translators_google = TranslationEngine('translators-google', _translators_google)