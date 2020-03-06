from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import csv
import pandas as pd
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request,'index.html')


def upload_csv(request):
    global fileurl
    if request.method == 'POST' or request.FILES['csv_file']:
        csv_file              = request.FILES['csv_file']
        fs                  = FileSystemStorage(location='files')
        filename            = fs.save(csv_file.name, csv_file)
        uploaded_file_url   = fs.url(filename)
        data = pd.read_csv('files/'+ uploaded_file_url)
        column = data.columns
        details = data.values
        fileurl = ('files/'+ uploaded_file_url)
        return render(request, 'index.html', {
            'data'             : column,
            'records'          : details
        })

def upload_csvrow(request):
    if request.method == 'POST':
        csv_col_names = request.POST.getlist('csv_col_names')
        data = pd.read_csv(fileurl, usecols=csv_col_names)
        column = data.columns
        details = data.values
        
        return render(request, 'upload_csv.html', {
            'data'             : column,
            'records'          : details
        })
        