from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_recipes', methods=["POST", "GET"])
def search_recipes():
    search_input = request.form['search_input']
    tag = request.form['tag']
    stars = request.form['stars']
    search_filter = request.form['filter']

    order_by_addon = ""
    if search_filter == 'alphabetical':
        group_by_addon = 'order by title'
    else:
        group_by_addon = 'order by avg'

    cursor = conn.cursor();
    if stars == "any":
        # query = 'Select DISTINCT recipeID, title, postedBy FROM \
        #     Recipe NATURAL JOIN RecipeTag \
        #     WHERE title like %s \
        #     and tagText like %s' 

        query = "select distinct recipeID, title, IFNULL(avg(stars), 'N/A') as avg \
                from Recipe NATURAL JOIN RecipeTag natural left JOIN Review \
                WHERE title like %s and tagText like %s \
                group by recipeID, title"
        # query += order_by_addon
        
        print(query)
        search_input = '%{}%'.format(search_input)
        tag = '%{}%'.format(tag)
        cursor.execute(query, (search_input, tag))
    else:
        query = 'select DISTINCT recipeID, title, postedBy, AVG(stars) as avg \
                from Recipe NATURAL JOIN RecipeTag NATURAL JOIN Review \
                WHERE title like %s and tagText like %s \
                group by recipeID, title, postedBy \
                having AVG(stars) >= %s '
        search_input = '%{}%'.format(search_input)
        tag = '%{}%'.format(tag)
        cursor.execute(query, (search_input, tag, stars))


    results = cursor.fetchall()
    # results = cursor.fetchall()
    cursor.close()
    return render_template('search.html', results=results)

