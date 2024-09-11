from cache import TranslationCache
from engine import translators_google
from formats import FormatHandler

def translate_subtitles(format, input_file, from_lang, output_file, to_lang):
  format_handler = FormatHandler(input_file, output_file).for_format(format)
  for subtitle, write_back in format_handler.iterable():
    write_back(translate(subtitle, from_lang, to_lang))
  format_handler.write()

def translate_and_store(content, from_lang, to_lang):
  translator = translators_google
  cache = TranslationCache(translator.key, from_lang, to_lang)

  stored_translation = cache.existing_translation(content)

  if stored_translation:
    return stored_translation[0], True

  translated_text = translator.translate(content, from_lang, to_lang)

  cache.store(content, translated_text)

  return translated_text, False

def translate(content, from_lang, to_lang):
  print(f'Translating "{content}" from {from_lang} to {to_lang} -> ', end='')
  
  try:
    translation, from_cache = translate_and_store(content, from_lang, to_lang)

    print(f'"{translation}" {"(cached)" if from_cache else ""}')

    return translation
  except Exception as e:
    print(f'Error translating: {e}')
    return content
