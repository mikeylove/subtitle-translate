from formats import FormatHandler
import os
import sqlite3
import translators as ts
from types import SimpleNamespace

con = sqlite3.connect(os.getenv('TRANSLATE_CACHE_DB_FILENAME', 'translate-cache.db'))
cur = con.cursor()

QUERIES = SimpleNamespace(**{
  'find_table': "SELECT name FROM sqlite_master WHERE name='translations'",
  'create_table': 'CREATE TABLE translations (id INTEGER PRIMARY KEY, api TEXT, source TEXT, target TEXT, source_text TEXT, target_text TEXT)',
  'find_translation': 'SELECT target_text FROM translations WHERE api=? AND source=? AND target=? AND source_text=?',
  'store_translation': 'INSERT INTO translations (api, source, target, source_text, target_text) VALUES (?, ?, ?, ?, ?)',
})

if cur.execute(QUERIES.find_table).fetchone() is None:
  cur.execute(QUERIES.create_table)

def existing_translation(api, source, target, source_text):
  return cur.execute(QUERIES.find_translation, (api, source, target, source_text)).fetchone()

def translate_subtitles(format, input_file, from_lang, output_file, to_lang):
  format_handler = FormatHandler(input_file, output_file).for_format(format)
  for subtitle, write_back in format_handler.iterable():
    write_back(translate(subtitle, from_lang, to_lang))
  format_handler.write()

def translate_and_store(content, from_lang, to_lang):
  stored_translation = existing_translation('translators-google', from_lang, to_lang, content)

  if stored_translation:
    return stored_translation[0], True

  translated_text = ts.translate_text(content, 'google', from_language=from_lang, to_language=to_lang)
  cur.execute(QUERIES.store_translation, ('translators-google', from_lang, to_lang, content, translated_text))
  con.commit()

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
