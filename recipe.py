from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/post_recipe')
def post_recipe():
    return render_template('create_recipe.html')


@app.route('/create_recipe')
def create_recipe():
    username = session['username']
    # cursor = conn.cursor();
    # query = 'SELECT * FROM Recipe where postedBy = %s'
    # cursor.execute(query, username)
    # recipes = cursor.fetchall()
    # cursor.close()
    return render_template('create_recipe.html')

#Authenticates the register
@app.route('/createRecipe', methods=['GET', 'POST'])
def createRecipe():
    username = session['username']
    #grabs information from the forms
    title = request.form['title']
    numServings = request.form['numServings']
    dietRestr = request.form['dietaryRestrictions']
    recipeTags = request.form['recipeTags']
    ingredients = request.form['ingredients']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Recipe WHERE title = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        # if recipe with same title exists in DB, stop them from creating the recipe.
        error = "This recipe already exists"
        return render_template('create_recipe.html', error = error)
    else:
        # query to get the username
        query = 'SELECT'
        ins = 'INSERT INTO Recipe (title, numServings, postedBy) VALUES (%s, %s, %s)'
        cursor.execute(ins, (title, numServings, username))
        conn.commit()
        cursor.close()
        return render_template('create_recipe.html')
    
    
# @app.route('/recipe-info')
# def create_recipe():
#     username = session['username']
#     # cursor = conn.cursor();
#     # query = 'SELECT * FROM Recipe where postedBy = %s'
#     # cursor.execute(query, username)
#     # recipes = cursor.fetchall()
#     # cursor.close()
#     return render_template('create_recipe.html')
