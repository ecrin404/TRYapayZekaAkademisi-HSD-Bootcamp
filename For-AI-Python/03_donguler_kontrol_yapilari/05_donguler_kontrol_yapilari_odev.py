# ========================================================================
# SORU 1 (IF)
# Kullanıcıdan bir sayı alın.
# Sayı pozitifse "Pozitif", negatifse "Negatif", sıfırsa "Sıfır" yazdırın.
# ========================================================================

sayi = int(input("Bir sayı giriniz: "))

if sayi > 0:
    print("Pozitif")
elif sayi < 0:
    print("Negatif")
else:
    print("Sıfır")

print("-" * 50)

# ============================================================
# SORU 2 (FOR)
# 1'den 10'a kadar (10 dahil) sayıları yazdırın.
# Ayrıca bu sayıların toplamını hesaplayıp ekrana yazdırın.
# ============================================================

toplam = 0

for a in range(1, 11):
    print(a)
    toplam += a

print("Toplam:", toplam)
print("-" * 50)

# ========================================================================
# SORU 3 (WHILE)
# Kullanıcıdan "q" yazana kadar sürekli giriş alın.
# Kullanıcı her giriş yaptığında "Girdiniz: ..." şeklinde ekrana yazdırın.
# Kullanıcı "q" yazarsa döngü bitsin ve "Çıkış yapıldı" yazsın.
# ========================================================================

while True:
    giris = input("Bir şey yazın (çıkmak için q yazın): ")
    
    if giris == "q":
        break 
        
    print(f"Girdiniz: {giris}")

print("Çıkış yapıldı!")
print("-" * 50)

# =========================================================================
# SORU 4 (NESTED)
# 1'den 20'ye kadar sayıları dolaşın.
# Eğer sayı çiftse "Çift", tekse "Tek" yazdırın.
# Ayrıca sayı 10'dan büyükse yanına "Büyük", değilse "Küçük/Eşit" yazdırın.
# Örnek çıktı: 12 -> Çift - Büyük
# =========================================================================

for i in range(1, 21):
    if i % 2 == 0:
        if i > 10:
            print(f"{i} -> Çift - Büyük")
        else:
            print(f"{i} -> Çift - Küçük/Eşit")
    else:
        if i > 10:
            print(f"{i} -> Tek - Büyük")
        else:
            print(f"{i} -> Tek - Küçük/Eşit")

print("-" * 50)