from django.db import models
# Create your models here.
class laboratoryDetails(models.Model):
    Labid = models.AutoField(primary_key=True)
    labname = models.CharField(max_length=50)
    emailid = models.EmailField()
    password = models.CharField(max_length=10)
    labaddress = models.TextField()
    Contact_no = models.CharField(max_length=10)
    DoctorName = models.CharField(max_length=20)
    DoctorDegree = models.CharField(max_length=10)
    city = models.CharField(null=True,max_length=30)
    LabOpenTime = models.TimeField()
    LabCloseTime = models.TimeField()
    class Meta: 
        db_table = "LaboratoryDetail"  
    def __str__(self):
        return self.labname