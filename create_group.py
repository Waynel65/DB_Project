#group membership and group table

from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/create_group')
def create_group():
    return render_template('create_group.html')

@app.route('/group_detail')
def group_detail():
    user = session['username']
    GroupName = request.form['GroupName']
    description=request.form['description']

    cursor = conn.cursor();
    query_1 = 'INSERT INTO Group (gName, gCreator, gDesc) \
            values (%s, %s, %s) '

    query_2= 'INSERT INTO GroupMembership (memberName, gName, gCreator) \
            values (%s, %s, %s) '
    cursor.execute(query_1, (user, GroupName, description))
    cursor.execute(query_2, (user, GroupName, user))
    conn.commit()
    cursor.close()

    return render_template('group_detail.html')