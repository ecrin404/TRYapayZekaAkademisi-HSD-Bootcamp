"""
Öğrenci Not Analiz Projesi

Plan/Program:
    1. CSV dosyasından öğrenci verileri oku
    2. Temel istatistiksel hesaplamalar (NumPy)
    3. Filtreleme (Pandas)
    4. Öğrenci notu görselleştirme (Matplotlib)
    5. OOP ile yapıyı class üzerinde toplama
    6. Hata yönetimi (Try-Except)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class OgrenciNotAnalizSistemi:

    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu
        self.df = None

    def veriyi_oku(self):
        try:
            # encoding="utf-8" Türkçe karakter desteği sağlar
            self.df = pd.read_csv(self.dosya_yolu, encoding="utf-8")

            if self.df.empty:
                raise ValueError("CSV dosyası boş veya veri içermiyor.")

            # Gerekli sütun kontrolü
            gerekli_sutunlar = {"isim", "yas", "bolum", "not"}
            if not gerekli_sutunlar.issubset(self.df.columns):
                raise ValueError(f"Eksik sütunlar var! Gerekli sütunlar: {gerekli_sutunlar}")

            # Not sütununu sayısal tipe çevir
            self.df["not"] = pd.to_numeric(self.df["not"], errors="raise")

            print("--- VERİ BAŞARIYLA OKUNDU ---")
            print(self.df)
            print("-" * 35)

        except FileNotFoundError:
            print(f"Hata: '{self.dosya_yolu}' adında bir dosya bulunamadı.")
            self.df = None
        except pd.errors.EmptyDataError:
            print("Hata: CSV dosyası tamamen boş!")
            self.df = None
        except ValueError as error:
            print(f"Veri Hatası: {error}")
            self.df = None
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")
            self.df = None

    def numpy_ile_hesaplama(self):
        try:
            if self.df is None:
                raise ValueError("İstatistik hesabı için önce geçerli bir veri yüklenmelidir.")

            notlar = self.df["not"].to_numpy()

            print("\n--- GENEL İSTATİSTİKLER ---")
            print(f"Ortalama Not      : {np.mean(notlar):.2f}")
            print(f"En Yüksek Not     : {np.max(notlar)}")
            print(f"En Düşük Not      : {np.min(notlar)}")
            print(f"Standart Sapma    : {np.std(notlar):.2f}")
            print("-" * 35)

        except ValueError as hata:
            print(f"Hata: {hata}")

    def pandas_ile_filtreleme(self):
        try:
            if self.df is None:
                raise ValueError("Filtreleme için önce veri okunmalıdır.")

            print("\n--- FİLTRELEME SONUÇLARI ---")

            # 1. Notu 80'den büyük olanlar
            yuksek_notlular = self.df[self.df["not"] > 80]
            print(f"\nNotu 80'den büyük olan öğrenciler:\n{yuksek_notlular}")

            # 2. Bölümü Yapay Zeka olanlar (Harf duyarsız yapıp tüm tabloyu basıyoruz)
            yz_ogrencileri = self.df[self.df["bolum"].str.lower() == "yapay zeka"]
            print(f"\nBölümü Yapay Zeka olanlar:\n{yz_ogrencileri}")

            # 3. Yaşı 22'den büyük olanlar
            yasi_buyukler = self.df[self.df["yas"] > 22]
            print(f"\n22 yaşından büyük olan öğrenciler:\n{yasi_buyukler}")
            print("-" * 35)

        except ValueError as hata:
            print(f"Hata: {hata}")

    def grafik_ciz(self):
        try:
            if self.df is None:
                raise ValueError("Grafik çizimi için önce veri okunmalı.")

            plt.figure(figsize=(9, 5))

            # Renkli sütunlar oluşturma
            bars = plt.bar(self.df["isim"], self.df["not"], color="skyblue", edgecolor="black")

            # Çubukların üzerine not değerlerini yazma
            for bar in bars:
                yval = bar.get_height() # Sütunun yüksekliğini al, yani öğrencinin not değerini
                plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval}", ha='center', va='bottom', fontweight='bold')

                # Grafiğe metin ekle:
                # - X konumu: bar.get_x() + bar.get_width()/2 -> Sütunun tam yatay ortası
                # - Y konumu: yval + 1 -> Çubuğun en üst sınırının 1 birim yukarısı (değer çubuğa yapışmasın diye)
                # - Metin: f"{yval}" -> Yazdırılacak not değeri
                # - ha='center': Metni yatayda ortala
                # - va='bottom': Metnin alt kısmını hizalama noktasına al
            

            plt.title("Öğrenci Not Dağılımı", fontsize=14, fontweight="bold")
            plt.xlabel("Öğrenci İsimleri", fontsize=11)
            plt.ylabel("Notlar", fontsize=11)
            plt.ylim(0, 110) # Y eksenine biraz boşluk bırakalım
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Grafik çizilirken hata oluştu: {e}")

    def tum_analizi_calistir(self):
        self.veriyi_oku()

        # Veri okunamadıysa işlemi durdur
        if self.df is None:
            print("Analiz iptal edildi. Lütfen CSV dosyanızı kontrol edin.")
            return

        self.numpy_ile_hesaplama()
        self.pandas_ile_filtreleme()
        self.grafik_ciz()


# Program başlangıcı
if __name__ == "__main__":
    dosya_yolu = "ogrenci_notlari.csv"
    sistem = OgrenciNotAnalizSistemi(dosya_yolu)
    sistem.tum_analizi_calistir()