from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/dashboard')
def dashboard():
    if not session.get('user_is_logged_in'):
        return redirect('/login')
    username = session['username']
    print(username)
    cursor = conn.cursor();
    query = 'SELECT * FROM Recipe where postedBy = %s'
    cursor.execute(query, username)
    recipes = cursor.fetchall()

    # query_detect_group = 'Select gName FROM  \
    #                      (Person JOIN GroupMembership where Person.userName = GroupMembership.memberName) as Merged \
    #                       WHERE %s = GroupMembership.memberName or %s = gCreator'

    query_detect_group = 'SELECT gName, gCreator, eID FROM \
                          GroupMembership NATURAL JOIN Event \
                          WHERE %s = memberName or %s = gCreator'

    group_name = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', recipe_list=recipes, groups=group_name)


@app.route('/settings')
def settings():
    """
        will render a setting page that allows user to set their preference
    """

    return render_template('settings.html')

@app.route('/set_preferences', methods=['GET','POST'])
def set_preferences():
    unit = request.form['unit']
    session['unit_pref'] = unit ## either metric or imperial

    return redirect('/dashboard')

"""
    often seen units in recipes:
    https://en.wikibooks.org/wiki/Cookbook:Units_of_measurement#Volume
"""