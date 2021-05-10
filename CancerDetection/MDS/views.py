from django.shortcuts import render,HttpResponse

def home(request):
    ID = request.session['ID']
    return render(request, 'index.html', {'ID': ID})

