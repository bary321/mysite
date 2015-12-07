from django.shortcuts import render_to_response
import os
import commands
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


class ImgForm(forms.Form):
    """
    A class for create a form to upload images
    """
    conp_name = forms.CharField(max_length=20, label="input company name")
    Img1 = forms.FileField(label="select Logo_big")
    Img2 = forms.FileField(label="select Logo")


class Compli_Form(forms.Form):
    """
    A class for create a form to input company name
    """
    conp_name = forms.CharField(max_length=20, label="input company name")


def download_file_zip(request):
    """
    download files
    """
    fp = open(r'/home/projects/bary/release/Zadmin.zip')
    data = fp.read()
    response = HttpResponse(data, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=Zadmin.zip'
    fp.close()
    err, status4 = commands.getstatusoutput(r"rm /home/projects/bary/release/Zadmin.zip")
    if err != 0:
        return HttpResponse("An error arise when rm temp : " + status4)
    return response


def uploadfile(request):
    """
    Upload company's logo and input company name
    """
    if request.method == "POST":
        imga = ImgForm(request.POST, request.FILES)
        if imga.is_valid():
            cn = imga.cleaned_data['conp_name']
            ig1 = imga.cleaned_data['Img1'].name
            ig2 = imga.cleaned_data['Img2'].name
            print (ig1, ig2)
            cmd = "cd /home/projects/nw-packer/logo && " + "mkdir " + cn
            # os.system("cd /home/projects/nw-packer/logo")
            if not os.system(cmd):
                print "make direction success"
            fp1 = open(r'/home/projects/nw-packer/logo/' + cn + '//' + ig1, 'wb')
            s = imga.cleaned_data["Img1"].read()
            fp1.write(s)
            fp1.close()
            fp2 = file(r'/home/projects/nw-packer/logo/' + cn + '//' + ig2, 'wb')
            s = imga.cleaned_data['Img2'].read()
            fp2.write(s)
            fp2.close()
            return HttpResponseRedirect(reverse('server.views.home'))
    else:
        imga = ImgForm()

    return render_to_response('uploadfile.html', {'imgfile': imga})


def home(requeset):
    """
    A function handle the page which should show first
    """
    # os.system("cd /home/projects/nw-packer/logo")
    err, li = commands.getstatusoutput('cd /home/projects/nw-packer/logo && ls ')
    # li.split('\n')
    if requeset.method == "POST":
        compliform = Compli_Form(requeset.POST)
        if 'compi' in requeset.POST:
            if compliform.is_valid():
                name = compliform.cleaned_data['conp_name']
                statu = local_packing(name)
                if not statu:
                    return HttpResponseRedirect(reverse('server.views.download_file_zip'))
                else:
                    return HttpResponse(statu)
        else:
            return HttpResponseRedirect(reverse('server.views.uploadfile'))
    else:
        compliform = Compli_Form()
    return render_to_response('home.html', {'list': li.split('\n'), 'compliform': compliform})


def local_packing(conp_name):
    """
    Do the compile and pack job in local
    """
    if os.getcwd() != r"/home/projects/nw-packer/":
        os.getcwd()
        print os.getcwd()
        if os.chdir(r"/home/projects/nw-packer/"):
            # return HttpResponse("A error arise : can't change direction to /home/projects/nw-packer")
            return "An error arise : can't change direction to /home/projects/nw-packer/"
    err, status1 = commands.getstatusoutput(r'python /home/projects/nw-packer/replace_logo.py ' + conp_name)
    if err != 0:
        # return HttpResponse("A error arise when place logo : " + status1)
        return "An error arise when place logo : " + status1
    else:
        err, status2 = commands.getstatusoutput(r"grunt | grep 'Done' ")
        if err != 0:
            # return HttpResponse("A error arise when compile: ", err)
            return "An error arise when compile: ", err
        if os.getcwd() != r"/home/projects/nw-packer/build/releases/Zadmin/win/":
            os.getcwd()
            print os.getcwd()
            if os.chdir(r"/home/projects/nw-packer/build/releases/Zadmin/win/"):
                # return HttpResponse("A error arise : can't change direction to /home/projects/nw-packer")
                return "An error arise when packing : can't change direction to \
                /home/projects/nw-packer/build/releases/Zadmin/win/"
        err, status3 = commands.getstatusoutput(r"zip -r /home/projects/bary/release/Zadmin.zip ./Zadmin/")
        if err != 0:
            # return HttpResponse("A error arise when packing: " + status3)
            return "An error arise when packing: " + status3
        return 0
