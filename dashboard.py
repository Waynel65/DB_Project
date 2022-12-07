from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/dashboard')
def dashboard():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT * FROM Recipe where postedBy = %s'
    cursor.execute(query, username)
    recipes = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', recipe_list=recipes)