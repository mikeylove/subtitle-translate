from formats import FormatHandler
import os
import sqlite3
import translators as ts

con = sqlite3.connect(os.getenv('TRANSLATE_CACHE_DB_FILENAME', 'translate-cache.db'))
cur = con.cursor()

if cur.execute("SELECT name FROM sqlite_master WHERE name='translations'").fetchone() is None:
  cur.execute("CREATE TABLE translations (id INTEGER PRIMARY KEY, api TEXT, source TEXT, target TEXT, source_text TEXT, target_text TEXT)")

def existing_translation(api, source, target, source_text):
  return cur.execute("SELECT target_text FROM translations WHERE api=? AND source=? AND target=? AND source_text=?", (api, source, target, source_text)).fetchone()

def translate_subtitles(format, input_file, from_lang, output_file, to_lang):
  format_handler = FormatHandler(input_file, output_file).for_format(format)
  for subtitle, write_back in format_handler.iterable():
    write_back(translate(subtitle, from_lang, to_lang))
  format_handler.write()

def translate(content, from_lang, to_lang):
  print(f'Translating "{content}" from {from_lang} to {to_lang} -> ', end='')
  
  try:
    stored_translation = existing_translation('translators-google', from_lang, to_lang, content)

    if stored_translation is None:
      translated_text = ts.translate_text(content, 'google', from_language=from_lang, to_language=to_lang)
      cur.execute("INSERT INTO translations (api, source, target, source_text, target_text) VALUES (?, ?, ?, ?, ?)", ('translators-google', from_lang, to_lang, content, translated_text))
      con.commit()
      print(f'"{translated_text}"')
    else:
      translated_text = stored_translation[0]
      print(f'"{translated_text}" (cached)')
    
    return translated_text
  except Exception as e:
    print(f'Error translating: {e}')
    return content
