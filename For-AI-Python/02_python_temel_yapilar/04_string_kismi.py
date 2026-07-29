# string
isim = "kaan" # çift tırnak örneği
sirket = 'ucanble' # tek tırnak örneği

bilgi = "kaan hocanın şirketinin ismi ucanble teknoloji"
print(bilgi)

# string birleştirme (concatenation)
isim = "kaan"
sirket = 'ucanble'
bilgi2 = isim + " hocanın şirketinin ismi " + sirket + " " + "teknoloji"
print(bilgi2)

# string ve sayı birleştirme
yas = 35 # int
int_to_str = str(yas) # 35 -> "35"
isim = "kaan" # string
sonuc = isim + " hocanın yaşı: " + int_to_str # kaan hocanın yaşı: 35
print(sonuc)

kurulum_tarihi = 2023
print("Ucanble teknoloji " + str(kurulum_tarihi) +  " yılında kurulmuştur.")
print(f"Ucanble teknoloji {kurulum_tarihi} yılında kurulmuştur.") # f string

accuracy = 95
print(f"Karar ağacı accuracy: {accuracy} %")

# string indexleme
kelime = "python" # string = karakter dizisi
print(kelime[0])
print(kelime[3])

# string metotları
metin = "PythoN"
metin_kucuk_harf = metin.lower()
print(metin_kucuk_harf)

# uzunluk bulma
metin = "python"
metin_uzunlugu = len(metin)
print(metin_uzunlugu)

# yer değiştirme
metin = "python"
print(metin.replace("o", "O"))