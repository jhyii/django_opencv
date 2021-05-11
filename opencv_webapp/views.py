from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face

# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})

def simple_upload(request):
    if request.method == 'POST':
        #print(request.POST)
        #print(request.FILES)
        SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)

            uploaded_file_url = fs.url(filename)

            context = {'form':form, 'uploaded_file_url':uploaded_file_url}
            return render(request, 'opencv_webapp/simple_upload.html', context)


    else:
        form = SimpleUploadForm()
        context = {'form':form}
        return render(request, 'opencv_webapp/simple_upload.html', context)


def detect_face(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            imageURL = settings.MEDIA_URL + form.instance.document.name
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL)
            print('********************')
            print('form.instance : ', form.instance)
            print('form.instance.document : ', form.instance.document)
            print('form.instance.document.name : ', form.instance.document.name)
            print()
            print('settings.MEDIA_URL :', settings.MEDIA_URL)
            print('imageURL :', imageURL)
            context = {'form':form, 'post':post}
            return render(request, 'opencv_webapp/detect_face.html', context)
    else: # request.method == 'GET'
        form = ImageUploadForm()
        return render(request, 'opencv_webapp/detect_face.html', {'form':form})
