# sözlük (dictionary)
ogrenci = { # isim = anahtar, ali = key değeri -> {anahtar: değer}
    "isim": "ali", 
    "yas": 25,
    "bolum": "bilgisayar"
}

print(ogrenci)

# dictionary ye erişim
print(ogrenci["isim"]) # ali
print(ogrenci["yas"])

# dictionary yeni değer ekleme
ogrenci["not"] = 85
print(ogrenci) # {'isim': 'ali', 'yas': 25, 'bolum': 'bilgisayar', 'not': 85}

# dictionary değer güncelleme
ogrenci["yas"] = 26
print(ogrenci) # {'isim': 'ali', 'yas': 26, 'bolum': 'bilgisayar', 'not': 85}

# dictionary eleman silme
del ogrenci["bolum"]
print(ogrenci) # {'isim': 'ali', 'yas': 26, 'not': 85}

# anahtarları ve değerleri al
print(ogrenci.keys()) # anahtarlar
print(ogrenci.values()) # değerler
print(ogrenci.items()) # anahtar - değer 

"""
dict_keys(['isim', 'yas', 'not'])
dict_values(['ali', 26, 85])
dict_items([('isim', 'ali'), ('yas', 26), ('not', 85)])
"""