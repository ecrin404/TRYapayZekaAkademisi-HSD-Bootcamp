# integer (int)

yas = 35
ogrenci_sayisi = 55000
sicaklik = -15 

print(yas)
print(35)

# hesaplama
a = 10
b = 5 

toplam = a + b  # a ve b değerlerini toplamış oluruz
print(toplam)

carpma = a * b
print(carpma)

cikarma = a - b
print(cikarma)

bolme = a/b
print(bolme)

# gercek hayat örneği: ürün sayısı var ve her bir ürünün birim fiyatı - amaç: toplam ürün fiyatı
urun_sayisi = 8   # 8 adet ürün var
birim_fiyat = 10  # birim fiyat 10 tl

toplam = urun_sayisi * birim_fiyat
print(toplam)

# zam uygulaması
birim_fiyat = 10
yuzde = int(input("Yüzdeyi yazın: "))
print(yuzde)
zamli_fiyat = birim_fiyat + birim_fiyat*yuzde/100
print(zamli_fiyat)
