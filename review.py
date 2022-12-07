from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/review/')
def review():
    # getting args from URL: https://stackoverflow.com/questions/40369016/using-request-args-in-flask-for-a-variable-url
    recipeID = request.args.get('recipeID')
    title = request.args.get('title')
    return render_template('review.html', recipeID=recipeID, title=title)

@app.route('/review_recipe')
def review_recipe():
    user = session['username']
    recipeID = request.form['recipeID']
    rev_title = request.form['rev_title']
    stars = request.form['stars']
    rev_desc = request.form['rev_desc']

    cursor = conn.cursor();
    query = 'INSERT INTO Review (userName, recipeID, revTitle, revDesc, stars) \
            values (%s, %s, %s, %s, %s) '
    cursor.execute(query, (user, recipeID, rev_title, rev_title, rev_desc, stars))
    conn.commit()
    cursor.close()
    return redirect(url_for('dashboard'))