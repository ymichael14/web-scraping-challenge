# import necessary libraries
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    movie_list=['Infinity War', 'The Replacements','Gone Girl', 'X-Men: Days of Future Past','Bad Boys 2']
    return render_template('index.html', movie_list=movie_list)


if __name__ == "__main__":
    app.run(debug=True)
