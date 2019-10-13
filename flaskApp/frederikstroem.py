from flask import Flask
from flask import render_template, url_for, request, send_from_directory, redirect
import json
import os
from journal import Journal

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
journalHandler = Journal()

# Debug mode active if file exist.
debugMode = os.path.isfile('./_DEBUG_MODE')

# Force HTTPS. Source: https://stackoverflow.com/a/32238093 (2019-05-26)
@app.before_request
def before_request():
    if debugMode:
        pass
    else:
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

@app.route("/")
def home():
    latestPosts = journalHandler.getLatestPosts()[:2]

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

@app.route("/donate/")
def donate():
    donateList = None
    with open("donate.json", "r") as f:
        donateList = json.loads(f.read())
    return render_template('pages/donate.html', donateList=donateList)

# https://stackoverflow.com/a/14054039 (2019-05-10)
@app.route('/robots.txt')
@app.route('/sitemap.xml')
@app.route('/feed.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == "__main__":
    if debugMode:
        app.run(debug=True)
    else:
        app.run(debug=False)
