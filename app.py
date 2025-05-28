from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load artifacts
pt = pickle.load(open('artifacts/pt.pkl', 'rb'))
books = pickle.load(open('artifacts/books.pkl', 'rb'))
similarity_scores = pickle.load(open('artifacts/similarity_scores.pkl', 'rb'))

def recommend(book_name):
    # index fetch
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        try:
            recommendations = recommend(book_name)
        except:
            recommendations = [["Book not found. Please check the title.", "", ""]]
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
