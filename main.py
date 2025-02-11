import wikipediaapi

def get_wikipedia_page(title):
    wiki_wiki = wikipediaapi.Wikipedia('ru')  # Указываем язык (русский)
    page = wiki_wiki.page(title)
    return page

def display_paragraphs(page):
    if not page.exists():
        print("Страница не найдена.")
        return

    paragraphs = page.text.split('\n')
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip():
            print(f"{i + 1}. {paragraph}")
            input("Нажмите Enter для продолжения...")

def display_links(page):
    links = page.links
    for i, (title, link_page) in enumerate(links.items()):
        print(f"{i + 1}. {title}")
        if i >= 9:  # Ограничим вывод 10 ссылками для удобства
            break

    choice = int(input("Выберите номер статьи для перехода (или 0 для отмены): "))
    if choice == 0:
        return None
    return list(links.keys())[choice - 1]

def main():
    query = input("Введите ваш запрос для поиска на Википедии: ")
    current_page = get_wikipedia_page(query)

    while True:
        if not current_page.exists():
            print("Страница не найдена. Попробуйте другой запрос.")
            break

        print(f"\nТекущая статья: {current_page.title}")
        print("Выберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")

        choice = input("Ваш выбор: ")

        if choice == '1':
            display_paragraphs(current_page)
        elif choice == '2':
            selected_title = display_links(current_page)
            if selected_title:
                current_page = get_wikipedia_page(selected_title)
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()