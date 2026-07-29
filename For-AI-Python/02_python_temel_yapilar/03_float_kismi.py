# float
pi = 3.14
# pi = 3,14 dersek hata verir çünkü python ondalıklı sayıları nokta ile ayırır.
sicaklik = 35.5
urun_fiyati = 99.99

print(sicaklik)

# matematiksel işlemler
a = 3.5
b = 2.0 

print(a + b) # toplama
print(a/b) # bolme

# ondalık hassasiyeti
print(0.1 + 0.2) # 0.3 -> 0.30000000000000004 

# yuvarlama (round) 
sonuc = 0.1 + 0.2
print(sonuc)

sonuc_yuvarlanmis = round(sonuc, 2)
print(sonuc_yuvarlanmis)

# proje: gelen fiyat üzerinden kdv (%20) hesapla
fiyat = float(input("Fiyat Girin: "))
print(fiyat)
kdvli_fiyat = fiyat + 20*fiyat/100
print(kdvli_fiyat)