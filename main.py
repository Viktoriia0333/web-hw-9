from mongoengine import connect
from models import Author, Quote

connect(
    db="quotes_db",
    host="mongodb+srv://v9bondarenko:password@quotesproject.mcddql9.mongodb.net/?retryWrites=true&w=majority&appName=QuotesProject",  # Заміни на свій URI
)


def search_by_author(name):
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        for q in quotes:
            print(q.quote.encode('utf-8').decode())
    else:
        print("Автор не знайдений.")


def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    for q in quotes:
        print(q.quote.encode('utf-8').decode('utf-8'))


def search_by_tags(tags):
    tag_list = tags.split(",")
    quotes = Quote.objects(tags__in=tag_list)
    for q in quotes:
        print(q.quote.encode('utf-8').decode('utf-8'))


if __name__ == '__main__':
    print("Введіть команду у форматі name: ім'я або tag: тег або tags: тег1,тег2. Введіть 'exit' для виходу.")

    while True:
        command = input("Введіть команду: ").strip()
        if command == "exit":
            break
        if command.startswith("name:"):
            name = command[5:].strip()
            search_by_author(name)
        elif command.startswith("tag:"):
            tag = command[4:].strip()
            search_by_tag(tag)
        elif command.startswith("tags:"):
            tags = command[5:].strip()
            search_by_tags(tags)
        else:
            print("Невідома команда. Спробуйте ще раз.")