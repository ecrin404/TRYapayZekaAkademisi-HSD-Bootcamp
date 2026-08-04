# Makine Öğrenmesi Ara Ödev – Müşteri Ayrılma Tahmini

## Projenin Amacı
Bu proje, temel bir makine öğrenmesi akışını (veri oluşturma, veri ön işleme,
öznitelik üretme, train-validation-test bölme, model eğitimi ve
sınıflandırma metrikleriyle değerlendirme) küçük ve anlaşılır bir
sınıflandırma problemi üzerinde uygulamak için hazırlanmıştır.

Problem: Bir müşterinin abonelikten ayrılıp ayrılmayacağını (**churn**)
tahmin etmek.

Veri seti; yaş, gelir, abonelik süresi, destek talebi sayısı, şehir ve
üyelik tipi gibi sütunlar içeren, kod içinde otomatik olarak üretilen ve
kaydedilen sentetik (yapay) bir veri setidir.

## Proje İçeriği
- `musteri_ayrilma_tahmini.py` → Tüm akışı içeren tek Python dosyası
  (veri üretimi, ön işleme, öznitelik mühendisliği, modelleme, değerlendirme)
- `musteri_verisi.csv` → Kod ilk çalıştırıldığında otomatik olarak üretilip
  kaydedilen veri seti (300 satır). `np.random.seed(42)` sabit olduğu için
  kod her çalıştırıldığında aynı veri yeniden üretilir.
- `requirements.txt` → Gerekli kütüphaneler
- `README.md` → Bu dosya

## Nasıl Çalıştırılır?

1. Sanal ortam (virtual environment) oluşturun ve aktive edin:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```

2. Gerekli kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt
   ```

3. Python dosyasını çalıştırın:
   ```bash
   python musteri_ayrilma_tahmini.py
   ```

4. Kod çalıştığında sırasıyla şu adımları uygular ve sonuçları terminale
   yazdırır:
   - Sentetik veri setinin oluşturulması ve ilk incelenmesi
   - Eksik değer kontrolü ve doldurma
   - Öznitelik üretimi (`gelir_grubu`, `destek_talebi_var_mi`)
   - Kategorik değişkenlerin One-Hot Encoding ile dönüştürülmesi
   - Train (%60) / Validation (%20) / Test (%20) olarak stratify ile bölme
   - Sayısal değişkenlerin ölçeklenmesi (StandardScaler)
   - Logistic Regression ve KNN modellerinin eğitilmesi
   - Validation sonuçlarına göre model karşılaştırması
   - Seçilen modelin test seti üzerinde confusion matrix, accuracy,
     precision, recall ve F1-score ile değerlendirilmesi
   - Kısa bir sonuç yorumu

