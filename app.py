from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load our saved data
pt = pickle.load(open('data/pt.pkl', 'rb'))
books = pickle.load(open('data/books.pkl', 'rb'))

@app.route('/')
def index():
    # This is for your "Top Picks" landing page
    # Just show the first 50 books from the master list for now
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

    # Use the BIG master list for searching so we don't miss anything!
    search_result = books[books['Book-Title'].str.contains(user_input, case=False , na=False)].head(10) #using head to get top 10 results and NA to handle NA values
    
    search_result = search_result[['Book-Title','Book-Author','Image-URL-L', 'Year-Of-Publication', 'Publisher']].to_dict('records')


    return render_template('search.html', results=search_result , query=user_input) # sending query back to print it on ui

if __name__ == '__main__':
    app.run(debug=True)