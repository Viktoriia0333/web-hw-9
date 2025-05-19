import json
from mongoengine import connect
from models import Author, Quote

connect(
    db="quotes_db",
    host="mongodb+srv://v9bondarenko:password@quotesproject.mcddql9.mongodb.net/?retryWrites=true&w=majority&appName=QuotesProject",
)


def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
        for author in authors_data:
            if not Author.objects(fullname=author['fullname']).first():
                Author(**author).save()


def load_quotes():
    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
        for q in quotes_data:
            author = Author.objects(fullname=q['author']).first()
            if author:
                Quote(tags=q['tags'], author=author, quote=q['quote']).save()


if __name__ == "__main__":
    load_authors()
    load_quotes()
    print("Дані завантажено успішно.")
