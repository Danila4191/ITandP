import pandas as pd
import hashlib
import re
from cryptography.fernet import Fernet

file_path = './csv/Laptop_price.csv'
error_loading = "Ошибка загрузки файла"
security_err_CSV_injection = "Обнаружены потенциальные CSV-инъекции в столбце"
security_ok = "столбец безопасен"
sql_keywords_kit = ["SELECT","DROP","DELETE","INSERT","UPDATE","ALTER","UNION"]
file_filet = 'Фильтрация данных завершена'
file_hash = 'Столбец с хешированными ценами добавлен'
file_crypt = 'Столбец с зашифрованными ценами добавлен'
file_save = 'Обработанный файл сохранен'

try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"{error_loading} : {e}")

def check_csv_injection(df):
    dangerous_chars = ('=','+','-','@',' =', ' +', ' -', ' @', '#', ' #')
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].astype(str).apply(lambda x: x.startswith(dangerous_chars)).any() :
            print(f"{security_err_CSV_injection} {col}!")
        elif     df[col].astype(str).apply(lambda x: x.count(' ') >= 2).any() :
             print(f"{security_err_CSV_injection} {col}!")
        else: 
            print(f"{col} {security_ok}")

check_csv_injection(df)



def clean_input(value):
    sql_keywords = sql_keywords_kit
    xss_patterns = [r'<script.*?>.*?</script>',r'javascript:.*',r'onerror=.*']
    for keyword in sql_keywords:
        if keyword.lower() in value.lower():
            return "[BLOCKED]"
        return value
df = df.applymap(lambda x:clean_input(str(x)) if isinstance(x,str) else x)
print(file_filet)


def hash_price(price):
    return hashlib.sha256(str(price).encode()).hexdigest()
df['Price_Hashed'] = df['Price'].apply(hash_price)
print(file_hash)

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_price(price):
    return cipher.encrypt(str(price).encode()).decode()

def decrypt_price(encrypted_price):
    return  cipher.decrypt(encrypted_price).decode()

df['Price_Encrypted'] = df['Price'].apply(encrypt_price)
print('5 расшифрованных значений столбца Price_Encrypted ')
print(df['Price_Encrypted'].apply(decrypt_price).head(5))
print(file_crypt)
output_path = './csv/Laptop_price_secured.csv'
df.to_csv(output_path,index=False)
print("{file_save}: {output_path}")