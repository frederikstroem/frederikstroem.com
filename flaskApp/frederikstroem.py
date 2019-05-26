from flask import Flask
from flask import render_template, url_for, request, send_from_directory, redirect
import json
from journal import Journal

app = Flask(__name__)
journalHandler = Journal()

@app.route("/")
def home():
    latestPosts = journalHandler.getLatestPosts()[-2:]

    return render_template('pages/home.html', latestPosts=latestPosts)

@app.route("/journal/")
def journal():
    return render_template('pages/journal/journal.html', latestPosts=journalHandler.getLatestPosts(), paginationOverview=journalHandler.getPaginationOverview())

@app.route("/journal/<int:page>/")
def journalPage(page):
    return render_template('pages/journal/journal.html', latestPosts=journalHandler.getLatestPosts(page), paginationOverview=journalHandler.getPaginationOverview(page))

@app.route("/journal/<string:postName>/")
def journalPost(postName):
    return render_template('pages/journal/post.html', post=journalHandler.getPost(postName))

@app.route("/projects/")
def projects():
    projectsList = None
    with open("projects.json", "r") as f:
        projectsList = json.loads(f.read())
    return render_template('pages/projects.html', projectsList=projectsList)

@app.route("/curriculum-vitae/")
def curriculumVitae():
    curriculumVitaeList = None
    with open("curriculum-vitae.json", "r") as f:
        curriculumVitaeList = json.loads(f.read())
    workList = curriculumVitaeList["work"]
    educationList = curriculumVitaeList["education"]
    return render_template('pages/curriculum-vitae.html', workList=workList, educationList=educationList)

# https://stackoverflow.com/a/14054039 (2019-05-10)
@app.route('/robots.txt')
@app.route('/sitemap.xml')
@app.route('/feed.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == "__main__":
    app.run(debug=False)
