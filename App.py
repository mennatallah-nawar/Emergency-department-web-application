import os
from flask import Flask,flash, render_template, request,redirect,url_for
from werkzeug.utils import secure_filename
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="databaseApp"  
)
mycursor = mydb.cursor()
# Code of created tables :

# mycursor.execute("CREATE TABLE Doctor (name VARCHAR(255), ID INT, Phone INT, Email VARCHAR(255), Password INT, PRIMARY KEY(ID,name))")

# mycursor.execute("CREATE TABLE Operating_rooms (Room_num INT, type VARCHAR(255),PRIMARY KEY(Room_num))")

# mycursor.execute("CREATE TABLE Surgeries (Room_no INT, Doc_ID INT, Pat_ID INT, Date VARCHAR(255), St_time VARCHAR(255), End_time VARCHAR(255) , PRIMARY KEY(Room_no,Date,St_time),FOREIGN KEY (Doc_ID) REFERENCES Doctor(ID),FOREIGN KEY (Room_no) REFERENCES Operating_rooms(Room_num))")

# mycursor.execute("CREATE TABLE Admin (name VARCHAR(255), Email VARCHAR(255), ID INT, Phone INT, Password INT, PRIMARY KEY(ID))")

# mycursor.execute("CREATE TABLE Complaints (id INT auto_increment ,email VARCHAR(255) , message VARCHAR(255),User_ID INT,  PRIMARY KEY(id))")

# mycursor.execute("CREATE TABLE Patient (ID INT,name VARCHAR(255),gender VARCHAR(255),age INT, blood_type VARCHAR(255),Phone INT, Email VARCHAR(255),Diagnosis VARCHAR(255),Supv_Doctor_info INT,Patient_scans VARCHAR(255),Allergies VARCHAR(255),medicine VARCHAR(255),PRIMARY KEY(ID),Password INT)")

#mycursor.execute("CREATE TABLE Special_requests (User_ID INT, category VARCHAR(255),request VARCHAR(255),PRIMARY KEY(User_ID,category))")

# mycursor.execute("ALTER TABLE Complaints AUTO_INCREMENT=1")


# mycursor.execute("ALTER TABLE Surgeries ADD FOREIGN KEY (Pat_ID) REFERENCES Patient(ID)")

# mycursor.execute("ALTER TABLE Patient ADD FOREIGN KEY (Supv_Doctor_info) REFERENCES Doctor(ID)")




app = Flask(__name__)


@app.route('/')
def index():
   return render_template("Home.html")


# @app.route('/signin')
# def signin():
#    return render_template("signin.html")


@app.route('/signin', methods=['POST','GET'])
def signin():
   if request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]

      sql = ('SELECT * FROM admin WHERE ID = %s AND Password = %s')
      values=(username, password)
      mycursor.execute(sql,values)
      admin = mycursor.fetchall()
      if (admin):
             #done by ola about admin page
         mycursor.execute("SELECT * FROM Surgeries")
         row_headers=[x[0] for x in mycursor.description]
         myresult = mycursor.fetchall()
         for i in myresult:
            print(i)
         data={
            'rec':myresult,
            'header':row_headers
            }
         mycursor.execute("SELECT * FROM Special_requests")
         row_headers=[x[0] for x in mycursor.description]
         myresult = mycursor.fetchall()
         for i in myresult:
            print(i)
         DBRequests={
         'rec':myresult,
         'header':row_headers
         }
         mycursor.execute("SELECT * FROM Complaints")
         row_headers=[x[0] for x in mycursor.description]
         myresult = mycursor.fetchall()
         for i in myresult:
            print(i)
         DBComplaints={
         'rec':myresult,
         'header':row_headers
         }
         mycursor.execute("SELECT count(message) FROM complaints")
         Complaints = mycursor.fetchone()
         mycursor.execute("SELECT count(request) FROM special_requests")
         Requests = mycursor.fetchone()
         RequestsComplaints = [Requests[0], Complaints[0]]
         RecComplabels=[ "Requests" , "Complaints" ]
         mycursor.execute("SELECT count(ID) FROM doctor")
         Doctors = mycursor.fetchone()
         mycursor.execute("SELECT count(ID) FROM Patient")
         Patients = mycursor.fetchone()
         patdoc = [Patients[0], Doctors[0]]
         patdoclabels=[ "Patients" , "Doctors" ]
         mycursor.execute("SELECT date, count(date) FROM surgeries GROUP BY date ORDER BY date")
         SurguriesDone= mycursor.fetchall()
         SurguriesDoneLabels=[]
         SurguriesDoneValues=[]
         for (label, count) in SurguriesDone:
            SurguriesDoneLabels.append(label)
            SurguriesDoneValues.append(count)
         mycursor.execute("SELECT blood_type, count(blood_type) FROM patient GROUP BY blood_type")
         BloodType= mycursor.fetchall()
         BloodTypeLabels=[]
         BloodTypeValues=[]
         for (label, count) in BloodType:
            BloodTypeLabels.append(label)
            BloodTypeValues.append(count)
            print(BloodTypeValues)
         return render_template('admin2.html',info=admin , data=data, dbComplaints=DBComplaints, dbRequests=DBRequests, legend = 'Surguries Made',patdoc=patdoc,patdoclabels=patdoclabels,RequestsComplaints=RequestsComplaints,RecComplabels=RecComplabels,SurguriesDoneLabels=SurguriesDoneLabels,SurguriesDoneValues=SurguriesDoneValues,BloodTypeLabels=BloodTypeLabels,BloodTypeValues=BloodTypeValues)
   #end by ola (Admin GET)
             

      sql = ('SELECT * FROM doctor WHERE ID = %s AND Password = %s')
      values=(username, password)
      mycursor.execute(sql,values)
      doctor = mycursor.fetchall()
      if (doctor):
         return render_template('Doctors.html', info = doctor)

      sql = ('SELECT * FROM patient WHERE ID = %s AND Password = %s')
      values=(username, password)
      mycursor.execute(sql,values)
      patient = mycursor.fetchall()


      if (patient):
        
      
         sql="SELECT Medicine FROM Patient"
         mycursor.execute(sql)
         row_headers=[x[0] for x in mycursor.description]
         myresult = mycursor.fetchall()
         med={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
         }
         
         #Selecting doctor's info for Contact
         mycursor.execute("SELECT Supv_Doctor_info FROM Patient")
         row_headers=[x[0] for x in mycursor.description]
         myresult = mycursor.fetchall()
         Cont={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
         }
         print("here ola")
         print(patient[0][0])
         mycursor.execute("SELECT Surgeries.Room_no, Surgeries.Date, Surgeries.St_time ,Surgeries.End_time,Operating_rooms.type From Patient JOIN Surgeries on Surgeries.Pat_ID=Patient.ID JOIN Operating_rooms ON Surgeries.Room_no=Operating_rooms.Room_num WHERE patient.ID=%s",(patient[0][0],))
         print("here again")
         row_headers=[x[0] for x in mycursor.description]
         myresult = mycursor.fetchall()
         Op={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
         }
          #Selecting Diagonsis info 
         mycursor.execute("SELECT Diagnosis FROM Patient")
         row_headers=[x[0] for x in mycursor.description] 
         myresult = mycursor.fetchall()
         Go={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
         }
         #giving variables to be used in patient.html
         return render_template("Patients.html", info = patient ,no=Cont,dd=Op,ee=Go,aa=med)

   else:
      return render_template("signin.html")

# @app.route('/signup')
# def signup():
       
#    return render_template("signup.html")
@app.route('/signup', methods =['GET', 'POST'])
def signup():
   msg = '' 
   if request.method == 'POST':
      name = request.form['name']
      ID=request.form['id']
      type = request.form['type']
      password = request.form['password']
      phone = request.form['phone']

      email = request.form['email']

      age = request.form['age']

      gender = request.form['gender']

      bloodtype = request.form['bloodtype']

      allergy = request.form['allergy']

      cursor = mydb.cursor()

		#cursor.execute('SELECT * FROM accounts WHERE name = % s', (name, )) 
		#account = cursor.fetchone()
      if type=="dr":
         cursor.execute('INSERT INTO Doctor (name,Email,ID,Phone,Password) VALUES (%s,%s, %s, %s, %s)', (name,email,ID,phone,password ))
         mydb.commit()
         msg = 'You have successfully registered !'
      elif type=="patient":
         cursor.execute('INSERT INTO Patient (name,Email,ID,Phone,Password,age,gender,blood_type,Allergies)  VALUES (%s, %s, %s, %s , %s, %s, %s, %s, %s)', (name,email,ID,phone,password,age,gender,bloodtype,allergy  ))
         mydb.commit()
         msg = 'You have successfully registered !'
      elif type=="admin":
         print("love")
         cursor.execute('INSERT INTO Admin (name, Email, ID, Phone, Password) VALUES (%s, %s, %s, %s, %s)', (name,email,ID,phone,password  ))
         mydb.commit()
         msg = 'You have successfully registered !'
   return render_template("signup.html", msg = msg)


@app.route('/complain', methods=['POST','GET'])
def contactus():   
   if request.method=="POST":
      user_id = request.form['user_id']
      email = request.form['email']
      message = request.form['message']
      try:
         sql = "INSERT INTO Complaints (email, message,user_id) VALUES (%s, %s, %s)"
         val = (email,message,user_id)
         mycursor.execute(sql, val)
         mydb.commit()   
         return render_template("Home.html")
      except:
         return render_template("complain.html")
   else:
      return render_template("complain.html")






#Admin's part (ola)
@app.route('/admin2',methods = ['POST', 'GET'])
def admin2():
   if request.method == 'POST':
       #Edit profile
       
       name = request.form['name']
       email = request.form['email']
       password = request.form['password']
       phone=request.form['phone']
       id=request.form['ID']
       sql="UPDATE Admin SET name= %s, Email= %s ,  Password= %s , phone=%s  WHERE ID= %s "
       val=(name,email,password,phone,id)
       mycursor.execute(sql,val)
       mydb.commit()
       
      
       return  redirect(url_for('admin2'))
   else:
      mycursor.execute("SELECT * FROM Surgeries")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      for i in myresult:
         print(i)
      data={
         'rec':myresult,
         'header':row_headers
      }
      mycursor.execute("SELECT * FROM Special_requests")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      for i in myresult:
         print(i)
      DBRequests={
         'rec':myresult,
         'header':row_headers
      }

      mycursor.execute("SELECT * FROM Complaints")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      for i in myresult:
         print(i)
      DBComplaints={
         'rec':myresult,
         'header':row_headers
      }
      

      mycursor.execute("SELECT count(complaint) FROM complaints")
      Complaints = mycursor.fetchone()

      mycursor.execute("SELECT count(request) FROM special_requests")
      Requests = mycursor.fetchone()

      RequestsComplaints = [Requests[0], Complaints[0]]
      RecComplabels=[ "Requests" , "Complaints" ]



      mycursor.execute("SELECT count(ID) FROM doctor")
      Doctors = mycursor.fetchone()

      mycursor.execute("SELECT count(ID) FROM Patient")
      Patients = mycursor.fetchone()

      patdoc = [Patients[0], Doctors[0]]
      patdoclabels=[ "Patients" , "Doctors" ]


      mycursor.execute("SELECT date, count(date) FROM surgeries GROUP BY date ORDER BY date")
      SurguriesDone= mycursor.fetchall()
      SurguriesDoneLabels=[]
      SurguriesDoneValues=[]
      for (label, count) in SurguriesDone:
         SurguriesDoneLabels.append(label)
         SurguriesDoneValues.append(count)

      mycursor.execute("SELECT blood_type, count(blood_type) FROM patient GROUP BY blood_type")
      BloodType= mycursor.fetchall()
      BloodTypeLabels=[]
      BloodTypeValues=[]
      for (label, count) in BloodType:
         BloodTypeLabels.append(label)
         BloodTypeValues.append(count)
      print(BloodTypeValues)
      info=['ola',12,'jbjhik',244,'ddfbv']
      return render_template('admin2.html',info=info, data=data, dbComplaints=DBComplaints, dbRequests=DBRequests, legend = 'Surguries Made',patdoc=patdoc,patdoclabels=patdoclabels,RequestsComplaints=RequestsComplaints,RecComplabels=RecComplabels,SurguriesDoneLabels=SurguriesDoneLabels,SurguriesDoneValues=SurguriesDoneValues,BloodTypeLabels=BloodTypeLabels,BloodTypeValues=BloodTypeValues)
   return render_template('admin2.html')
@app.route('/admin2/searchDoctor',methods = ['POST', 'GET'])
def searchDoctor():
   if request.method == 'POST':
      dname=request.form['searchDoc']
      print(dname)
      mycursor.execute("SELECT name,ID,Phone,Email FROM `Doctor` WHERE name= %s ",(dname,))
      myresult = mycursor.fetchall()
      print(myresult)
      for i in myresult:
         print(i)
      return render_template('searchDoctor.html',result=myresult)
   return render_template('searchDoctor.html')

@app.route('/admin2/searchPatient',methods = ['POST', 'GET'])
def searchPatient():
   if request.method == 'POST':
      pname=request.form['searchPat']
      print(pname)
      mycursor.execute("SELECT name,ID,age,gender,Phone,Email FROM `Patient` WHERE name= %s ",(pname,))
      myresult = mycursor.fetchall()
      print(myresult)
      for i in myresult:
         print(i)
      # Did=myresult[0][6]
      # mycursor.execute("SELECT name FROM `Doctor` WHERE ID= %s ",(Did,))
      # dname = mycursor.fetchall()
      dname=0
      return render_template('searchPatient.html',result=myresult,dname=dname)

   return render_template('searchPatient.html')

@app.route('/admin2/AddSurgery',methods = ['POST', 'GET'])
def AddSurgery():
   if request.method == 'POST':
      room=request.form['roomNo']
      did=request.form['docId']
      pid=request.form['patId']
      print(room,did,pid)
      d=request.form['date']
      start=request.form['st']
      et=request.form['end_time']
      print(room,did,pid,d,start,et)
      try:
         sql = "INSERT INTO `surgeries`(`Room_no`, `Doc_ID`, `Pat_ID`, `Date`, `St_time`, `End_time`) VALUES (%s, %s, %s, %s, %s, %s)"
         val = (room,did,pid,d,start,et)
         mycursor.execute(sql, val)
         mydb.commit()   
         return render_template('AddSurgery.html',message="Surgery has been added successfully in room "+room)
      except:
         return render_template('AddSurgery.html',error="Something wrong please try again")
      return render_template('AddSurgery.html')
   return render_template('AddSurgery.html')   

@app.route('/admin2/AdminProfile',methods = ['POST', 'GET'])
def AdminProfile(): 
   return render_template('AdminProfile.html')


 #Patients: Fatmah's Part  
@app.route('/Patients')
def Patients():
       #Selecting medicine that was inserted by patient
   if request.method == 'GET':
      mycursor.execute("SELECT Medicine FROM Patient")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      med={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
       }

      #Selecting sign info in patient profile
      mycursor.execute("SELECT ID,name,gender,age,blood_type,Phone,Email FROM Patient")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
       }
      
      #Selecting doctor's info for Contact
      mycursor.execute("SELECT Supv_Doctor_info FROM Patient")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      Cont={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
       }
      
      #Selecting Operation plan info
      mycursor.execute("SELECT Surgeries.Room_no, Surgeries.Date, Surgeries.St_time ,Surgeries.End_time,Operating_rooms.type From Patient JOIN Surgeries on Surgeries.Pat_ID=Patient.ID JOIN Operating_rooms ON Surgeries.Room_no=Operating_rooms.Room_num")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      Op={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
       }
      #giving variables to be used in patient.html
      return render_template("Patients.html",data=data,no=Cont,dd=Op,aa=med)
      

#For uploading scans
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/Patients/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('file uploaded successfully')
            return redirect(url_for('upload'))
    return  render_template("upload.html")


#Farah's Part
@app.route('/DOCPAT',methods = ['POST', 'GET'])
def DOCPAT():
    if request.method=="POST":
      doc_id = request.form["doc_ID"]
      try:
         sql= "SELECT patient.name, patient.ID, patient.blood_type, patient.Email FROM patient JOIN doctor ON doctor.ID = patient.Supv_Doctor_info WHERE doctor.ID = %s"
         val = (doc_id,)
         mycursor.execute(sql, val)
         myresult = mycursor.fetchall()
         for i in myresult:
           print(i)
         return render_template("DOCPAT.html" ,esm =myresult)
      except:
         return render_template("DOCPAT.html")
    else:
      return render_template("DOCPAT.html")

@app.route('/patienthistory')
def patienthistory():
      mycursor.execute("SELECT * FROM Patient")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      for i in myresult:
         print(i)
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('patienthistory.html',data=data)

@app.route('/Doctors',methods = ['POST', 'GET'])
def Doctors():
   if request.method == 'POST':
       #Edit profile
       
       name = request.form['name']
       email = request.form['email']
       password = request.form['password']
       phone=request.form['phone']
       id=request.form['ID']
       sql="UPDATE Doctor SET name= %s, Email= %s ,  Password= %s , phone=%s  WHERE ID= %s "
       val=(name,email,password,phone,id)
       mycursor.execute(sql,val)
       mydb.commit()
       
       return  redirect(url_for('Doctors'))
   else:
      info=['',0,'', 0,'']
      return render_template('Doctors.html',info=info) 
   return render_template('Doctors.html')

@app.route('/Adddiagnosis',methods = ['POST', 'GET'])
def Adddiagnosis():
   if request.method == 'POST':
       diagnosis=request.form['diagnosis']
       id=request.form['ID']
       sql="UPDATE Patient SET Diagnosis= %s  WHERE ID= %s "
       val=(diagnosis,id)
       mycursor.execute(sql,val)
       mydb.commit()
       return  redirect(url_for('Adddiagnosis'))
   else:
       return render_template('Adddiagnosis.html') 
   return render_template('Adddiagnosis.html')


@app.route('/AddComplaints',methods = ['POST', 'GET'])
def AddComplaints():
   if request.method == 'POST':
      uid=request.form['userid']
      category=request.form['category']
      complaint=request.form['complaint']
      print(uid,category,complaint)
      try:
         sql = "INSERT INTO `Complaints`(`User_ID`, `category`, `complaint`) VALUES (%s, %s, %s)"
         val = (uid,category,complaint)
         mycursor.execute(sql, val)
         mydb.commit()   
         return render_template('AddComplaints.html',message="complaint has been added successfully")
      except:
         return render_template('AddComplaints.html',msg="complaint has been added successfully")
      return render_template('AddComplaints.html')
   return render_template('AddComplaints.html')


@app.route('/AddRequests',methods = ['POST', 'GET'])
def AddRequests():
   if request.method == 'POST':
      uid=request.form['userid']
      category=request.form['category']
      reques=request.form['request']
      print(uid,category,request)
      try:
         sql = "INSERT INTO `Special_requests`(`User_ID`, `category`, `request`) VALUES (%s, %s, %s)"
         val = (uid,category,reques)
         mycursor.execute(sql, val)
         mydb.commit()   
         return render_template('AddRequests.html',message="Request has been added successfully")
      except:
         return render_template('AddRequests.html',msg="Request has been added successfully")
      return render_template('AddRequests.html')
   return render_template('AddRequests.html')


@app.route('/AddMedicine',methods = ['POST', 'GET'])
def AddMedicine():
   if request.method == 'POST':
       medicine=request.form['medicine']
       id=request.form['ID']
       sql="UPDATE Patient SET medicine = %s  WHERE ID= %s "
       val=(medicine,id)
       mycursor.execute(sql,val)
       mydb.commit()
       return  redirect(url_for('AddMedicine'))
   else:
       return render_template('AddMedicine.html') 
   return render_template('AddMedicine.html')

@app.route('/Doctors/DoctorProfile',methods = ['POST', 'GET'])
def DoctorProfile(): 
   return render_template('DoctorProfile.html')

@app.route('/Getprofile',methods = ['POST', 'GET'])
def Getprofile():
    if request.method=="POST":
      doc_id = request.form["doc_ID"]
      try:
         sql= "SELECT patient.name, patient.ID, patient.blood_type, patient.Email FROM patient JOIN doctor ON doctor.ID = patient.Supv_Doctor_info WHERE doctor.ID = %s"
         val = (doc_id,)
         mycursor.execute(sql, val)
         myresult = mycursor.fetchall()
         for i in myresult:
           print(i)
         return render_template("DOCPAT.html" ,esm =myresult)
      except:
         return render_template("DOCPAT.html")
    else:
      return render_template("DOCPAT.html")



if __name__ == '__main__':
   app.run()
