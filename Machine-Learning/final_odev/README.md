# Makine Öğrenmesi Final Ödevi

## Projenin Amacı
Bu proje, Türkiye Yapay Zeka Akademisi Makine Öğrenmesi dersi final ödevi kapsamında
hazırlanmıştır. Amaç; veri inceleme, veri ön işleme, öznitelik mühendisliği, model
eğitimi, model karşılaştırma, hiperparametre ayarlama ve sonuç yorumlama adımlarını
içeren uçtan uca bir makine öğrenmesi projesi geliştirmektir.

## Veri Seti Açıklaması
`scikit-learn` kütüphanesi içinde hazır bulunan **Breast Cancer Wisconsin** veri
seti kullanılmıştır.

- Satır sayısı: 569
- Öznitelik sayısı: 30 sayısal öznitelik (hücre çekirdeği ölçümleri)
- Hedef değişken: `target` → 0 = Malignant (Kötü Huylu), 1 = Benign (İyi Huylu)
- Problem türü: **İkili sınıflandırma**

Veri seti doğrudan `sklearn.datasets.load_breast_cancer()` fonksiyonu ile yüklenir.

## Proje Adımları
1. Veri setinin yüklenmesi ve temel keşifsel analiz (`head`, `shape`, `dtypes`, `describe`)
2. Verinin Train / Validation / Test kümelerine ayrılması (Data leakage riskini önlemek amacıyla `stratify` ile ilk adımda ayrılmıştır)
3. Eksik değer kontrolü ve Train seti medyanı ile işlenmesi
4. Öznitelik mühendisliği: `cevre_alan_orani` (oran temelli) ve `boyut_grubu` (kategorik grup) üretimi
5. Kategorik değişkenin One-Hot Encoding ile sayısal forma dönüştürülmesi
6. IQR yöntemiyle aykırı değer incelemesi ve sınırlandırılması (Yalnızca Train sınırları temel alınmıştır)
7. Korelasyon analizine dayalı öznitelik seçimi
8. Sayısal özelliklerin `StandardScaler` ile ölçeklenmesi
9. Üç farklı modelin eğitilmesi: Logistic Regression, KNN, Random Forest
10. Modellerin Validation kümesinde Accuracy ve F1-Score ile karşılaştırılması
11. En iyi model için `GridSearchCV` ile hiperparametre ayarlanması
12. En iyi modelin Test verisinde Accuracy, Precision, Recall, F1-Score ve Confusion Matrix ile değerlendirilmesi
13. Bonus: Katsayı analizi ile basit açıklanabilirlik yorumu

## Nasıl Çalıştırılır
```bash
1. Sanal ortam oluşturun ve aktif edin (opsiyonel):
    python -m venv venv
    venv\Scripts\activate     # Windows
    source venv/bin/activate  # Linux/Mac        
2. Gerekli kütüphaneleri yükleyin: pip install -r requirements.txt
3. Python dosyasını çalıştırın: python uctan_uca_makine_ogrenmesi.py
```

Script çalıştığında tüm adımların çıktıları terminale yazdırılır ve test
sonuçlarına ait confusion matrix görseli `confusion_matrix.png` olarak
proje klasörüne kaydedilir.

# Kısa Sonuç Yorumu ve Model Değerlendirmesi

## Model Performansı ve Karşılaştırma
Validation kümesinde yapılan karşılaştırmalar sonucunda en yüksek F1-score başarımını **Logistic Regression** modeli göstermiştir. 

GridSearchCV ile yapılan hiperparametre optimizasyonunun ardından modelin **Test Verisi** üzerindeki başarım metrikleri şu şekildedir:

| Metrik | Skor |
| :--- | :--- |
| **Accuracy (Doğruluk)** | `%97.4` (0.974) |
| **Precision (Kesinlik)** | `%98.6` (0.986) |
| **Recall (Duyarlılık)** | `%97.2` (0.972) |
| **F1-Score** | `%97.9` (0.979) |

> **Kritik Tıbbi Önem (Recall Vurgusu):** Göğüs kanseri teşhisinde kötü huylu (*malignant*) bir vakayı kaçırmak (Yanlış Negatif) hayati risk taşıdığı için yüksek **Recall** (%97.2) değeri projenin en kritik başarısıdır. Test setindeki 43 Kötü Huylu vakadan 41 tanesi doğru tespit edilmiştir.

---

## Açıklanabilirlik ve Önemli Öznitelikler
Logistic Regression model katsayıları (korelasyon analizi ile elendikten sonra) incelendiğinde, teşhis kararında en yüksek etkiye sahip **ilk 3 öznitelik** şunlardır:
1. `worst concave points` (1.13)
2. `worst texture` (-1.09)
3. `worst radius` (-0.95)

---

## Modelin Sınırlılıkları (Limitations)
* **Veri Kısıtı:** Veri setinin 569 satırdan oluşması sebebiyle, farklı `train/test` bölünmelerinde veya farklı veri gruplarında metriklerde küçük sapmalar yaşanabilir.
* **Lineer Bağımlılık:** Öznitelik seçiminde yalnızca doğrusal korelasyon (|r| > 0.25) dikkate alındığı için olası doğrusal olmayan ilişkiler elenmiş olabilir.
