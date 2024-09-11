import os
import sqlite3
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

def stats():
  stats_overall()
  stats_by_language()
  stats_by_engine()
  stats_by_engine_and_language()

def stats_overall():
  total = cur.execute('SELECT COUNT(*) FROM translations').fetchone()[0]
  print(f'Total translations in cache: {total}')

def stats_by_language():
  for row in cur.execute('SELECT source, target, COUNT(*) FROM translations GROUP BY source, target'):
    print(f'{row[0]} -> {row[1]}: {row[2]} translations')

def stats_by_engine():
  for row in cur.execute('SELECT api, COUNT(*) FROM translations GROUP BY api'):
    print(f'{row[0]}: {row[1]} translations')

def stats_by_engine_and_language():
  for row in cur.execute('SELECT api, source, target, COUNT(*) FROM translations GROUP BY api, source, target'):
    print(f'{row[0]}: {row[1]} -> {row[2]}: {row[3]} translations')

def existing_translation(api, source, target, source_text):
  return cur.execute(QUERIES.find_translation, (api, source, target, source_text)).fetchone()

class TranslationCache:
  def __init__(self, api, source, target):
    self.api = api
    self.source = source
    self.target = target
    
  def existing_translation(self, source_text):
    return cur.execute(
      QUERIES.find_translation,
      (self.api, self.source, self.target, source_text)
    ).fetchone()
    
  def store(self, source_text, target_text):
    cur.execute(
      QUERIES.store_translation,
      (self.api, self.source, self.target, source_text, target_text)
    )
    con.commit()  