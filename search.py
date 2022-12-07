from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_recipes')
def search_recipes():
    search_input = request.form['search_input']
    tag = request.form['tag']
    stars = request.form['stars']

    cursor = conn.cursor();
    query = 'Select recipeID, title FROM \
            Recipe NATURAL JOIN RecipeTag NATURAL JOIN Review \
            WHERE title like %\%s% \
            and tagText = %s \
            and stars=stars' 
    
    cursor.execute(query, (search_input, tagText, stars))
    results = cursor.fetchall()
    cursor.close()
    return render_template('search.html', results=results)

