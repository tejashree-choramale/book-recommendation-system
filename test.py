print("hello world")
import pandas as pd
import pickle

#pt = pickle.load(open('data/pt.pkl', 'rb'))
books = pickle.load(open('data/books.pkl', 'rb'))

#print(pt.head())
#print(books)

#print(books.count())

#no_duplicates = books.drop_duplicates()

#print(no_duplicates.count())

books = books.drop(columns = ["Image-URL-S", "Image-URL-M", "Publisher", "Image-URL-L"])

books["Book-Title"] = books["Book-Title"].str.lower()

books["Book-Author"] = books["Book-Author"].str.lower()

print(books.head())

#books_by_title = books.set_index("Book-Title")
#print(books_by_title.loc["classical mythology"])

#book_name = input("Enter the Book Name: ").lower()

#result = books[books["Book-Title"].str.contains(book_name, case=False, na=False)]

#if result.empty:
#    print(f"{book_name} NOT FOUND")
#else:
#    print(result)

new_books = books[books["Year-Of-Publication"] < 2000]
print(new_books)