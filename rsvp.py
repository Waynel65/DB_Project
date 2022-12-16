from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/event_rsvp/', methods=['GET','POST'])
def event_rsvp():
    user = session['username']
    gName = request.args.get('gName')
    gCreator = request.args.get('gCreator')

    cursor = conn.cursor();
    query = 'select eid from RSVP where %s != userName' 
    cursor.execute(query,(user))
    result = cursor.fetchall()
    cursor.close()
    return render_template("event_rsvp.html",result=result)

@app.route('/rsvp/', methods=['GET','POST'])
def rsvp():
    user = session['username']
    eventID=request.args.get('eID')
    cursor = conn.cursor();
    query = 'INSERT INTO FlaskDemo.RSVP (username, eID) values (%s,%s)' 
    cursor.execute(query,(user,eventID))
    conn.commit()
    cursor.close()
    return redirect('/dashboard')
