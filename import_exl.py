import requests
from bs4 import BeautifulSoup
import pandas as pd

prefix = "https://www.olx.kz/"

# Создание пустого списка для хранения данных
data = []

with open("links.txt", "r") as file:
    for line in file:
        if "/d/obyavlenie/" in line:
            link_part = line.strip()
            full_link = prefix + link_part
            print(full_link)

            response = requests.get(full_link)
            content = response.text

            soup = BeautifulSoup(content, "html.parser")

            try:
                # Извлечение данных
                title = soup.find("h1", class_="css-1soizd2 er34gjf0").text.strip()
            except AttributeError:
                # Если заголовок не найден, пропустить ссылку
                continue

            name = soup.find("h4", class_="css-1lcz6o7 er34gjf0").text.strip()
            price = soup.find("h3", class_="css-ddweki er34gjf0")
            price = price.text.strip() if price else ""
            description = soup.find("div", class_="css-bgzo2k er34gjf0")
            description = description.get_text(separator="\n").strip() if description else ""
            date = soup.find("span", class_="css-19yf5ek").text.strip()

            # Формирование строки данных
            row = {
                "id": len(data) + 1,
                "название": title,
                "цена": price,
                "имя": name,
                "описание": description,
                "дата публикации": date,
                "ссылка": full_link
            }

            # Добавление строки данных в список
            data.append(row)

# Создание DataFrame из списка данных
df = pd.DataFrame(data)

# Сохранение DataFrame в Excel файл
df.to_excel("output.xlsx", index=False)
