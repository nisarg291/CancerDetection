from django.shortcuts import render,HttpResponse,redirect
from .models import addpatientform,generatereport,Hospital,Feedback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.template.loader import get_template
from .utils import render_to_pdf
from django.core.files import File
from io import BytesIO
from login.models import laboratoryDetails
import datetime
from MDS import settings
from django.core.mail import EmailMessage
#from sklearn.preprocessing import LabelEncoder
import keras,cv2
mymodel=keras.models.load_model("cancer_model.h5")

def home(request):
  labid = request.session["ID"]
  generatereports = generatereport.objects.filter(isreportgenerated = False,labid=labid)
  if generatereports:
    return render(request, "generatereport.html",{'generatereport':generatereports})
  else:
    return render(request, "generatereport.html")

def detect(request):
    #get image from html and read
    Image = request.FILES['img'].read()
    #convert into format which is readable by opencv
    npimg = np.fromstring(Image, np.uint8)
    #converting into grayscale image
    grayScale_img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
    #resizing into 50X50
    resized_img=cv2.resize(grayScale_img,dsize=(50,50)) 
    #converting it into numpy array 
    np_arr=np.array(resized_img)
    #Pre processing step -> Normalization
    n_arr=np_arr.reshape(1,50,50,1).astype(float)
    n_arr=n_arr/255.0
    #predication printing on console
    print("Predicted", mymodel.predict([[n_arr.reshape(1,50,50,1)]]).astype(float))
    #Pridiction assigning into one variable and printing it on console which is in form of matrix
    prediction=mymodel.predict([[n_arr.reshape(1,50,50,1)]]).astype(float)
    #print((prediction[0][0]-prediction[0][1])*100)
    #prediction Logic
    if prediction.argmax()==0:
      print("Predicted image=Parasitised")
      patientid = request.POST.get('id',"")
      generatereport.objects.filter(patientid=patientid).update(isreportgenerated=True)
      generatereport.objects.filter(patientid=patientid).update(result="positive")
      obj = generatereport.objects.get(patientid=patientid)
      patient = addpatientform.objects.get(Patientid=patientid)
      labid = patient.labid
      lab = laboratoryDetails.objects.get(Labid=labid)
      city = lab.city
      rs = Hospital.objects.get(city=city).hospital
      ws = Hospital.objects.get(city=city).website
      rs = rs.split(", ")
      ws = ws.split(", ")
      
      context = {
          'labname':lab.labname ,
          'doctorname':lab.DoctorName ,
          'doctordegree':lab.DoctorDegree ,
          'address':lab.labaddress ,
          'contact':lab.Contact_no ,
          'open':lab.LabOpenTime ,
          'close':lab.LabCloseTime ,
          'email':lab.emailid ,
          'patientname': patient.firstname + " " + patient.lastname ,
          'age' : patient.age ,
          'gender' : patient.gender ,
          'ref' : patient.RefBy,
          'date' : datetime.date.today(),
          'result': obj.result,
          'rs' : rs ,
          'ws' : ws

      }
      pdf = render_to_pdf('report.html',context)
      filename = patientid + ".pdf" 
      obj.report.save(filename, File(BytesIO(pdf.content)))
      report = obj.report.file.name
      subject = patientid + " Cancer Report"
      to      = patient.email  
      email = EmailMessage(subject,"Report",'cancerdetectionsystem@gmail.com',[to])
      email.attach_file(report)
      email.send()      
      return render(request,'report.html',context)
      
    else:
      print("Predicted image=Uninfected")
      
      patientid = request.POST.get('id',"")

      generatereport.objects.filter(patientid=patientid).update(isreportgenerated=True)
      generatereport.objects.filter(patientid=patientid).update(result="Negative")
      obj = generatereport.objects.get(patientid=patientid)
      patient = addpatientform.objects.get(Patientid=patientid)
      labid = patient.labid
      lab = laboratoryDetails.objects.get(Labid=labid)
    
      context = {
          'labname':lab.labname ,
          'doctorname':lab.DoctorName ,
          'doctordegree':lab.DoctorDegree ,
          'address':lab.labaddress ,
          'contact':lab.Contact_no ,
          'open':lab.LabOpenTime ,
          'close':lab.LabCloseTime ,
          'email':lab.emailid ,
          'patientname': patient.firstname + " " + patient.lastname ,
          'age' : patient.age ,
          'gender' : patient.gender ,
          'ref' : patient.RefBy,
          'date' : datetime.date.today(),
          'result': obj.result

      }
      pdf = render_to_pdf('report.html',context)
      filename = patientid + ".pdf" 
      obj.report.save(filename, File(BytesIO(pdf.content)))
      report = obj.report.file.name
      subject = patientid + "Cancer Report"
      to      = patient.email  
      email = EmailMessage(subject,"Report",'cancerdetectionsystem@gmail.com',[to])
      email.attach_file(report)
      email.send()      
      return render(request,'report.html',context)
      return HttpResponse("Predicted image=Uninfected")
# Create your views here.
def addpatient(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname =  request.POST['lastname']
        email = request.POST['email']
        contact = request.POST['contact']
        gender = request.POST['gender']
        bloodgroup = request.POST['bloodgroup']
        age = request.POST['age']
        refby = request.POST['ref']
        Address = request.POST['address']
        labid = request.session['ID']
        add_patient = addpatientform(firstname=firstname,lastname=lastname,email=email,contact=contact,gender=gender,bloodgroup=bloodgroup,age=age,RefBy=refby,address=Address,labid=labid)
        generate_report = generatereport(patientname=firstname,labid=labid)
        add_patient.save()
        generate_report.save()
        return redirect('home')
    return render(request,'signup.html')

def userdetail(request):
  labid = request.session["ID"]
  rs = addpatientform.objects.all().filter(labid=labid)
  gs = generatereport.objects.all().filter(labid=labid)
  
  print(rs)
  return render(request,'userdetail.html',{'rs':zip(rs,gs)}) 

def feedback(request):
    if request.method == "POST":
        LabName = request.POST['LabName']
        Emailid = request.POST['Emailid']
        Description = request.POST['Description']
        Address= request.POST['Address']
        feedback_form = Feedback(LabName=LabName,Emailid=Emailid,Description=Description,Address=Address)
        feedback_form.save()
    return render(request,'feedback.html')

def logout(request):
    del request.session['ID']
    return redirect('/')