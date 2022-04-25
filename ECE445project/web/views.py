from re import L
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def index(request):
    # return HttpResponse("hello world")
    return render(request,"Home.html")
############################################
#upload

def upload_clothes_index(request):
    return render(request,"upload_clothes.html")

def do_upload(request):
    try:
        file=request.POST.get("filename",None)
        file_content=request.FILES.get("file_content")
        # print(file_content)
        if not file_content:
             return render(request,"upload_fail.html")
        destination = open("./static/user_upload/"+file+".jpg","wb+")
        file_scr = "/static/user_upload/"+file+".jpg"
        for chunk in file_content.chunks():     
            destination.write(chunk)  
        destination.close()
        context={"file_scr":file_scr}
    except:
        print("error")
        
    return render(request,"upload_success.html",context)
def comfirm_category(request,category):
    print(category)
    return HttpResponse("store upload "+category)
###############################################
#gallery

def gallery_index(request,catename='Blazer',pidx=1):
    context = {'pidx':pidx,'catename':catename}
    return render(request,"gallery.html",context)

def change_cate(request,catename='Blazer',pidx=1):
    print(catename)
    print(pidx)
    print(request)
    context = {'pidx':pidx,'catename':catename}
    return render(request,"gallery.html",context)







#################################################
#recommendation
def recom_index(request):
    return render(request,"recommedation.html")

def generate_outfit(request,style):
    context={"style":style}
    return render(request,"outfit_display.html",context)
    

    
    
# def upload_success(request):
#     return render(request,'update_success.html')



    
    
    