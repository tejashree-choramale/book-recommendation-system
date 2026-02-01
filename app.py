from flask import Flask, render_template, request
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load our saved data
pt = pickle.load(open('data/pt.pkl', 'rb'))
books = pickle.load(open('data/books.pkl', 'rb'))

similarity = cosine_similarity(pt)

@app.route('/')
def index():
# 10 books to show on index page
    return render_template('index.html', 
                           book_name = list(books['Book-Title'].values[:10]),
                           image = list(books['Image-URL-L'].values[:10]))

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

    if exists:
        recommendations = get_recommendations(book_name)

    return render_template(
        'book.html',
        book_name=book_name,
        exists=exists,
        recommendations=recommendations
    )


def get_recommendations(book_name):
    book_index = pt.index.get_loc(book_name)

    scores = list(enumerate(similarity[book_index]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommended_books = []
    for i in scores[1:6]:  # to skip the same book we clicked
        recommended_books.append(pt.index[i[0]])

    return recommended_books


if __name__ == '__main__':
    app.run(debug=True)