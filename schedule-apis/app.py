import calendar
import datetime
import requests
from operator import and_
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import extract

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://269hfclo1agvd0hd4lwp:pscale_pw_aY7dXTNvklEK4saRT0Sqw6YT5hNbuyiP1bP3J6fegZh@us-east.connect.psdb.cloud/care-coordination-and-management?ssl=true'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db= SQLAlchemy(app)

ma = Marshmallow(app)

class Schedule(db.Model):
  __tablename__ = "Schedule"
  id = db.Column(db.Integer, primary_key = True)
  userName = db.Column(db.String(255))
  createdAt = db.Column(db.DateTime)
  modifiedAt = db.Column(db.DateTime)
  scheduleActivity = db.Column(db.String(255))
  providerGroup = db.Column(db.String(255))
  scheduleStatus = db.Column(db.String(255))
  scheduleDate = db.Column(db.Date)
  scheduleFrom = db.Column(db.DateTime)
  scheduleTo = db.Column(db.DateTime)
  userId = db.Column(db.Integer)
  patientId = db.Column(db.Integer)
  roomNumber = db.Column(db.Integer)


  def __init__(self, id, userName, createdAt, modifiedAt, scheduleActivity, providerGroup,scheduleStatus, scheduleDate, scheduleFrom, scheduleTo, userId, patientId, roomNumber):
    self.id = id
    self.userName = userName
    self.createdAt =createdAt
    self.modifiedAt =modifiedAt
    self.scheduleActivity = scheduleActivity
    self.providerGroup = providerGroup
    self.scheduleStatus = scheduleStatus
    self.scheduleDate = scheduleDate
    self.scheduleFrom =scheduleFrom
    self.scheduleTo =scheduleTo
    self.userId = userId
    self.patientId =patientId
    self.roomNumber =roomNumber

class ScheduleSchema(ma.Schema):
  class Meta:
    fields = ('userName', 'scheduleActivity', 'scheduleDate', 'scheduleFrom', 'scheduleTo', 'roomNumber', 'scheduleStatus', 'scheduleId', 'userId', 'patientId', 'id' )

schedule_Schema = ScheduleSchema()
all_schedule_schema = ScheduleSchema(many = True)

@app.route("/schedule/currentDaySchedule", methods = ['GET'])
def getCurrentDaySchedule():
  auth_Key = request.headers.get('Auth-Key', None)
  if auth_Key == "pc7inqnmni8ec7j32qki":
    all_Schedule = Schedule.query.filter_by(scheduleDate=datetime.date.today()).all()
    result = all_schedule_schema.dump(all_Schedule)
    return jsonify(result)
  else:
    return jsonify({"Message": "Authentication Failed."}) 

@app.route("/schedule/monthlySchedule/<string:month>", methods = ['GET'])
def getMonthlySchedule(month):
  auth_Key = request.headers.get('Auth-Key', None)
  if auth_Key == "4hn1q79l2b4ftj6oprwk":
    num_days = calendar.monthrange(int(month[:4]), int(month[5:7]))[1]
    start_date = datetime.date(int(month[:4]), int(month[5:7]), 1)
    end_date = datetime.date(int(month[:4]), int(month[5:7]), num_days)
    all_Schedule = Schedule.query.filter(and_(Schedule.scheduleDate >= start_date, Schedule.scheduleDate <= end_date)).all()
    result = all_schedule_schema.dump(all_Schedule)
    return jsonify(result)
  else:
    return jsonify({"Message": "Authentication Failed."}) 

@app.route("/schedule/userSchedule/<string:userID>&<string:date>", methods = ['GET'])
def getUserSchedule(userID,date):
  auth_Key = request.headers.get('Auth-Key', None)
  if auth_Key == "yycvi9cmp1sjbnv53kyl":
    all_Schedule = Schedule.query.filter_by(userId=userID, scheduleDate=datetime.datetime.strptime(date, '%Y-%m-%d').date()).all()
    result = all_schedule_schema.dump(all_Schedule)
    return jsonify(result)
  else:
    return jsonify({"Message": "Authentication Failed."}) 


@app.route("/schedule/newUserSchedule", methods = ['POST'])
def addNewUserSchedule():
  auth_Key = request.headers.get('Auth-Key', None)
  if auth_Key == "lb8xqjvlw9hbt3pj9mbs":
    doctor = requests.get('https://creepy-dog-sunglasses.cyclic.app/doctors/'+request.json['userId'])
    doctorObj = doctor.json()
    if not 'data' in doctorObj or len(doctorObj['data']) == 0:
      return jsonify({"Message": "Doctor with ID: "+request.json['userId']+" not found."}) 
    else:
      patient = requests.get('https://dzsqyl-8080.preview.csb.app/patient/single/'+request.json['patientId'])
      if patient.text == "Patient with ID: "+request.json['patientId']+" not found.":
        return jsonify({"Message": "Patient with ID: "+request.json['patientId']+" not found."}) 
      else:
        all_Schedule = Schedule.query.filter(Schedule.userId == request.json['userId']).\
                                      filter(Schedule.scheduleStatus == "New").\
                                      filter(and_(request.json['scheduleFrom'] >= Schedule.scheduleFrom, request.json['scheduleFrom'] <= Schedule.scheduleTo)).\
                                      filter(and_(request.json['scheduleTo'] >= Schedule.scheduleFrom,request.json['scheduleTo'] <= Schedule.scheduleTo)).all()
        result = all_schedule_schema.dump(all_Schedule)
        if len(result):
          return jsonify({"Message": "Schedule not available.Please change time"}) 
        else:
          all_rooms = Schedule.query.filter(Schedule.roomNumber == request.json['location']).\
                                    filter(Schedule.scheduleStatus == "New").\
                                    filter(and_(request.json['scheduleFrom'] >= Schedule.scheduleFrom, request.json['scheduleFrom'] <= Schedule.scheduleTo)).\
                                    filter(and_(request.json['scheduleTo'] >= Schedule.scheduleFrom,request.json['scheduleTo'] <= Schedule.scheduleTo)).all()
          result = all_schedule_schema.dump(all_rooms)
          if len(result):
            return jsonify({"Message": "Room not available.Please change room number"}) 
          else:
            
            latestSchedule = Schedule.query.order_by(Schedule.id.desc()).first()
            if latestSchedule is None:
              id =1
            else:
              id = latestSchedule.id + 1
            userId = request.json['userId']
            userName = request.json['userName']
            createdAt = datetime.date.today()
            modifiedAt = datetime.date.today()
            scheduleActivity = request.json['activity']
            providerGroup = request.json['providerGroup']
            scheduleStatus = request.json['scheduleStatus']
            scheduleDate = request.json['scheduleDate']
            scheduleFrom = request.json['scheduleFrom']
            scheduleTo = request.json['scheduleTo']
            patientId = request.json['patientId']
            roomNumber = request.json['location']
            new_Schedule = Schedule(id, userName, createdAt, modifiedAt,  scheduleActivity, providerGroup, scheduleStatus,scheduleDate, scheduleFrom, scheduleTo, userId, patientId, roomNumber)

            db.session.add(new_Schedule)
            db.session.commit()

            return jsonify({"Message": "User schedule added successfully"}) 
  else:
    return jsonify({"Message": "Authentication Failed."}) 

@app.route("/schedule/userSchedule/<string:schID>", methods = ['PUT'])
def updateUserSchedule(schID):
  auth_Key = request.headers.get('Auth-Key', None)
  if auth_Key == "ibwq7p5384dph4ird1mg":
    schedule = Schedule.query.get(schID)
    if schedule is None:
      return jsonify({"Message": "Invalid Schedule. Please select valid schedule."}) 
    else:
      doctor = requests.get('https://creepy-dog-sunglasses.cyclic.app/doctors/'+request.json['userId'])
    doctorObj = doctor.json()
    if not 'data' in doctorObj or len(doctorObj['data']) == 0:
      return jsonify({"Message": "Doctor with ID: "+request.json['userId']+" not found."}) 
    else:
      patient = requests.get('https://dzsqyl-8080.preview.csb.app/patient/single/'+request.json['patientId'])
      if patient.text == "Patient with ID: "+request.json['patientId']+" not found.":
        return jsonify({"Message": "Patient with ID: "+request.json['patientId']+" not found."}) 
      else:
        all_Schedule = Schedule.query.filter(Schedule.userId == request.json['userId']).\
                                      filter(Schedule.scheduleStatus == "New").\
                                      filter(and_(request.json['scheduleFrom'] >= Schedule.scheduleFrom, request.json['scheduleFrom'] <= Schedule.scheduleTo)).\
                                      filter(and_(request.json['scheduleTo'] >= Schedule.scheduleFrom,request.json['scheduleTo'] <= Schedule.scheduleTo)).all()
        result = all_schedule_schema.dump(all_Schedule)
        if len(result):
          return jsonify({"Message": "Schedule not available.Please change time"}) 
        else:
          all_rooms = Schedule.query.filter(Schedule.roomNumber == request.json['location']).\
                                    filter(Schedule.scheduleStatus == "New").\
                                    filter(and_(request.json['scheduleFrom'] >= Schedule.scheduleFrom, request.json['scheduleFrom'] <= Schedule.scheduleTo)).\
                                    filter(and_(request.json['scheduleTo'] >= Schedule.scheduleFrom,request.json['scheduleTo'] <= Schedule.scheduleTo)).all()
          result = all_schedule_schema.dump(all_rooms)
          if len(result):
            return jsonify({"Message": "Room not available.Please change room number"}) 
          else:
            schedule.scheduleStatus = "Rescheduled"
            schedule.modifiedAt = datetime.date.today()
            db.session.commit()
            latestSchedule = Schedule.query.order_by(Schedule.id.desc()).first()
            id = latestSchedule.id + 1
            userId = request.json['userId']
            userName = request.json['userName']
            createdAt = datetime.date.today()
            modifiedAt = datetime.date.today()
            scheduleActivity = request.json['activity']
            providerGroup = request.json['providerGroup']
            scheduleStatus = request.json['scheduleStatus']
            scheduleDate = request.json['scheduleDate']
            scheduleFrom = request.json['scheduleFrom']
            scheduleTo = request.json['scheduleTo']
            patientId = request.json['patientId']
            roomNumber = request.json['location']
            new_Schedule = Schedule(id, userName,  createdAt, modifiedAt, scheduleActivity,providerGroup, scheduleStatus,scheduleDate, scheduleFrom, scheduleTo, userId, patientId, roomNumber)

            db.session.add(new_Schedule)
            db.session.commit()
            return jsonify({"Message": "User schedule updated successfully"}) 
  else:
    return jsonify({"Message": "Authentication Failed."}) 

@app.route("/schedule/userSchedule/<string:scheduleID>", methods = ['DELETE'])
def deleteUserSchedule(scheduleID):
  auth_Key = request.headers.get('Auth-Key', None)
  if auth_Key == "1qnf3kdo7jptk09logkr":
    schedule = Schedule.query.get(scheduleID)
    if schedule is None:
      return jsonify({"Message": "Invalid Schedule. Please select valid schedule."}) 
    else:
      schedule.scheduleStatus = "Cancelled"
      db.session.commit()
      return jsonify({"Message": "User schedule deleted successfully"}) 
  else:
    return jsonify({"Message": "Authentication Failed."}) 


if __name__ == "__main__":
    app.run(debug = True)
