from django.contrib import admin
from .models import addpatientform,generatereport,Hospital,Feedback
# Register your models here.
admin.site.register(addpatientform)
admin.site.register(generatereport)
admin.site.register(Hospital)
admin.site.register(Feedback)