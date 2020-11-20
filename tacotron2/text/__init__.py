import re
from text import cleaners
from text.symbols import vn_symbols, en_symbols
from unicodedata import normalize
from underthesea import word_tokenize
import re
from num2words import num2words
import pandas as pd
import os

vn_symbol_to_id = {s: i for i, s in enumerate(vn_symbols)}
vn_id_to_symbol = {i: s for i, s in enumerate(vn_symbols)}

en_symbol_to_id = {s: i for i, s in enumerate(en_symbols)}
en_id_to_symbol = {i: s for i, s in enumerate(en_symbols)}
_curly_re = re.compile(r'(.*?)\{(.+?)\}(.*)')

en_vn_map = {}
en_vn_df = pd.read_csv('en_vn.csv')
for en_word, vn_word in zip(en_vn_df.en_word.values, en_vn_df.vn_word.values):
  en_word = en_word.lower()
  vn_word = vn_word.lower()
  en_vn_map[en_word] = vn_word


def vi_num2words(num):
    return num2words(num, lang='vi')


def convert_time_to_text(time_string):
    try:
        h, m = time_string.split(":")
        time_string = vi_num2words(int(h)) + " giờ " + \
            vi_num2words(int(m)) + " phút"
        return time_string
    except:
        return None


def replace_time(text):
    result = re.findall(r'\d{1,2}:\d{1,2}|', text)
    match_list = list(filter(lambda x: len(x), result))

    for match in match_list:
        if convert_time_to_text(match):
            text = text.replace(match, convert_time_to_text(match))
    return text


def replace_number(text):
    return re.sub('(?P<id>\d+)', lambda m: vi_num2words(int(m.group('id'))), text)


def remove_invalid_character(text):
  _pad = '_'
  _punctuation = '!\'(),.:;? '
  _special = '-'
  vn_letters = '0123456789aáảàãạâấẩầẫậăắẳằẵặbcdđeéẻèẽẹêếểềễệfghiíỉìĩịjklmnoóỏòõọôốổồỗộơớởờỡợpqrstuúủùũụưứửừữựvwxyýỷỳỹỵz'
  vn_symbols = [_pad] + list(_special) + \
      list(_punctuation) + list(vn_letters)
  pattern_unchars_vn = f"[^{vn_symbols}]"
  text = re.sub(pattern_unchars_vn, '', text.strip())
  return text


def map_english_vn(text):
    global en_vn_map
    for k, v in en_vn_map.items():
        text = text.replace(k, v)
    return text

def normalize_text(text):
  text = text.strip()
  text = text.replace("<br>", "")
  text = normalize("NFC", text)
  text = text.lower()
  text = replace_time(text)
  text = replace_number(text)
  text = map_english_vn(text)
  text = text.replace('-', '_')
  text = text.replace('"', " ")
  text = remove_invalid_character(text)
  text = re.sub("\.+", ".", text)
  text = re.sub("[?!;…\"]", " . ", text)
  text = re.sub("[:/]", " , ", text)
  text = re.sub("\s+", " ", text)
  return text


def text_to_sequence(text, cleaner_names, normalize=True):
  sequence = []
  if normalize:
    text = normalize_text(text)
  while len(text):
    m = _curly_re.match(text)
    if not m:
      sequence += _symbols_to_sequence(_clean_text(text, cleaner_names))
      break
    sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names))
    sequence += _arpabet_to_sequence(m.group(2))
    text = m.group(3)

  return sequence


def sequence_to_text(sequence):
  _id_to_symbol = vn_id_to_symbol

  result = ''
  for symbol_id in sequence:
    if symbol_id in _id_to_symbol:
      s = _id_to_symbol[symbol_id]

      if len(s) > 1 and s[0] == '@':
        s = '{%s}' % s[1:]
      result += s
  return result.replace('}{', ' ')


def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text)
  return text


def _symbols_to_sequence(symbols):
  _symbol_to_id = vn_symbol_to_id
  return [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s, _symbol_to_id)]


def _arpabet_to_sequence(text):
  return _symbols_to_sequence(['@' + s for s in text.split()])


def _should_keep_symbol(s, _symbol_to_id):
  return s in _symbol_to_id and s is not '_' and s is not '~'
