"""
Makine Öğrenmesi Ara Ödev - Müşteri Ayrılma Tahmini

Amaç:
    Bu proje, temel bir makine öğrenmesi akışını (veri oluşturma, ön işleme,
    öznitelik üretme, train-validation-test bölme, model eğitimi ve
    değerlendirme) küçük ve anlaşılır bir sınıflandırma problemi üzerinde
    uygulamak için hazırlanmıştır. Amaç, bir müşterinin abonelikten
    ayrılıp ayrılmayacağını (churn) tahmin etmektir.

Kullanılan Kütüphaneler:
    - pandas       : veri okuma / işleme
    - numpy        : sayısal işlemler ve sentetik veri üretimi
    - scikit-learn : ön işleme, model eğitimi ve değerlendirme metrikleri

Çalıştırma Adımları:
    1) Sanal ortam oluşturun ve aktif edin (opsiyonel):
        python -m venv venv
        venv\Scripts\activate     # Windows
        source venv/bin/activate  # Linux/Mac
        
    2) requirements.txt içindeki kütüphaneleri kurun:
         pip install -r requirements.txt
    3) Dosyayı çalıştırın:
         python musteri_ayrilma_tahmini.py
    4) Kod; veri setini kendi içinde oluşturur, kaydeder, ön işler, iki model eğitir
       ve sonuçları ekrana yazdırır.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

np.random.seed(42)

def bolum_yazdir(numara, baslik):
    """
    Terminal çıktısında adımları tutarlı ve düzenli bir şekilde
    ayırmak için kullanılan basit bir başlık yazdırma fonksiyonu.
    """
    print("\n" + "-" * 88)
    print(f"{numara}) {baslik}")
    print("-" * 88)

# ---------------------------------------------------------------------------
# 2) Veri setini pandas DataFrame olarak hazırla
# ---------------------------------------------------------------------------
def veri_seti_olustur(n = 300):
    """
    Müşteri ayrılma tahmini için basit, sentetik bir veri seti üretir.
    Sütunlar: yas, gelir, abonelik_suresi, destek_talebi_sayisi,
              sehir, uyelik_tipi, churn
    """
    sehirler = ["Istanbul", "Ankara", "Izmir", "Bursa"]
    uyelik_tipleri = ["Standart", "Premium", "Gold"]

    yas = np.random.randint(18, 70, size = n)
    gelir = np.random.randint(4000, 40000, size = n)
    abonelik_suresi = np.random.randint(1, 60, size = n)          
    destek_talebi_sayisi = np.random.randint(0, 10, size = n)
    sehir = np.random.choice(sehirler, size = n)
    uyelik_tipi = np.random.choice(uyelik_tipleri, size = n, p = [0.5, 0.3, 0.2])

    # np.where(koşul, doğruysa_değer, yanlışsa_değer)
    destek_kurali = np.where(destek_talebi_sayisi > 5, 1, 0)
    abonelik_kurali = np.where(abonelik_suresi < 6, 1, 0)
    gelir_kurali = np.where(gelir < 8000, 1, 0)

    churn_skoru = (
        destek_kurali * 0.4
        + abonelik_kurali * 0.3
        + gelir_kurali * 0.2
        + np.random.rand(n) * 0.3
    )
    churn = np.where(churn_skoru > 0.5, 1, 0)

    df = pd.DataFrame({
        "yas": yas,
        "gelir": gelir,
        "abonelik_suresi": abonelik_suresi,
        "destek_talebi_sayisi": destek_talebi_sayisi,
        "sehir": sehir,
        "uyelik_tipi": uyelik_tipi,
        "churn": churn,
    })

    # Bazı eksik değerler kasıtlı olarak eklendi ki eksik değer
    # kontrolü/temizleme adımı da anlamlı olsun.
    eksik_indeksler = np.random.choice(df.index, size = 10, replace = False)
    df.loc[eksik_indeksler, "gelir"] = None

    return df


df = veri_seti_olustur(n = 300)

# Üretilen veri setini bir CSV dosyasına da kaydediyoruz. 
# np.random.seed(42) sabit olduğu için 
# kod her çalıştırıldığında aynı veri üretilir.
df.to_csv("musteri_verisi.csv", index = False)
print("\nVeri seti 'musteri_verisi.csv' dosyasına kaydedildi.")


# ---------------------------------------------------------------------------
# 3) İlk satırlar, satır-sütun sayısı ve hedef değişken dağılımı
# ---------------------------------------------------------------------------
bolum_yazdir(3, "VERİ SETİ İNCELEME")
 
print("İlk 5 satır:")
print(df.head())
 
print(f"\nSatır sayısı: {df.shape[0]}, Sütun sayısı: {df.shape[1]}")

print("\nHedef değişken (churn) dağılımı:")
print(df["churn"].value_counts())
print(df["churn"].value_counts(normalize = True).round(3))


# ---------------------------------------------------------------------------
# 4) Eksik değer kontrolü ve temizleme
# ---------------------------------------------------------------------------
bolum_yazdir(4, "EKSİK DEĞER KONTROLÜ")
 
print("Eksik değer sayıları:")
print(df.isnull().sum())

# 'gelir' sütunundaki eksik değerleri medyan ile dolduruyoruz.
df["gelir"] = df["gelir"].fillna(df["gelir"].median())

print("\nDoldurma sonrası eksik değer sayıları:")
print(df.isnull().sum())


# ---------------------------------------------------------------------------
# 7) Basit öznitelik üretimi
#    (One-Hot Encoding'den önce yaptık ki 'sehir' gibi orijinal
#    sütunlar üzerinden mantıklı öznitelikler üretebilelim.)
# ---------------------------------------------------------------------------
bolum_yazdir(7, "ÖZNİTELİK ÜRETİMİ")

df["destek_talebi_var_mi"] = np.where(df["destek_talebi_sayisi"] > 0, 1, 0)

# gelir_grubu: geliri düşük/orta/yüksek olarak gruplayan basit bir öznitelik
def gelir_grubunu_belirle(gelir):
    if gelir < 10000:
        return "dusuk"
    elif gelir < 25000:
        return "orta"
    else:
        return "yuksek"


df["gelir_grubu"] = df["gelir"].apply(gelir_grubunu_belirle)

print("Yeni sütunlar eklendi: destek_talebi_var_mi, gelir_grubu\n")
print(df[["gelir", "gelir_grubu", "destek_talebi_sayisi", "destek_talebi_var_mi"]].head())


# ---------------------------------------------------------------------------
# 5) Kategorik değişkenleri One-Hot Encoding ile sayısal forma dönüştürme
# ---------------------------------------------------------------------------
bolum_yazdir(5, "ONE-HOT ENCODING")

kategorik_sutunlar = ["sehir", "uyelik_tipi", "gelir_grubu"]
df_encoded = pd.get_dummies(df, columns = kategorik_sutunlar, drop_first = True)

print(f"Encoding sonrası sütun sayısı: {df_encoded.shape[1]}")
print("Yeni sütunlar:", list(df_encoded.columns))


# ---------------------------------------------------------------------------
# 8) Train - Validation - Test bölme
# ---------------------------------------------------------------------------
bolum_yazdir(8, "TRAIN - VALIDATION - TEST BÖLME")

X = df_encoded.drop(columns = ["churn"])
y = df_encoded["churn"]

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size = 0.4, random_state = 42, stratify = y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size = 0.5, random_state = 42, stratify = y_temp
)

print(f"Train boyutu: {X_train.shape[0]}")
print(f"Validation boyutu: {X_val.shape[0]}")
print(f"Test boyutu: {X_test.shape[0]}")


# ---------------------------------------------------------------------------
# 6) Sayısal değişkenlerde ölçekleme
#    (Veri sızıntısını önlemek için scaler sadece train
#    verisiyle fit edilir, sonra val/test verisine uygulanır.)
# ---------------------------------------------------------------------------
bolum_yazdir(6, "ÖLÇEKLEME")

sayisal_sutunlar = ["yas", "gelir", "abonelik_suresi", "destek_talebi_sayisi"]

scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_val_scaled = X_val.copy()
X_test_scaled = X_test.copy()

X_train_scaled[sayisal_sutunlar] = scaler.fit_transform(X_train[sayisal_sutunlar])
X_val_scaled[sayisal_sutunlar] = scaler.transform(X_val[sayisal_sutunlar])
X_test_scaled[sayisal_sutunlar] = scaler.transform(X_test[sayisal_sutunlar])

print("Sayısal sütunlar ölçeklendi:", sayisal_sutunlar)


# ---------------------------------------------------------------------------
# 9) En az 2 model eğitimi: Logistic Regression ve KNN
# ---------------------------------------------------------------------------
bolum_yazdir(9, "MODEL EĞİTİMİ")

log_reg = LogisticRegression(random_state = 42)
log_reg.fit(X_train_scaled, y_train)

knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(X_train_scaled, y_train)

print("Logistic Regression ve KNN modelleri eğitildi.")


# ---------------------------------------------------------------------------
# 10) Validation sonuçlarına göre modelleri karşılaştırma
# ---------------------------------------------------------------------------
bolum_yazdir(10, "VALIDATION KARŞILAŞTIRMASI")

modeller = {
    "Logistic Regression": log_reg,
    "KNN": knn,
}

val_sonuclari = {}
for isim, model in modeller.items():
    tahmin = model.predict(X_val_scaled)
    acc = accuracy_score(y_val, tahmin)
    val_sonuclari[isim] = acc
    print(f"{isim} -> Validation Accuracy: {acc:.3f}")

# En iyi modeli validation accuracy'sine göre seçiyoruz
en_iyi_model_adi = max(val_sonuclari, key=val_sonuclari.get)
en_iyi_model = modeller[en_iyi_model_adi]
print(f"\nValidation sonuçlarına göre seçilen model: {en_iyi_model_adi}")


# ---------------------------------------------------------------------------
# 11) Test seti üzerinde değerlendirme
# ---------------------------------------------------------------------------
bolum_yazdir(11, "TEST SETİ DEĞERLENDİRMESİ")

test_tahmin = en_iyi_model.predict(X_test_scaled)

test_accuracy = accuracy_score(y_test, test_tahmin)
test_cm = confusion_matrix(y_test, test_tahmin)
test_rapor = classification_report(y_test, test_tahmin)

print(f"Seçilen model: {en_iyi_model_adi}")
print(f"Test Accuracy: {test_accuracy:.3f}")
print("\nConfusion Matrix:")
print(test_cm)
print("\nSınıflandırma Raporu (Precision, Recall, F1-score):")
print(test_rapor)


# ---------------------------------------------------------------------------
# 12) Kısa yorum
# ---------------------------------------------------------------------------
bolum_yazdir(12, "SONUÇ YORUMU")

diger_model_adi = [isim for isim in modeller if isim != en_iyi_model_adi][0]

if en_iyi_model_adi == "Logistic Regression":
    sebep_aciklamasi = (
        "Logistic Regression modelinin daha başarılı olmasının sebebi,\n"
        "veri setindeki ilişkilerin doğrusala yakın olması ve bu tür basit,\n"
        "ayrılabilir yapılarda Logistic Regression'ın genelde KNN'e göre\n"
        "daha kararlı sonuçlar vermesi olabilir. KNN'in performansı ise\n"
        "komşu sayısı (k) ve ölçekleme gibi parametrelere daha duyarlıdır."
    )
else:
    sebep_aciklamasi = (
        "KNN modelinin daha başarılı olmasının sebebi, veri setindeki\n"
        "sınıflar arası ilişkinin tamamen doğrusal olmaması ve KNN'in\n"
        "komşuluk tabanlı yapısı sayesinde bu tür doğrusal olmayan\n"
        "örüntüleri Logistic Regression'a göre daha iyi yakalayabilmesi\n"
        "olabilir. Öte yandan KNN'in sonuçları k değeri ve ölçekleme gibi\n"
        "parametrelere daha duyarlıdır."
    )

print(
    f"Validation aşamasında {en_iyi_model_adi}, {diger_model_adi} modeline göre\n"
    f"daha yüksek accuracy elde etmiştir (Validation Accuracy: {val_sonuclari[en_iyi_model_adi]:.3f} vs {val_sonuclari[diger_model_adi]:.3f}).\n"
    f"Bu nedenle test değerlendirmesi için {en_iyi_model_adi} seçilmiştir.\n\n"
    f"{sebep_aciklamasi}"
)
