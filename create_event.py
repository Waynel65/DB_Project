from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn
@app.route('/create_event', methods=['GET','POST'])
def create_event():
    GroupName = request.args.get('gName')
    return render_template("create_event.html")

@app.route('/event_detail', methods=['GET','POST'])
def event_detail():
    user = session['username']
    GroupName = request.form['gName']
    eventName=request.form['eventsName']
    eventDesc=request.form['eventDescription']

    cursor = conn.cursor();
    date_time='SELECT now();'
    cursor.execute(date_time)
    data = cursor.fetchone()
    query_1 = 'INSERT INTO FlaskDemo.Event (eName, eDesc,eDate,gName,gCreator) values (%s,%s, %s,%s, %s)'
    cursor.execute(query_1, (eventName, eventDesc,data['now()'],GroupName,user))
    conn.commit()
    cursor.close()

    return redirect('/dashboard')