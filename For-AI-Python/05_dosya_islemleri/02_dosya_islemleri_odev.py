# SORU 1
# "notlar.txt" adında bir dosya oluşturun ve içine
# 5 öğrencinin notunu yazın. Her not ayrı satırda olsun.

not_listesi = [70, 85, 40, 90, 60]

with open("notlar.txt", "w", encoding="utf-8") as dosya:
    for n in not_listesi:
        dosya.write(f"{n}\n")

# SORU 2
# Bu dosyayı okuyun ve:
# - Notların ortalamasını hesaplayın
# - En yüksek notu bulun
# - En düşük notu bulun

notlar = []

with open("notlar.txt", "r", encoding="utf-8") as dosya:
    notlar = [int(satir.strip()) for satir in dosya]

ortalama = sum(notlar) / len(notlar)
en_yuksek = max(notlar)
en_dusuk = min(notlar)

print("Notlar:", notlar)
print("Ortalama:", ortalama)
print("En yüksek not:", en_yuksek)
print("En düşük not:", en_dusuk)

# SORU 3
# Eğer ortalama 50'den büyükse "Sınıf geçti"
# değilse "Sınıf kaldı" sonucunu
# "sonuc.txt" dosyasına kaydedin.

if ortalama >= 50:
    sonuc = "Sınıf geçti"
else:
    sonuc = "Sınıf kaldı"

with open("sonuc.txt", "w", encoding="utf-8") as dosya:
    dosya.write(f"Ortalama: {ortalama:.2f}\n")
    dosya.write(f"Sonuç: {sonuc}")

print("Sonuç sonuc.txt dosyasına kaydedildi.")