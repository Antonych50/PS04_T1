import requests
from bs4 import BeautifulSoup

# Базовый URL для русской Википедии
BASE_URL = "https://ru.wikipedia.org"

def get_wikipedia_page(title):
    url = f"{BASE_URL}/wiki/{title}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1', {'id': 'firstHeading'}).text
    paragraphs = [p.text for p in soup.find_all('p')]
    links = [a.get('href') for a in soup.find_all('a', href=True) if a['href'].startswith('/wiki/')]
    return title, paragraphs, links

def display_paragraphs(paragraphs):
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip():
            print(f"{i + 1}. {paragraph}")
            input("Нажмите 'Enter' для продолжения...")

def display_links(links):
    unique_links = list(set(links))  # Убираем дубликаты
    for i, link in enumerate(unique_links[:10]):  # Ограничим вывод 10 ссылками
        print(f"{i + 1}. {link.split('/wiki/')[-1]}")
    choice = int(input("Выберите номер статьи для перехода (или 0 для отмены): "))
    if choice == 0:
        return None
    return unique_links[choice - 1]

def main():
    query = input("Введите ваш запрос для поиска на Википедии: ")
    html = get_wikipedia_page(query)

    if not html:
        print("Страница не найдена. Попробуйте другой запрос.")
        return

    current_title, current_paragraphs, current_links = parse_page(html)

    while True:
        print(f"\nТекущая статья: {current_title}")
        print("Выберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")

        choice = input("Ваш выбор: ")

        if choice == '1':
            display_paragraphs(current_paragraphs)
        elif choice == '2':
            selected_link = display_links(current_links)
            if selected_link:
                html = get_wikipedia_page(selected_link.split('/wiki/')[-1])
                if html:
                    current_title, current_paragraphs, current_links = parse_page(html)
                else:
                    print("Страница не найдена.")
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()