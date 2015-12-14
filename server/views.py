from django.shortcuts import render_to_response
import os
import commands
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import time

##################################
COMPILE_WORK_PATH = r"/home/projects/nw-packer/"
LOGO_PATH = COMPILE_WORK_PATH + "logo/"
##################################


class ImgForm(forms.Form):
    """
    A class for create a form to upload images
    """
    conp_name = forms.CharField(max_length=20, label="input company name")
    Img1 = forms.FileField(label="select Logo_big")
    Img2 = forms.FileField(label="select Logo")


class CompliForm(forms.Form):
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
        log("An error arise when rm temp : " + status4)
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
            cn = cn.strip()
            cn = cn.lower()
            if not cn.isalpha():
                return HttpResponse("Can not contain Chinese or digital, must be plain English")
            ig1 = imga.cleaned_data['Img1'].name
            ig2 = imga.cleaned_data['Img2'].name
            # print (ig1, ig2)
            if not (ig1 == "logo.png" or ig2 == "logo.png" and ig1 == "logo-big.png" or ig2 == "logo-big.png"):
                return HttpResponse("png name wrong")
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
            report = "upload photos ; Company name : " + cn
            log(report)
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
    getimage(li.split('\n'))
    err, list_version = git_tag_list()
    if err != 0:
        log(list_version)
        return HttpResponse(list_version)
    if requeset.method == "POST":
        compliform = CompliForm(requeset.POST)
        if 'compi' and 'choice' in requeset.POST:
            if compliform.is_valid():
                name = compliform.cleaned_data['conp_name']
                name = name.strip()
                name = name.lower()
                num = int(requeset.POST["choice"])
                err1, statu1 = git_checkout(list_version, num)
                if err1 != 0:
                    log(statu1)
                    return HttpResponse(statu1)
                logs = "change version : " + list_version[num]
                log(logs)
                statu = local_packing(name)
                if not statu:
                    clear_environment()
                    logs = "compiled successful and now begin the download.The Company name is: "+name
                    log(logs)
                    return HttpResponseRedirect(reverse('server.views.download_file_zip'))
                else:
                    clear_environment()
                    log(statu)
                    return HttpResponse(statu)
        elif 'add' in requeset.POST:
            return HttpResponseRedirect(reverse('server.views.uploadfile'))
        else:
            return render_to_response('home.html', {'list': li.split('\n'), 'compliform': compliform,
                                                    'version_list': list_version,
                                                    'error_message': "You didn't select any version"})
    else:
        compliform = CompliForm()
    return render_to_response('home.html', {'list': li.split('\n'), 'compliform': compliform,
                                            'version_list': list_version, 'error_message': "You must select a version"})


def local_packing(conp_name):
    """
    Do the compile and pack job in local
    """
    if os.getcwd() != r"/home/projects/nw-packer/":
        # os.getcwd()
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


def getimage(dir_list):
    """
    copy image to static direction.So it can show in the page.
    Improvement:
    check weather the image exists before copy it.
    """
    if os.getcwd() != r"/root/mysite/server/static/server":
        os.chdir(r"/root/mysite/server/static/server")
        if os.getcwd() != r"/root/mysite/server/static/server":
            return "Can change direction to the 'static'."
    """
    for comp in dir_list:
        err, status = commands.getstatusoutput(r"cp -i " + LOGO_PATH + comp + r"/logo.png " + comp + r".png")
        if err != 0:
            return "A error arise when copping image : " + status
        print comp, " done"
    return 0
    """
    d = dir_list
    # print len(dir_list)
    for n in range(len(d)):
        # print n
        err, status = commands.getstatusoutput(
            r"cp -f " + LOGO_PATH + dir_list[0] + r"/logo-big.png " + dir_list[0] + r".png")
        if err != 0:
            return "A error arise when copping image : " + status
        # print dir_list[0], " done"
        # print dir_list, type(dir_list)
        dir_list.pop(0)
        # print dir_list
    return 0


def git_tag_list():
    """
    get the version that can be use.
    """
    if os.getcwd() != r"/home/projects/zadmin":
        os.chdir(r"/home/projects/zadmin")
    if os.getcwd() != r"/home/projects/zadmin":
        return 1, r"Can't change direction to '/home/projects/zadmin'"
    err, statu1 = commands.getstatusoutput(r"git tag -l")
    if err != 0:
        return 2, r"A error arise when get tag list: " + statu1
    l = statu1.split("\n")
    return 0, l


def git_checkout(list_version, num):
    """
    checkout to the branch selected.
    """
    if os.getcwd() != r"/home/projects/zadmin":
        os.chdir(r"/home/projects/zadmin")
    if os.getcwd() != r"/home/projects/zadmin":
        return 1, r"Can't change direction to '/home/projects/zadmin'"
    try:
        list_version[num]
    except IndexError:
        return 2, r"A error arise: list index out of range."
    print r"git checkout " + "\"" + list_version[num] + "\""
    err1, statu1 = commands.getstatusoutput(r"git checkout " + "\"" + list_version[num] + "\"")
    if err1 != 0:
        return 3, r"A error arise when change branch: " + statu1
    return 0, "OK"


def clear_environment(conp_name="zexabox"):
    """
    replace all branch logo to zexabox.Ensure the error
    "error: Your local changes to the following files would be overwritten by checkout:
    images/logo-big.png
    images/logo.png
    Please, commit your changes or stash them before you can switch branches.
    Aborting"
    does no occur.
    """
    if os.getcwd() != r"/home/projects/nw-packer/":
        # os.getcwd()
        print os.getcwd()
        if os.chdir(r"/home/projects/nw-packer/"):
            # return HttpResponse("A error arise : can't change direction to /home/projects/nw-packer")
            return "An error arise : can't change direction to /home/projects/nw-packer/"
    err, status1 = commands.getstatusoutput(r'python /home/projects/nw-packer/replace_logo.py ' + conp_name)
    if err != 0:
        # return HttpResponse("A error arise when place logo : " + status1)
        return "An error arise when place logo : " + status1
    return 0


def log(string):
    sync_time()
    tm = time.asctime()
    fp = open(r"/root/mysite/server/log.txt", "a")
    try:
        logs = tm + " " + string + " \n"
        fp.write(logs)
    finally:
        fp.close()


def sync_time():
    if os.system("ntpdate 202.118.1.47"):
        return "Can't get time from ntp server."
    if os.system("hwclock -w"):
        return "Can't update time in BIOS."
    return 0