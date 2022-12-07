from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/post_recipe')
def post_recipe():
    return render_template('create_recipe.html')