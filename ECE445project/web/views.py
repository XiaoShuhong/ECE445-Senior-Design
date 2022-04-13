from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def index(request):
    # return HttpResponse("hello world")
    return render(request,"Home.html")

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
        for chunk in file_content.chunks():     
            destination.write(chunk)  
        destination.close()
       
    except:
        print("error")
        
    return render(request,"upload_success.html")
    


def gallery_index(request):
    return render(request,"gallery_body.html")

    
    
# def upload_success(request):
#     return render(request,'update_success.html')



    
    
    