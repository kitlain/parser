import requests
from bs4 import BeautifulSoup

def extract_href(url, number, page_number):
    if number == 0:
        return []

    hrefs = []
    current_page = 1

    if page_number is None:
        page_number = 1

    while len(hrefs) < number and current_page <= page_number:
        page_url = f"{url}?page={current_page}" if current_page > 1 else url
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        divs = soup.find_all('div', class_='css-1sw7q4x')

        for div in divs:
            inner_div = div.find('div', class_='css-qfzx1y')
            if not inner_div:
                continue

            link = div.find('a')
            if link and 'href' in link.attrs:
                href = link['href']
                if href not in hrefs:
                    hrefs.append(href)

                if len(hrefs) == number:
                    break

        current_page += 1

    return hrefs

def find_number_in_last_li_tag(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    div_element = soup.find('div', {'data-testid': 'pagination-wrapper', 'data-cy': 'pagination', 'class': 'css-4mw0p4'})
    if div_element:
        ul_element = div_element.find('ul', {'class': 'pagination-list', 'data-testid': 'pagination-list'})
        if ul_element:
            last_li_element = ul_element.find_all('li')[-1]
            if last_li_element:
                text = last_li_element.text.strip()
                number = int(''.join(filter(str.isdigit, text)))
                return number
    return None

def extract_number_from_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    div_element = soup.find('div', {'data-testid': 'total-count'})
    if div_element:
        text = div_element.text
        number = ''.join(filter(str.isdigit, text))
        return int(number)
    else:
        return None

def generate_service_link(base_url, input_string):
    input_string = input_string.strip()
    processed_string = input_string.replace(' ', '-')
    link = f"{base_url}{processed_string}/"
    return link

with open('searсh.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

base_urls = [
    "https://www.olx.kz/uslugi/avto-uslugi/q-",
    "https://www.olx.kz/uslugi/dlya-biznesa/q-",
    "https://www.olx.kz/uslugi/remont-i-stroitelstvo/q-",
    "https://www.olx.kz/uslugi/prochie-uslugi/q-",
    "https://www.olx.kz/uslugi/prokat-tovarov/q-"
]

with open("links.txt", "a") as links_file:
    for i in range(len(lines)):
        line = str(lines[i]).strip()
        links_file.write(line + "\n")

        for base_url in base_urls:
            link = generate_service_link(base_url, line)
            print(link)
            count = extract_number_from_link(link)
            page_number = find_number_in_last_li_tag(link)
            result_hrefs = extract_href(link, count, page_number)
            for href in result_hrefs:
                links_file.write(href + "\n")
