# Launch with
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys


app = Flask(__name__)


@app.route("/")
def articles():
    """Show a list of article titles"""
    return render_template('articles.html', result=all_file)


@app.route("/article/<topic>/<filename>")
def article(topic, filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    for article in articles_res:
        if article[0].endswith(topic + '/' + filename):
            title = article[1]
            contents = article[2]
            recom = recommended(article, articles_res, 5)
            recom_file = []
            for a in recom:
                recom_link = a[0].replace(articles_dirname, '/article')
                recom_file.append((recom_link, a[1]))
            return render_template('article.html', result=(title, contents, recom_file))
    return None


if __name__ == '__main__':
    i = sys.argv.index('server:app')
    glove_filename = sys.argv[i+1]
    articles_dirname = sys.argv[i+2]

    gloves = load_glove(glove_filename)
    articles_res = load_articles(articles_dirname, gloves)

    all_file = []
    for article in articles_res:
        link = article[0].replace(articles_dirname, '/article')
        all_file.append((link, article[1]))

# EX
# gunicorn -D --threads 1 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app ~/data/glove.6B.50d.txt ~/data/bbc
# ps aux | grep gunicorn
# kill -9 9042