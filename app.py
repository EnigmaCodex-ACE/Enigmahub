from flask import Flask, render_template,redirect,url_for,request,flash
from flaskext import markdown
import flask
from random import choice
from handledb import *
import json
import os
import requests
from jnturesultscrap import JNTUResult

app = Flask(__name__)
md = markdown.Markdown(app, extensions=['footnotes'])

@app.route('/')
@app.route('/miniproject/')
def home():
    return render_template('index.html',title='projects',posts=curated_db_data(),post_type="Curated Projects")

@app.route('/id/<int:post_id>')
@app.route('/miniproject/id/<string:id>')
def detail_page(id):
    return render_template('detail.html',title='detail',post=fetch_db_from_id(id))

@app.route('/search/<string:id>')
def search_db(id):
    return render_template('detail.html',title='detail',post=fetch_db_from_id(id))

@app.route('/huh')
def huh():
    errmsg = request.args.get('errmsg')
    return render_template('messprinter.html', showmessage=errmsg)


@app.route('/attd', methods=['GET'])
def attendance():
    errmsg = ""
    rollNo = request.args.get('rollno')
    print(rollNo)
    if(rollNo != None):
        try:
            attdnce = attddb.find({'_id': str(rollNo)})[0]
            attdnce = attdnce['attendance'] + " %"
        except:
            try:
                attdnce = fetchAttendance(str(rollNo))
                attdnce = attdnce + " %"
            except:
                randtaunts = ["Hm.. I don't know , where are you?","You don't exist in this universe...ahem database",f"Dear {rollNo} , Your existence is a mystery to me"]
                attdnce = {
                    '_id': str(rollNo),
                    'attendance': choice(randtaunts),
                    'name': "god.getName(babyID=\"400\")"
                }
        return render_template('attendance.html', errmsg=errmsg ,attdlist = attdnce)
    return render_template('attendance.html')


@app.route('/results')
def results():
    errmsg = None
    rollno = request.args.get('rollno')
    if(rollno != None):
        if("<" in rollno):
            err = "Wtf you trynna do m8??"
            return redirect(url_for('.huh', errmsg=err), code=302)
        if("rickroll" in rollno.replace(" ", "").lower()):
            err = "lol"
            return redirect(url_for('.results', errmsg=err), code=302)

        if('hentai' in rollno.replace(" ", "").lower()):
            err = "boi you're in a wrong website"
            return redirect(url_for('.huh', errmsg=err), code=302)

        if('jojo' in rollno.replace(" ", "").lower()):
            err = "ORA ORA ORA ORA ORA , Yes Oh My God b64:am9pbiB0aGUgY3VsdCBib2kgaHR0cHM6Ly9kaXNjb3JkLmdnL3NEOUU3VWQ="
            return redirect(url_for('.huh', errmsg=err), code=302)

    examcode = request.args.get('examcode')

    if(rollno or examcode):
        messages = json.dumps({"rollno": rollno, "examcode": examcode})
        return redirect(url_for('.showresult', messages=messages), code=302)
    if(request.args.get("messages") != None):
        errmsg = "Result not found ... Server didnt respond ( Probably RollNo Doesn't Exist )"
    else:
        errmsg = None

    try:
        examc = list(ecodes.find())
    except:
        examc = []
        print(examc)

    return render_template('home.html', errmsg=errmsg ,examcodes=examc)


@app.route('/showresult')
def showresult():
    messages = {'test':'lol'}
    try:
        msg = json.loads(request.args['messages'])
        
        dbMode = False
        
        rollNo = msg['rollno']
        examCode = msg['examcode']

        if(rollNo == None or examCode == None):
            responsejson = {
                'message': "Give a roll no and exam code"
            }
            return flask.jsonify(responsejson)
        try:
            resultWithSGPA = db.find({'unique': str(rollNo+examCode)})[0]
            resultWithSGPA.pop('_id')
            dbMode = False
        except IndexError:
            jr = JNTUResult(rollNo, examCode)
            jrmethod = jr.recursiveGet()
            try:
                SGPA = jrmethod['sgpa']
            except Exception as e:
                SGPA = "Coudn't Calculate due to > " + str(e)
            result = jrmethod['result']
            dbMode = True  # add to db for caching
            resultWithSGPA = {
                'unique': str(rollNo+examCode),
                'rollno': str(rollNo),
                'examcode': str(examCode),
                'result': result,
                'sgpa': SGPA,
                'usr': jrmethod['user']
            }

        jsonified = flask.jsonify(resultWithSGPA)
        try:
            if(dbMode):
                if(type(resultWithSGPA['sgpa']) == float or type(resultWithSGPA['sgpa']) == int):
                    print("Insert to dB cuz valid result")
                    db.insert_one(resultWithSGPA)
                dbMode = False
        except Exception as e:
            print(e)

        print(messages)
        return render_template('result.html', messages=resultWithSGPA, tabcol=len(resultWithSGPA['result']) , title=resultWithSGPA['rollno'])
    except ValueError as e:
        messages = f"someerror"
        return redirect(url_for('.home', messages=messages, code=302))


@app.route('/jnturesult', methods=['GET'])
def jntuRequestsAPI():
    # take post requests parameters and pass it through JNTUResultAPI
    dbMode = False
    rollNo = flask.request.args.get('rollno')
    examCode = flask.request.args.get('examcode')

    if(rollNo == None or examCode == None):
        responsejson = {
            'message': "Give a roll no and exam code"
        }
        return flask.jsonify(responsejson)
    try:
        resultWithSGPA = db.find({'unique': str(rollNo+examCode)})[0]
        resultWithSGPA.pop('_id')
        dbMode = False
    except IndexError:
        jr = JNTUResult(rollNo, examCode)
        jrmethod = jr.recursiveGet()
        try:
            SGPA = jrmethod['sgpa']
        except Exception as e:
            SGPA = "Coudn't Calculate due to > " + str(e)
        result = jrmethod['result']
        dbMode = True  # add to db for caching
        resultWithSGPA = {
            'unique': str(rollNo+examCode),
            'rollno': str(rollNo),
            'examcode': str(examCode),
            'result': result,
            'sgpa': SGPA,
            'usr': jrmethod['user']
        }

    jsonified = flask.jsonify(resultWithSGPA)
    try:
        if(dbMode):
            if(type(resultWithSGPA['sgpa']) == float or type(resultWithSGPA['sgpa']) == int):
                print("Insert to dB cuz valid result")
                db.insert_one(resultWithSGPA)
            dbMode = False
    except Exception as e:
        print(e)

    return jsonified


@app.route(r'/login')
def login_doesnt_exist():
    return choice(["wut u lookin for mate", "hmm there should be something important here right?", "something seems missing...!! weird"])




@app.route('/miniproject/all/<int:pageno>')
@app.route('/miniproject/all')
@app.route('/all/<int:pageno>')
@app.route('/all')
def all_page(pageno=0):
    if(pageno>=0):
        return render_template('index.html',title='all',posts=fetch_db_data(skip=pageno),post_type="All Projects",pgno=pageno+1)
    else:
        return render_template('index.html',title='all',posts=fetch_db_data(skip=0),post_type="All Projects",pgno=1,ermsg="Negative Numbers!!! ... Someone's learning url editing boi")

@app.errorhandler(404)
def handle404(e):
    msgs = ["Would you look at that.. someone's stalking my urls", "Are you supposed to be here?", "no..." , "Someone learning baby steps of hacking" , " I know the urls are too predictable but I'm not sure if you're supposed to be here" , "Not all urls are available ... I'm not sure if you're supposed to be here"]
    if(choice(range(0,10)) < 2):
        return redirect('https://youtu.be/dQw4w9WgXcQ')
    return render_template('404.html',ermsg=choice(msgs)), 404



if(__name__ == '__main__'):
    app.run(threaded=True,host="0.0.0.0", port=os.environ['PORT'])
    app.register_error_handler(404, handle404)
