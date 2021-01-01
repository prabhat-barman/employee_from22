from flask import *
import mysql.connector as mycon
app=Flask(__name__)
@app.route("/")
def detail():
    return render_template("login.html")

@app.route("/userreg")
def user():
    return render_template("from.html")
@app.route("/detail",methods=["POST"])
def det():
    fn=request.form["fn"]
    ln = request.form["ln"]
    dob=request.form["dob"]
    gender=request.form["gender"]
    experience=request.form["experience"]
    pic=request.file["photo"]
    pic.save(pic.filename)
    info = [fn, ln, dob, gender, experience]
    hobby=request.form.getlist('hobby')
    emp=mycon.connect(host="localhost" ,user ="root",password="",database="employee_from")
    if (emp.is_connected()):
            cur=emp.cursor()
            query="insert into detail (fname,lname,dob,gender,exp) values(%s,%s,%s,%s,%s)"
            cur.execute(query,info)
            cur.execute("select eid from detail order by eid desc limit 1")
            data=cur.fetchall()
            eid=int(list(data[0])[0])
            for per in hobby:
                hobby_list=[eid,per]
                query="insert into hobby(eid,hobbies) values (%s,%s)"
                cur.execute(query,hobby_list)
            return("inserted")
    else:
            print("not connected properly")
        #return render_template("display.html",info=info)
    hobby = request.form.getlist("hobby")
    cur=emp.cursor()
    query1="insert into hobby (hobbies) values(%s)"
    cur.execute(query1)
    cur.close()




@app.route('/getData')
def getData():
    emp=mycon.connect(host="localhost",password="",user="root",database="employee_from")
    cur=emp.cursor()
    cur.execute("select * from detail")
    data=cur.fetchall()
    return render_template('display2.html',data=data)
    return("data comes here")

@app.route('/profile',methods=['GET'])
def profile():
    eid=request.args['eid']
    getinfo=[]
    getinfo.append(eid)
    emp = mycon.connect(host="localhost", password="", user="root", database="employee_from")
    cur = emp.cursor()
    cur2 = emp.cursor()
    query2="select hobbies from hobby where eid=%s"
    cur2.execute(query2,(eid,))
    data2 = cur2.fetchall()
    query="select * from detail where eid=%s"
    cur.execute(query,(eid,))
    data = cur.fetchone()
    return render_template('profile.html', data=data,data2=data2)

@app.route('/deleteemp',methods=['GET'])
def deleteemp():
    eid=request.args['eid']
    emp = mycon.connect(host="localhost", password="", user="root", database="employee_from")
    cur = emp.cursor()
    query = "delete from detail where eid=%s"
    query2="delete from hobby where eid=%s"
    cur.execute(query, (eid,))
    cur.execute(query2, (eid,))
    return redirect('/getData')
app.run(debug=True,port=5485)

