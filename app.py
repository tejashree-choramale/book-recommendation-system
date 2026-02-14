import pandas as pd
from flask import Flask, render_template, request
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import random

app = Flask(__name__)

# Load our saved data
pt = pickle.load(open('data/pt.pkl', 'rb'))
books = pickle.load(open('data/books.pkl', 'rb'))

similarity = cosine_similarity(pt)

# getting top 10 books from dataset
pt_nonzero = pt.replace(0, pd.NA) #replacing 0 with nan

mean_ratings = pt_nonzero.mean(axis=1)

num_ratings = (pt > 0).sum(axis=1) # getting count of how many users rate the book

popularity_df = pd.DataFrame({
    'num_ratings': num_ratings,
    'avg_rating': mean_ratings
})

popularity_df = popularity_df[popularity_df['num_ratings'] >= 10] # rejecting books with less than 10 ratings

popularity_df['score'] = popularity_df['avg_rating'] * popularity_df['num_ratings']

popularity_df = popularity_df.sort_values(by='score', ascending=False) #sorting from more to less

popularity_df = popularity_df.merge(
    books[['Book-Title', 'Book-Author', 'Image-URL-L']],
    left_index=True,
    right_on='Book-Title'
)

popularity_df = popularity_df.drop_duplicates(subset='Book-Title', keep='first') #dropping duplicates

top_10_popular = popularity_df.head(10)


@app.route('/')
def index():
# 10 books to show on index page
    return render_template('index.html', 
                           top_10_popular=top_10_popular.to_dict(orient='records'))

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form.get('user_input', '').strip()

    if not user_input:
        return render_template(
            'search.html',
            results=[],
            query=user_input,
            error="Please enter something to search"
        ) 

    # list of books that contain search results
    search_result = books[books['Book-Title'].str.contains(user_input, case=False , na=False)].head(10) #using head to get top 10 results and NA to handle NA values
    
    search_result = search_result[['Book-Title','Book-Author','Image-URL-L', 'Year-Of-Publication', 'Publisher']].to_dict('records')


    return render_template('search.html', results=search_result , query=user_input) # sending query back to print it on ui

@app.route('/book/<book_name>')
def book_detail(book_name):
    exists = book_name in pt.index

    recommendations = [] #list to get recs
    fallback_books = []

    if exists:
        recommendations = get_recommendations(book_name)

    # Fallback logic if recs are not prsent
    if not recommendations:
        same_author = get_same_author_books(book_name)
        top_books = top_10_popular.to_dict('records')

        fallback_books = same_author + top_books

        # shuffling for random books
        random.shuffle(fallback_books)

        fallback_books = fallback_books[:8]

    return render_template (
        'book.html',
        book_name=book_name,
        exists=exists,
        recommendations=recommendations,
        fallback_books=fallback_books
    )


def get_recommendations(book_name):
    book_index = pt.index.get_loc(book_name)

    scores = list(enumerate(similarity[book_index]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommended_books = []
    for i in scores[1:6]:  # to skip the same book clicked
        book_title = pt.index[i[0]]

        book_data = books[books['Book-Title'] == book_title].iloc[0]

        recommended_books.append({
            'Book-Title': book_data['Book-Title'],
            'Book-Author': book_data['Book-Author'],
            'Image-URL-L': book_data['Image-URL-L']
        })

    return recommended_books

def get_same_author_books(book_name):
    book_row = books[books['Book-Title'] == book_name]

    if book_row.empty:
        return []

    author = book_row.iloc[0]['Book-Author']

    author_books = books[(books['Book-Author'] == author) & (books['Book-Title'] != book_name) ]  #getting books of same author

    author_books = author_books.head(10) # first 10

    return author_books.to_dict('records')


if __name__ == '__main__':
    app.run(debug=True)