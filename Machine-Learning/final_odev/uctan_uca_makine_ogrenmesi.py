r"""
Makine Öğrenmesi Final Ödevi - Uçtan Uca Sınıflandırma Projesi

[SORU 1]
Amaç:
    Göğüs kanseri (breast cancer) veri seti üzerinde bir hastalığın iyi huylu
    (benign) mu yoksa kötü huylu (malignant) mu olduğunu tahmin eden
    uçtan uca bir makine öğrenmesi projesi geliştirmek. Veri inceleme,
    veri ön işleme, öznitelik mühendisliği, model eğitimi, model karşılaştırma,
    hiperparametre ayarlama ve sonuç yorumlama adımları uygulanmıştır.

Kullanılan kütüphaneler:
    pandas, numpy, matplotlib, seaborn, scikit-learn

Veri Seti:
    scikit-learn içinde hazır bulunan "Breast Cancer Wisconsin" veri seti
    kullanılmıştır (569 satır, 30 sayısal öznitelik).
    Hedef değişken; hücre örneğinin kötü huylu (0) ya da iyi huylu (1)
    olduğunu belirtir.
    Problem türü: İkili sınıflandırma (binary classification)

Çalıştırma adımları:
    1. Sanal ortam oluşturun ve aktif edin (opsiyonel):
        python -m venv venv
        venv\Scripts\activate     # Windows
        source venv/bin/activate  # Linux/Mac
    2. Gerekli kütüphaneleri yükleyin: pip install -r requirements.txt
    3. Python dosyasını çalıştırın: python uctan_uca_makine_ogrenmesi.py

"""

# ---------------------------------------------------------------------------
# Gerekli kütüphanelerin içeriye aktarılması
# ---------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

print("[SORU 1] Docstring projenin amacını, kütüphaneleri ve çalıştırma adımlarını içerir (dosyanın başına bakınız).")

# ---------------------------------------------------------------------------
# [SORU 2] Veri setinin pandas ile okunması ve problemin açıklanması
# ---------------------------------------------------------------------------
print("\n[SORU 2] Veri setinin okunması ve problem açıklaması")

veri = load_breast_cancer()
df = pd.DataFrame(data = veri.data, columns = veri.feature_names)
df["target"] = veri.target  # 0: kötü huylu (malignant), 1: iyi huylu (benign)

sinif_isimleri = veri.target_names  # ["malignant", "benign"]

print(
    "Veri seti; hücre çekirdeği ölçümlerinden yola çıkarak bir tümörün "
    "kötü huylu (malignant) mu yoksa iyi huylu (benign) mu olduğunu "
    "sınıflandırma problemini çözmektedir."
)
print(f"Sınıf isimleri: {sinif_isimleri}")

# ---------------------------------------------------------------------------
# [SORU 3] Hedef değişkenin belirlenmesi ve problem türünün açıklanması
# ---------------------------------------------------------------------------
print("\n[SORU 3] Hedef değişken ve problem türü")

hedef_degisken = "target"
print(f"Hedef değişken: '{hedef_degisken}'")
print("Problem türü: Sınıflandırma")

# ---------------------------------------------------------------------------
# [SORU 4] Veri setinin ilk incelenmesi
# ---------------------------------------------------------------------------
print("\n[SORU 4] Veri setinin ilk incelenmesi")

print("Veri setinin ilk 5 satırı:")
print(df.head())

print(f"\nVeri seti boyutu (satır, sütun): {df.shape}")

print("\nVeri tipleri:")
print(df.dtypes)

print("\nTemel istatistikler:")
print(df.describe())

print("\nHedef değişken dağılımı:")
print(df[hedef_degisken].value_counts())

# ---------------------------------------------------------------------------
# [SORU 11] Veriyi train / validation / test kümelerine ayırma
# ---------------------------------------------------------------------------
print("\n[SORU 11] Train / validation / test ayrımı")

X = df.drop(columns = [hedef_degisken])
y = df[hedef_degisken]

X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size = 0.2, random_state = 42, stratify = y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size = 0.25, random_state = 42, stratify = y_train_val
)

print(f"X_train boyutu: {X_train.shape}")
print(f"X_val boyutu: {X_val.shape}")
print(f"X_test boyutu: {X_test.shape}")

# ---------------------------------------------------------------------------
# [SORU 5] Eksik değer kontrolü
# ---------------------------------------------------------------------------
print("\n[SORU 5] Eksik değer kontrolü")

eksik_deger_sayisi = X_train.isnull().sum().sum()
print(f"Toplam eksik değer sayısı: {eksik_deger_sayisi}")

if eksik_deger_sayisi > 0:
    # sayısal sütunları medyan ile doldur
    sayisal_sutunlar = X_train.select_dtypes(include = [np.number]).columns
    train_medyanlar = X_train[sayisal_sutunlar].median()

    X_train = X_train.fillna(train_medyanlar)
    X_val = X_val.fillna(train_medyanlar)
    X_test = X_test.fillna(train_medyanlar)
    print("Eksik değerler medyan ile dolduruldu.")
else:
    print("Veri setinde eksik değer bulunmamaktadır.")

# ---------------------------------------------------------------------------
# [SORU 9] Öznitelik mühendisliği - en az 2 anlamlı öznitelik üretme
# ---------------------------------------------------------------------------
print("\n[SORU 9] Yeni öznitelik üretimi (feature engineering)")

for df_kume in [X_train, X_val, X_test]:
    # 1. öznitelik: oran temelli sayısal öznitelik -> çevre / alan oranı
    df_kume["cevre_alan_orani"] = df_kume["mean perimeter"] / df_kume["mean area"]

    # 2. öznitelik: "mean area" değerine göre kategorik grup öznitelik
    df_kume["boyut_grubu"] = pd.cut(
        df_kume["mean area"],
        bins = [0, 500, 1000, np.inf], # np.inf ile üst sınır sonsuz olarak belirleniyor
        labels = ["kucuk", "orta", "buyuk"],
)

print("Üretilen özniteliklerden X_train için örnek satırlar:")
print(X_train[["mean perimeter", "mean area", "cevre_alan_orani", "boyut_grubu"]].head())

# ---------------------------------------------------------------------------
# [SORU 6] Kategorik değişkenin encoding ile sayısal forma dönüştürülmesi
# ---------------------------------------------------------------------------
print("\n[SORU 6] Kategorik değişken encoding")

X_train = pd.get_dummies(X_train, columns = ["boyut_grubu"], drop_first = True, dtype = int)
X_val = pd.get_dummies(X_val, columns = ["boyut_grubu"], drop_first = True, dtype = int)
X_test = pd.get_dummies(X_test, columns = ["boyut_grubu"], drop_first = True, dtype = int)

print("Encoding sonrası sütunlar:")
print(X_train.columns.tolist())

# ---------------------------------------------------------------------------
# [SORU 7] Aykırı değer incelemesi (IQR yöntemi)
# ---------------------------------------------------------------------------
print("\n[SORU 7] Aykırı değer incelemesi")

incelenecek_sutunlar = ["mean radius", "mean texture", "mean area"]

# copy() ile orijinal veri setlerini koruyoruz, çünkü aykırı değer sınırlandırması sonrası
# veri seti boyutu değişmeyecek, sadece aykırı değerler sınırlandırılacak
X_train = X_train.copy()
X_val = X_val.copy()
X_test = X_test.copy()

for sutun in incelenecek_sutunlar:
    q1 = X_train[sutun].quantile(0.25)
    q3 = X_train[sutun].quantile(0.75)
    iqr = q3 - q1

    alt_sinir = q1 - 1.5 * iqr
    ust_sinir = q3 + 1.5 * iqr

    aykiri_sayisi = ((X_train[sutun] < alt_sinir) | (X_train[sutun] > ust_sinir)).sum()

    print(f"'{sutun}' sütunundaki aykırı değer sayısı: {aykiri_sayisi}")

    X_train[sutun] = X_train[sutun].clip(lower = alt_sinir, upper = ust_sinir)
    X_val[sutun] = X_val[sutun].clip(lower = alt_sinir, upper = ust_sinir)
    X_test[sutun] = X_test[sutun].clip(lower = alt_sinir, upper = ust_sinir)

print(f"Aykırı değer sınırlandırması sonrası veri seti boyutu: {X_train.shape}")
print("Aykırı değerler Train sınırlarına göre başarıyla sınırlandırıldı.")

# ---------------------------------------------------------------------------
# [SORU 10] Öznitelik seçimi (korelasyon analizi)
# ---------------------------------------------------------------------------
print("\n[SORU 10] Öznitelik seçimi (korelasyon analizi)")

train_df = X_train.copy()
train_df[hedef_degisken] = y_train

korelasyonlar = train_df.corr(numeric_only = True)[hedef_degisken].drop(hedef_degisken).sort_values(ascending=False)
print("Hedef değişken ile en yüksek mutlak korelasyona sahip 10 öznitelik:")
print(korelasyonlar.abs().sort_values(ascending = False).head(10))

# mutlak korelasyonu 0.25'ten büyük olan öznitelikleri seçiyoruz
secilen_ozniteliler = korelasyonlar[abs(korelasyonlar) > 0.25].index.tolist()

# SORU 9'da türettiğimiz özniteliklerin modelde kalmasını garanti altına alıyoruz
uretilen_oznitelikler = ["cevre_alan_orani", "boyut_grubu_orta", "boyut_grubu_buyuk"]
for uretilen in uretilen_oznitelikler:
    if uretilen in X_train.columns and uretilen not in secilen_ozniteliler:
        secilen_ozniteliler.append(uretilen)

print(f"Seçilen öznitelik sayısı: {len(secilen_ozniteliler)}")

# Seçilen öznitelikleri tüm kümelere uyguluyoruz
X_train = X_train[secilen_ozniteliler]
X_val = X_val[secilen_ozniteliler]
X_test = X_test[secilen_ozniteliler]

# ---------------------------------------------------------------------------
# [SORU 8] Sayısal özelliklerde ölçekleme
# ---------------------------------------------------------------------------
print("\n[SORU 8] Sayısal özelliklerin ölçeklenmesi (standardization)")

scaler = StandardScaler()

# ölçekleyiciyi yalnızca eğitim verisi üzerinde öğretiyoruz
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print("Ölçekleme tamamlandı (fit yalnızca train verisinde yapıldı, val/test'e transform uygulandı).")

# ---------------------------------------------------------------------------
# [SORU 12] En az 3 farklı modelin eğitilmesi
# ---------------------------------------------------------------------------
print("\n[SORU 12] Modellerin eğitilmesi")

modeller = {
    "Logistic Regression": LogisticRegression(max_iter = 1000, random_state = 42),
    "KNN": KNeighborsClassifier(n_neighbors = 5),
    "Random Forest": RandomForestClassifier(n_estimators = 100, random_state = 42),
}

validation_sonuclari = []

for model_adi, model in modeller.items():
    model.fit(X_train_scaled, y_train)
    y_val_pred = model.predict(X_val_scaled)

    val_accuracy = accuracy_score(y_val, y_val_pred)
    val_f1 = f1_score(y_val, y_val_pred)

    validation_sonuclari.append(
        {"model": model_adi, "val_accuracy": val_accuracy, "val_f1": val_f1}
    )
    print(f"{model_adi} eğitildi.")

# ---------------------------------------------------------------------------
# [SORU 13] Validation sonuçlarına göre modellerin karşılaştırılması
# ---------------------------------------------------------------------------
print("\n[SORU 13] Validation küme performans karşılaştırması")

validation_df = pd.DataFrame(validation_sonuclari).sort_values(
    by = "val_f1", ascending = False
)

print(validation_df)

en_iyi_model_adi = validation_df.iloc[0]["model"]
print(f"Validation kümesinde en iyi performansı gösteren model: {en_iyi_model_adi}")

# ---------------------------------------------------------------------------
# [SORU 14] Seçilen en iyi model için hiperparametre ayarlama
# ---------------------------------------------------------------------------
print("\n[SORU 14] Hiperparametre ayarlama")

# not: bu bölüm en_iyi_model_adi hangi model olursa olsun çalışacak şekilde yazılmıştır
grid_parametreleri = {
    "Logistic Regression": {
        "C": [0.01, 0.1, 1, 10],
    },
    "KNN": {
        "n_neighbors": [3, 5, 7, 9, 11],
        "metric": ["euclidean", "manhattan"],
    },
    "Random Forest": {
        "n_estimators": [100, 200],
        "max_depth": [3, 5, None],
        "min_samples_split": [2, 4],
    },
}

en_iyi_model_taslak = modeller[en_iyi_model_adi]
secilen_parametreler = grid_parametreleri[en_iyi_model_adi]

grid_search = GridSearchCV(
    estimator = en_iyi_model_taslak,
    param_grid = secilen_parametreler,
    cv = 5,
    scoring = "f1",
    n_jobs = -1,
)

# hiperparametre aramasını train verisi üzerinde yapıyoruz
grid_search.fit(X_train_scaled, y_train)

print(f"{en_iyi_model_adi} için en iyi hiperparametreler: {grid_search.best_params_}")
print(f"En iyi cross-validation f1 skoru: {round(grid_search.best_score_, 3)}")

en_iyi_model = grid_search.best_estimator_

# ---------------------------------------------------------------------------
# [SORU 15] En iyi modelin test verisi üzerinde değerlendirilmesi
# ---------------------------------------------------------------------------
print("\n[SORU 15] Test verisi değerlendirmesi")

y_test_pred = en_iyi_model.predict(X_test_scaled)

test_accuracy = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred)
test_recall = recall_score(y_test, y_test_pred)
test_f1 = f1_score(y_test, y_test_pred)
test_conf_matrix = confusion_matrix(y_test, y_test_pred)

print("--- Test Verisi Sonuçları ---")
print(f"Accuracy : {round(test_accuracy, 3)}")
print(f"Precision: {round(test_precision, 3)}")
print(f"Recall   : {round(test_recall, 3)}")
print(f"F1-score : {round(test_f1, 3)}")
print("\nConfusion Matrix:")
print(test_conf_matrix)

# confusion matrix görselleştirmesi
disp = ConfusionMatrixDisplay(
    confusion_matrix = test_conf_matrix, display_labels = sinif_isimleri
)
disp.plot(cmap = "Blues")
plt.title(f"{en_iyi_model_adi} - Test Verisi Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()
print("\nConfusion matrix görseli 'confusion_matrix.png' olarak kaydedildi.")

# ---------------------------------------------------------------------------
# [SORU 17] Bonus: Basit açıklanabilirlik yorumu (feature importance / katsayılar)
# Not: bu bölüm SORU 16'daki yorumda kullanılacağı için önce hesaplanıyor,
# ama çıktısı yine "SORU 17" başlığı altında yazdırılıyor.
# ---------------------------------------------------------------------------
if hasattr(en_iyi_model, "feature_importances_"):
    onem_dereceleri = pd.Series(
        en_iyi_model.feature_importances_, index = secilen_ozniteliler
    ).sort_values(ascending = False)
    en_onemli_3_ozellik = onem_dereceleri.head(3).index.tolist()
elif hasattr(en_iyi_model, "coef_"):
    onem_dereceleri = pd.Series(
        en_iyi_model.coef_[0], index = secilen_ozniteliler
    ).sort_values(key = abs, ascending = False)
    en_onemli_3_ozellik = onem_dereceleri.head(3).index.tolist()
else:
    onem_dereceleri = None
    en_onemli_3_ozellik = []

# ---------------------------------------------------------------------------
# [SORU 16] Sonuç yorumu
# ---------------------------------------------------------------------------
print("\n[SORU 16] Kısa model yorumu")

# tüm modellerin validation sonuçlarını okunabilir bir metne çeviriyoruz
model_karsilastirma_metni = "\n".join(
    f"- {satir['model']}: val_accuracy={round(satir['val_accuracy'], 3)}, "
    f"val_f1={round(satir['val_f1'], 3)}"
    for _, satir in validation_df.iterrows()
)

onemli_ozellik_metni = (
    ", ".join(en_onemli_3_ozellik) if en_onemli_3_ozellik else "belirlenemedi"
)

print(
    f"""--- Kısa Model Yorumu ---
Validation kümesinde 3 model şu şekilde karşılaştırılmıştır:
{model_karsilastirma_metni}

Bu karşılaştırmada en iyi F1 skorunu '{en_iyi_model_adi}' modeli vermiştir. 
Bu model, hiperparametre ayarlamasından sonra test verisinde {round(test_accuracy, 3)} accuracy, {round(test_precision, 3)} precision, 
{round(test_recall, 3)} recall ve {round(test_f1, 3)} F1-score elde etmiştir. Bu problemde recall metriği ayrıca önemlidir; 
çünkü kötü huylu (malignant) bir vakayı iyi huylu olarak sınıflandırmak (yanlış negatif), tam tersi hataya göre çok daha risklidir.

Öznitelik seçiminde korelasyon analizi kullanılmış, hedef değişken ile ilişkisi
zayıf olan öznitelikler (mutlak korelasyon <= 0.25) elenmiştir. 
Modelin tahmin kararında en etkili görünen öznitelikler: {onemli_ozellik_metni}.

Modelin sınırlılıkları:
- Veri seti görece küçük olduğu için (569 satır) sonuçlar farklı bir
  train/test bölünmesinde değişkenlik gösterebilir.
- Hiperparametre arama uzayı, çalışma süresini kısa tutmak amacıyla
  sınırlı tutulmuştur; daha geniş bir arama ile sonuçlar biraz daha
  iyileştirilebilir.
- Öznitelik seçiminde yalnızca doğrusal korelasyon dikkate alınmıştır;
  doğrusal olmayan ilişkiler bu seçimde gözden kaçmış olabilir.
"""
)

# ---------------------------------------------------------------------------
# [SORU 17] Öznitelik önem dereceleri (açıklanabilirlik) - detaylı çıktı
# ---------------------------------------------------------------------------
print("[SORU 17] Bonus: Öznitelik önem dereceleri (açıklanabilirlik)")

if onem_dereceleri is not None:
    if hasattr(en_iyi_model, "feature_importances_"):
        print("Random Forest feature importance (ilk 10):")
        print(onem_dereceleri.head(10))
    else:
        print("Logistic Regression katsayıları, mutlak değere göre sıralı (ilk 10):")
        print(onem_dereceleri.head(10))
else:
    print("Bu model için doğrudan bir önem derecesi/katsayı çıktısı bulunmuyor.")