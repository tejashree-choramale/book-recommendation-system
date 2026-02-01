from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load our saved data
pt = pickle.load(open('data/pt.pkl', 'rb'))
books = pickle.load(open('data/books.pkl', 'rb'))

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
        recommendations = ["Book A", "Book B", "Book C"]

    return render_template(
        'book.html',
        book_name=book_name,
        exists=exists,
        recommendations=recommendations
    )


if __name__ == '__main__':
    app.run(debug=True)