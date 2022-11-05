from flask import Flask,jsonify

app = Flask(__name__)




@app.route("/schedule/currentDaySchedule", methods = ['GET'])
def getCurrentDaySchedule():
    return jsonify({
  "schedules": {
    "userName": "Varun Ignatius",
    "providerGroup": "Doctor",
    "schedule": {
      "scheduleTime": "2022-11-02T18:36:13.593Z",
      "activity": "Patient visit"
    }
  }
},
{
  "schedules": {
    "userName": "Daniel",
    "providerGroup": "Doctor",
    "schedule": {
      "scheduleTime": "2022-11-02T12:46:13.593Z",
      "activity": "Patient visit"
    }
  }
})

@app.route("/schedule/monthlySchedule/<string:month>", methods = ['GET'])
def getMonthlySchedule(month):
    return jsonify({
  "date": "2022-01-01",
  "dateWiseSchedule": {
    "schedules": {
      "userName": "Varun Ignatius",
      "providerGroup": "Doctor",
      "schedule": {
        "scheduleTime": "2022-01-01T18:44:01.358Z",
        "activity": "Patient visit"
      }
    }
  }
},
{
  "date": "2022-01-02",
  "dateWiseSchedule": {
    "schedules": {
      "userName": "Varun Ignatius",
      "providerGroup": "Doctor",
      "schedule": {
        "scheduleTime": "2022-01-02T18:44:01.358Z",
        "activity": "Patient visit"
      }
    }
  }
})

@app.route("/schedule/userSchedule/<string:userId>", methods = ['GET'])
def getUserSchedule(userId):
    return jsonify({
  "userName": "Varun Ignatius",
  "providerGroup": "Doctor",
  "schedule": {
    "scheduleTime": "2022-11-02T19:03:59.053Z",
    "activity": "Patient visit"
  }
})


@app.route("/schedule/newUserSchedule", methods = ['POST'])
def addNewUserSchedule():
  return "User schedule added successfully"

@app.route("/schedule/userSchedule", methods = ['PUT'])
def updateUserSchedule():
  return "User schedule updated successfully"

@app.route("/schedule/userSchedule/<string:userId>&<string:scheduleTime>", methods = ['DELETE'])
def updateUserSchedule():
  return "User schedule deleted successfully"





if __name__ == "__main__":
    app.run(debug = True)
