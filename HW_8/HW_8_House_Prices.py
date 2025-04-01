import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

train = pd.read_csv(r"c:\Users\Саша - Лютый\Desktop\DataEng\HW_8\train.csv")
test = pd.read_csv(r"c:\Users\Саша - Лютый\Desktop\DataEng\HW_8\test.csv")
submission = pd.read_csv(r"c:\Users\Саша - Лютый\Desktop\DataEng\HW_8\sample_submission.csv")

train['DataType'] = 'train'
test['DataType'] = 'test'


df = pd.concat([train, test], axis=0, ignore_index=True)
print("Исходный датасет:")
print(df.head())  


print("\nОбщая информация о датасете:")
print(df.info())  
print("\nСтатистика по числовым столбцам:")
print(df.describe(include=["number"]))  

missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0].sort_values(ascending=False)
print("\nПропущенные значения:")
print(missing_values)  

for col in missing_values.index:
    if df[col].dtype == "object":
        df[col].fillna(df[col].mode()[0], inplace=True)  
    else:
        df[col].fillna(df[col].median(), inplace=True)  


df.drop_duplicates(inplace=True)

categorical_cols = df.select_dtypes(include=["object"]).columns
for col in categorical_cols:
    df[col] = df[col].astype("category")

# Разведочный анализ данных (EDA)

plt.figure(figsize=(10, 6))
sns.histplot(df["SalePrice"], bins=30, kde=True)
plt.title("Распределение SalePrice")
plt.xlabel("Цена продажи")
plt.ylabel("Частота")
plt.show()

numerical_cols = df.select_dtypes(include=["number"]).columns  
corr = df[numerical_cols].corr() 

sale_price_corr = corr["SalePrice"].sort_values(ascending=False)
sale_price_corr = sale_price_corr[abs(sale_price_corr) > 0.5]

plt.figure(figsize=(10, 6))
sns.heatmap(sale_price_corr.to_frame(), annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5)
plt.title("Корреляция признаков с 'SalePrice'")
plt.show()

plt.figure(figsize=(14, 10))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5)
plt.title("Корреляционная матрица всех числовых переменных")
plt.show()

df_encoded = pd.get_dummies(df, drop_first=True)

df_encoded.to_csv("cleaned_house_prices.csv", index=False)
print("Данные сохранены в cleaned_house_prices.csv")

print("\nОткрытие нового очищенного CSV файла:")
cleaned_df = pd.read_csv("cleaned_house_prices.csv")

print("\nПервые 5 строк из cleaned_house_prices.csv:")
print(cleaned_df.head())  

pd.set_option('display.max_columns', None)  
pd.set_option('display.max_rows', 10)  