from django.db import models
# database 
# Create your models here.
class addpatientform(models.Model):
    Patientid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    contact = models.CharField(max_length=25)
    gender = models.CharField(max_length=25)
    bloodgroup = models.CharField(max_length=25)
    age = models.CharField(max_length=3)
    RefBy = models.CharField(max_length=20)
    address = models.TextField()
    labid = models.CharField(max_length=3)
    class Meta: 
        db_table = "AddPatient"  
    def __str__(self):
        return str(self.Patientid)

class generatereport(models.Model):
    patientid = models.AutoField(primary_key=True)
    patientname = models.CharField(max_length=25)
    isreportgenerated = models.BooleanField(default=False)
    labid= models.CharField(max_length=3)
    image = models.ImageField(upload_to="image")
    report = models.FileField(upload_to="pdf")
    result = models.CharField(max_length=25,default="")
    Date = models.DateField(null=True)
    class Meta: 
        db_table = "GenerateReport"  
    def __str__(self):
        return str(self.patientid)

class Hospital(models.Model):
    city = models.CharField(max_length=30)
    hospital = models.CharField(max_length=500)
    website = models.CharField(max_length=500)
    class Meta: 
        db_table = "Hospital"  
    def __str__(self):
        return str(self.city)

class Feedback(models.Model):
    LabName = models.CharField(max_length=25)
    Emailid = models.CharField(max_length=25)
    Description=models.TextField()
    Address = models.TextField()

    class Meta:
        db_table = "Feedback"
