import unicodedata

chinese_char = "你"
width = unicodedata.east_asian_width(chinese_char)
print(width)
