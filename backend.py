from flask import Flask,request,render_template,jsonify
from pymongo import MongoClient

client=MongoClient('127.0.0.1',27017)
db=client['train']
trainregcollection=db['trainreg']
donarcollection=db['donors']
enquirycollection=db['enquiry']

api=Flask(__name__)

@api.route('/register',methods=['GET'])
def register():
    Name=request.args.get('Name')
    Email=request.args.get('Email')
    Phone=request.args.get('Phone')
    Gender=request.args.get('Gender')
    Password=request.args.get('Password')
    
    data={}
    data['Name']=Name
    data['Email']=Email
    data['Phone']=Phone
    data['Gender']=Gender
    data['Password']=Password
    
    query={'Phone':Phone}
    for i in trainregcollection.find(query):
        return('account exist')
    trainregcollection.insert_one(data)
    return('data stored')

@api.route('/login',methods=['get'])
def login():
    UserID=request.args.get('UserID')
    Password=request.args.get('Password')
    query={'Phone':UserID}
    for i in trainregcollection.find(query):
        if (i['Password']==Password):
            return 'True'
    return 'False'
        
@api.route('/enquiry',methods=['get'])
def application_form():
    To=request.args.get('To')
    From=request.args.get('From')

    data={}
    data['To']=To
    data['From']=From
    query={'To':To,'From':From}
    for i in enquirycollection.find(query):
        return('already stored')
    enquirycollection.insert_one(data)
    return('data stored')

   
@api.route('/page',methods=['get'])
def requirement_page():
    Name=request.args.get('Name')
    Email=request.args.get('Email')
    BloodType=request.args.get('BloodType')
    Quantity=request.args.get('Quantity')
    Urgency=request.args.get('Urgency')
    RequirementDate=request.args.get('RequirementDate')
    AdditionalInformation=request.args.get('AdditionalInformation')

    data={}
    data['Name']=Name
    data['Email']=Email
    data['BloodType']=BloodType
    data['Quantity']=Quantity
    data['Urgency']=Urgency
    data['RequrirementDate']=RequirementDate
    data['AdditionalInformation']=AdditionalInformation
    query={'Email':Email,'RequrirementDate':RequirementDate}
    for i in enquirycollection.find(query):
        return('already stored')
    enquirycollection.insert_one(data)
    return('data stored')

@api.route('/trainbtw',methods=['get'])
def trainbtw():
    To=request.args.get('To')
    From=request.args.get('From')

    data={}
    data['Name']=To
    data['Email']=From
    query={'To':To,'From':From}

    for i in enquirycollection.find(query):
        return('already stored')
    enquirycollection.insert_one(data)
    return('data stored')

@api.route('/availablet')
def availablet():
    req=[]
    for i in enquirycollection.find():
        enres=[]
        enres.append(i['SNO'])
        enres.append(i['TO'])
        enres.append(i['FROM'])
        enres.append(i['DAY'])
        enres.append(i['TIME'])
        req.append(enres)
    return jsonify(req)

if __name__=="__main__":
    api.run(
        host='0.0.0.0',
        port=2000,
        debug=True
    )