import pandas as pd
import numpy as np


# csv dosyasını oku
df = pd.read_csv("dataset\Superstore.csv",encoding='latin1')

# Tüm satırları ekranda göster
pd.set_option("display.max_columns",None)

# Satır genişliğini arttır
pd.set_option("display_width",200)

###############  VERİ SETİNİ TANIMA ##############
"""
'Row ID': Satır Kimliği
'Order ID': Sipariş Kimliği
'Order Date': Sipariş Tarihi
'Ship Date': Sevkiyat Tarihi 
'Ship Mode':Sevkiyat Modu
'Customer ID': Müşteri Kimlği
'Customer Name': Müşteri Adı
'Segment': Segment
'Country': Ülke
'City' : Şehir
'State': Eyalet
'Postal Code': Posta Kodu
'Region' : Bölge
'Product ID': Ürün ID
'Category': KAtegori
'Sub-Category': Alt Kategori
'Product Name' : Ürün Adı
'Sales': Satışlar
'Quantity': Miktar
'Discount': İndirim
'Profit': Kar
"""
df.head()
df.tail()
df.columns
df.info()
df.shape
df.isnull().sum()
df.describe().T

# Yukarıda ki işlemler için bir fonksiyon oluşturduk.

def check_df(dataframe,head=5):
    print("############################ HEAD ###############################")
    print(dataframe.head())

    print("############################ TAİL ###############################")
    print(dataframe.tail())

    print("############################ SHAPE ###############################")
    print(dataframe.shape)

    print("############################ Columns ###############################")
    print(dataframe.columns)

    print("############################ Null ###############################")
    print(dataframe.isnull().sum())

    print("############################ INFO ###############################")
    print(dataframe.info())

    print("############################ DESCRIBE ###############################")
    print(dataframe.describe().T)

check_df(df)

df["Order Date"].dtype
df["Ship Date"].dtype

# Tarih kolonları object türünde. Bunları datatime'a çevirelim . Böylece uzerınde sayısal işlemler yapabiliriz
for col in ["Order Date","Ship Date"]:
    df[col] = pd.to_datetime(df[col],dayfirst=True)


# Gönderim süresine bakalım ve bunu yeni bir kolon olarak ekleyelim
df["Shipping Duration"] = (df["Ship Date"] - df["Order Date"]).dt.days


        ############## Genel Satış Analizi #############

# Toplam satış ve toplam kar
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
print("Toplam Satış : ", total_sales)
print("Toplam Kar : ", total_profit)

# Ortalama satış ve kar
print("Ortalama Satış : ", df["Sales"].mean())
print("Ortalama Kar : " , df["Profit"].mean())

# Bölgelere göre satış 
region_sales = df.groupby("Region")["Sales"].sum()
region_profit = df.groupby("Region")["Profit"].sum()
print(region_sales)
print(region_profit)

# Kategorilere göre satış
category_sales = df.groupby("Category").agg({"Sales" : "sum"})
category_profit = df.groupby("Category").agg({"Profit":"sum"})
print(category_sales)
print(category_profit)

# Teslim sürelerine göre analiz
print("Ortalama Teslim Süresi  ", df["Shipping Duration"].mean())
print("En hızlı teslimat(gün)" , df["Shipping Duration"].min())
print("En uzun teslimat (gün)", df["Shipping Duration"].max())


# Bölgelere göre ortalama teslim süresi
region_shipping = df.groupby("Region")["Shipping Duration"].mean()
print(region_shipping)


                ################## VERİLERİN GÖRSELLEŞTİRİLMESİ ##################

# *************Teslim sürelerine göre dağılım***************
import matplotlib.pyplot as plt
plt.hist(df["Shipping Duration"] , bins=8 , color="red")
plt.title("Shipping Duration Distribution")
plt.xlabel("Teslim Süresi (gün)")
plt.ylabel("Sipariş Sayısı")
plt.show()


# **************** Kategorik bazlı satışlar (Bar Chart) *********************
# Hangi ürün kategorisi daha çok satmış

category_sales = df.groupby("Category")["Sales"].sum()
# Bar grafiği çiz
bars = plt.bar(category_sales.index, category_sales.values, 
        color=plt.cm.Set2.colors)

plt.title("Kategori Bazlı Satışlar")
plt.ylabel("Toplam Satış")
plt.show()



# Her barın üzerine otomatık değer ekleyerek istenen görsellştirmeyi alabileceiğmiz bir fonksiyon yazdık
def plot_bar_with_labels(data,kind="bar" , title="",xlabel ="",ylabel="",color="skyblue"):
    """
    Bar grafiği çizer ve her barın üzerine değer yazar

    
    data: Series veya DataFrame kolonları gruplanmış veri
    kind: "bar" veya "barh" (dikey veya yatay)
    title: Grafiğin Başlığı
    xlabel: x ekseni etiketi
    ylabel: y ekseni etiketi
    color: Bar renkleri
    """

    ax= data.plot(kind=kind , color= color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Etiketleri ekleme

    max_val = max(data)
    
    if kind == "bar":  # Dikey
        for i, v in enumerate(data):
            if v > 0.1*max_val:  # Bar uzunsa etiketi içine yaz
                ax.text(i, v - 0.02*max_val, f"{v:.2f}", ha='center', va='top', color="black")
            else:  # Bar kısa ise etiketi üstüne yaz
                ax.text(i, v + 0.02*max_val, f"{v:.2f}", ha='center', va='bottom', color="black")
                
    elif kind == "barh":  # Yatay
        for i, v in enumerate(data):
            if v > 0.1*max_val:  # Bar uzunsa etiketi içine yaz
                ax.text(v - 0.02*max_val, i, f"{v:.2f}", va='center', ha='right', color="black")
            else:  # Bar kısa ise etiketi sağında yaz
                ax.text(v + 0.02*max_val, i, f"{v:.2f}", va='center', ha='left', color="black")
    
    plt.show()

# Kategorik bazlı satışları fonksiyon uzerınden hem yatay hem de dikey olarak görselleştırelim
plot_bar_with_labels(category_sales,kind = "barh",title="Kategori Bazlı Satışlar", xlabel="Toplam Satış",ylabel="Kategori") # Yatay
plot_bar_with_labels(category_sales,kind = "bar",title="Kategori Bazlı Satışlar", xlabel="Toplam Satış",ylabel="Kategori" , color= plt.cm.Set3.colors) # Dikey


# ************************ Bölgelere Göre Ortalama Kar Oranları(Horizontal Bar) **********************

# HAngi bölge daha karlı?
region_profit = df.groupby("Region")["Profit"].mean().sort_values()
region_profit.plot(kind="barh",color="seagreen")
plt.title("Bölgelere Göre Ortalama Kâr")
plt.xlabel("Ortalama Kar")
plt.show()

# Fonksiyon yardımıyla aynı sonucu elde edelim.

plot_bar_with_labels(region_profit,kind="barh",color="orange",title="Bölgelere Göre Dağılım",xlabel="Ortalama Kar")


            ######################### İndirim – Kâr İlişkisi (Scatter Plot) ###########################
plt.scatter(df["Discount"],df["Profit"],alpha=0.5,color="purple")
plt.title("İNDİRİM - KÂR İLİŞKİSİ")
plt.xlabel("İndirim")
plt.ylabel("Kâr")
plt.show()


            ############################### Aylara Göre Satışlar (Line Chart) ############################
df["Order Date"]=pd.to_datetime(df["Order Date"],dayfirst=True)

# aynı ay içerisindeki tüm atışları toplar
monthly_sales = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()
monthly_sales.plot(kind="line",marker="o",color="red")
plt.title("Aylık Satış Trendleri")
plt.xlabel("Ay")
plt.ylabel("Toplam Satış")
plt.show()




            ######################### En Çok Satan Ürünler (Top 10) (Bar Chart) #############################
top_products = df.groupby("Product Name")["Sales"].sum().nlargest(10)
top_products.plot(kind="bar" ,color="gold")
plt.title("En Çok Satan 10 Ürün")
plt.ylabel("Toplam Satış")
plt.show()


            ########################### Kategorilere Göre Satış Dağılımı (Pie Chart)###########################
category_sales = df.groupby("Category")["Sales"].sum()

category_sales.plot(
    kind="pie", 
    autopct="%1.1f%%",   # yüzde değerlerini göster
    startangle=90,       # grafiği 90 derece döndürerek başlat
    colors=["gold", "lightblue", "lightgreen"], # 3 kategoriye renkler
    explode=[0.05, 0.05, 0.05] # dilimleri biraz ayır
)

plt.title("Kategoriye Göre Satış Dağılımı")
plt.ylabel("")  # y eksenini gizle (pie için gereksiz)
plt.show()


# Bu grafik türünü tekrar tekrar kullanırken kolaylık sağlaması açısından fonksiyona çevirelim

def plot_pie(dataframe,group_col,value_col,title = "Pie Chart" , colors=None):
    """
    dataframe: pandas DataFrame
    group_col: Gruplama yapılacak kolon (ör: 'Category', 'Segment')
    value_col: Hesaplanacak kolon (ör: 'Sales', 'Profit')
    title: Grafik Başlığı
    colors: İsteğe bağlı renk listesi
    """

    data = dataframe.groupby(group_col)[value_col].sum()

    data.plot(
        kind="pie",
        autopct="%1.1f%%",   # yüzde göster
        startangle=90,       # başlangıç açısı
        colors=colors,       # özel renk listesi (yoksa default)
        explode=[0.05]*len(data) # dilimleri ayırma
    )

    plt.title(title)
    plt.ylabel("")  # y-axis gizle
    plt.show()

# Kategoriye göre satış oranları
plot_pie(df, "Category", "Sales", title="Kategoriye Göre Satış Dağılımı",
         colors=["gold", "lightblue", "lightgreen"])


# Segmente göre kâr oranları
plot_pie(df, "Segment", "Profit", title="Segmentlere Göre Kâr Dağılımı",
         colors=["coral", "skyblue", "lightgreen"])

# Bölgelere göre satış oranları
plot_pie(df, "Region", "Sales", title="Bölgelere Göre Satış Dağılımı")
