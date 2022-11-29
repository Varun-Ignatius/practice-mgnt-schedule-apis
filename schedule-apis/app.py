import calendar
import datetime
from operator import and_
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import extract

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://49ken39w43vjxx7wo25d:pscale_pw_fWPEnRBxGKxtPiHrCtxWBHQCjUNQP8lUkaWg1Vw3yga@us-east.connect.psdb.cloud/schedule?ssl=true'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db= SQLAlchemy(app)

ma = Marshmallow(app)

class Schedule(db.Model):
  scheduleId = db.Column(db.Integer, primary_key = True)
  userName = db.Column(db.String(255))
  scheduleActivity = db.Column(db.String(255))
  providerGroup = db.Column(db.String(255))
  scheduleStatus = db.Column(db.String(255))
  scheduleDate = db.Column(db.Date)
  scheduleFrom = db.Column(db.DateTime)
  scheduleTo = db.Column(db.DateTime)
  userId = db.Column(db.Integer)
  patientId = db.Column(db.Integer)
  roomNumber = db.Column(db.Integer)


  def __init__(self, scheduleId, userName, scheduleActivity, providerGroup,scheduleStatus, scheduleDate, scheduleFrom, scheduleTo, userId, patientId, roomNumber):
    self.scheduleId = scheduleId
    self.userName = userName
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
    fields = ('userName', 'scheduleActivity', 'scheduleDate', 'scheduleFrom', 'scheduleTo', 'roomNumber', 'scheduleStatus', 'scheduleId', 'userId', 'patientId')

schedule_Schema = ScheduleSchema()
all_schedule_schema = ScheduleSchema(many = True)

@app.route("/schedule/currentDaySchedule", methods = ['GET'])
def getCurrentDaySchedule():
  all_Schedule = Schedule.query.filter_by(scheduleDate=datetime.date.today()).all()
  result = all_schedule_schema.dump(all_Schedule)
  print(result)
  return jsonify(result)

@app.route("/schedule/monthlySchedule/<string:month>", methods = ['GET'])
def getMonthlySchedule(month):
  num_days = calendar.monthrange(int(month[:4]), int(month[5:7]))[1]
  start_date = datetime.date(int(month[:4]), int(month[5:7]), 1)
  end_date = datetime.date(int(month[:4]), int(month[5:7]), num_days)
  all_Schedule = Schedule.query.filter(and_(Schedule.scheduleDate >= start_date, Schedule.scheduleDate <= end_date)).all()
  result = all_schedule_schema.dump(all_Schedule)
  print(result)
  return jsonify(result)

@app.route("/schedule/userSchedule/<string:userID>", methods = ['GET'])
def getUserSchedule(userID):
  all_Schedule = Schedule.query.filter_by(userId=userID, scheduleDate=datetime.date.today()).all()
  result = all_schedule_schema.dump(all_Schedule)
  print(result)
  return jsonify(result)


@app.route("/schedule/newUserSchedule", methods = ['POST'])
def addNewUserSchedule():
  scheduleId = request.json['scheduleId']
  userId = request.json['userId']
  userName = request.json['userName']
  scheduleActivity = request.json['activity']
  providerGroup = request.json['providerGroup']
  scheduleStatus = request.json['scheduleStatus']
  scheduleDate = request.json['scheduleDate']
  scheduleFrom = request.json['scheduleFrom']
  scheduleTo = request.json['scheduleTo']
  patientId = request.json['patientId']
  roomNumber = request.json['location']
  new_Schedule = Schedule(scheduleId, userName, scheduleActivity, providerGroup, scheduleStatus,scheduleDate, scheduleFrom, scheduleTo, userId, patientId, roomNumber)

  db.session.add(new_Schedule)
  db.session.commit()

  return "User schedule added successfully"

@app.route("/schedule/userSchedule/<string:schID>", methods = ['PUT'])
def updateUserSchedule(schID):
  schedule = Schedule.query.get(schID)
  schedule.scheduleStatus = "Rescheduled"
  db.session.commit()

  scheduleId = request.json['scheduleId']
  userId = request.json['userId']
  userName = request.json['userName']
  scheduleActivity = request.json['activity']
  providerGroup = request.json['providerGroup']
  scheduleStatus = request.json['scheduleStatus']
  scheduleDate = request.json['scheduleDate']
  scheduleFrom = request.json['scheduleFrom']
  scheduleTo = request.json['scheduleTo']
  patientId = request.json['patientId']
  roomNumber = request.json['location']
  new_Schedule = Schedule(scheduleId, userName, scheduleActivity, providerGroup, scheduleStatus,scheduleDate, scheduleFrom, scheduleTo, userId, patientId, roomNumber)

  db.session.add(new_Schedule)
  db.session.commit()
  return "User schedule updated successfully"

@app.route("/schedule/userSchedule/<string:scheduleID>", methods = ['DELETE'])
def deleteUserSchedule(scheduleID):
  schedule = Schedule.query.get(scheduleID)
  schedule.scheduleStatus = "Cancelled"
  db.session.commit()
  return "User schedule deleted successfully"





if __name__ == "__main__":
    app.run(debug = True)
