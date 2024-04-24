import os
import time
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import MyFileUpload, FileHash
import hashlib

# Create your views here.

def index(request):
    files_obj = MyFileUpload.objects.filter(user=request.user.id).order_by('file_name')
    context = {'files': files_obj}
    return render(request, 'main/home.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
        return HttpResponse('form is invalid')
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)


@login_required(login_url='/login')
def file_upload(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file[]')
        files_name_list=[]
        for file in files:
            # print(file.name)
            md5 = hashlib.md5()
            files_name_list.append(file.name)

            for chunk in file.chunks():
                md5.update(chunk)
            file_hash = md5.hexdigest()

            if MyFileUpload.objects.filter(user_id=request.user.id, file_hash=file_hash).exists():
                messages.error(request, f'file {file.name} already exists')

            else:
                user = User.objects.get(username=request.user.username)

                exists = MyFileUpload.objects.filter(file_hash=file_hash).exists()

                if exists:
                    obj = MyFileUpload.objects.filter(file_hash=file_hash).first()
                    MyFileUpload.objects.create(user=user, file_name=file.name, file_hash=file_hash, file=obj.file)

                    try:
                        obj = FileHash.objects.get(file_hash=file_hash)
                        obj.count += 1
                        obj.save()
                    except:
                        pass
                else:
                    MyFileUpload.objects.create(user=user, file_name=file.name, file_hash=file_hash,
                                                file=file)
                    FileHash.objects.create(file_hash=file_hash)

        file_names = f'File names: {files_name_list}'
        formatted_time = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H-%M-%S')
        time_of_upload = f'Time of upload: {formatted_time}'

        subject = f'File upload succesful'
        message = f'{file_names}\n{time_of_upload}'
        sender = 'sivagnanasankar2003@gmail.com'
        recipient = [f'{request.user.email}']

        send_mail(subject, message, sender, recipient)

        return redirect('index')

    return render(request, 'main/file_upload.html')


@login_required(login_url='/login')
def delete_file(request, id):
    obj = MyFileUpload.objects.get(id=id)

    file_name = f'File name: {obj.file_name}'
    formatted_time = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H-%M-%S')
    time_of_deletion = f'Time of deletion: {formatted_time}'

    subject = f'File deleted succesfully'
    message = f'{file_name}\n{time_of_deletion}'
    sender = 'sivagnanasankar2003@gmail.com'
    recipient = [f'{request.user.email}']

    file_hash_obj = FileHash.objects.get(file_hash=obj.file_hash)
    if file_hash_obj.count == 1:
        os.remove(obj.file.path)
        file_hash_obj.delete()
    else:
        file_hash_obj.count -= 1
        file_hash_obj.save()
    obj.delete()

    send_mail(subject, message, sender, recipient)

    return redirect('index')


@login_required(login_url='/login')
def download_file(request, id):
    file_obj = MyFileUpload.objects.get(id=id)
    file_path = file_obj.file.path
    response = FileResponse(open(file_path, 'rb'))

    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_obj.file.name)
    #  'attachment; filename="myname"' it is the name provided when the file is downloading
    return response



def logout1(request):
    logout(request)
    return redirect('index')
