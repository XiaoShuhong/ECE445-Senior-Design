from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
import requests
import time
import random 
from web.models import hanger,img_info,bind
from threading import Thread
from django.core.paginator import Paginator

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
        #get the uploaded image
        file=request.POST.get("filename",None)
        file_content=request.FILES.get("file_content")
        if not file_content:
            return render(request,"upload_fail.html")
        #run the recognition model, get the three category candidates
        category_list = ['Blazer','Blouse','Coat','Hoodie','Jacket','Parka','Sweater','Tank','Tee','Chinos','Culottes','Cutoffs','Jeans','Jeggings','Joggers','Shorts','Skirt','Dress','Romper']
        random.shuffle(category_list)
        candidate1 = category_list[0]
        candidate2 = category_list[1]
        candidate3 = category_list[2]
        print(candidate1,candidate2,candidate3)
        #store the image
        destination = open("./static/user_upload/"+file+".jpg","wb+")
        file_scr = "/static/user_upload/"+file+".jpg"
        for chunk in file_content.chunks():     
            destination.write(chunk)  
        destination.close()
        
        # pass context to html
        context={"file_scr":file_scr,"candidate1":candidate1,"candidate2":candidate2,"candidate3":candidate3,"filename":file}
    except:
        print("error")
        
    return render(request,"upload_success.html",context)
def comfirm_category(request,category,filename):
    
    tops=['Blouse','Hoodie','Sweater','Tank','Tee']
    outerwear=['Blazer','Coat','Jacket','Parka',]
    bottoms=['Chinos','Culottes','Cutoffs','Jeans','Jeggings','Joggers','Shorts','Skirt']
    all_body=['Dress','Romper']
    try:
        #create img_info 
        ob1 = img_info()
        ob1.img_name = filename
        ob1.img_content = "/static/user_upload/"+filename+".jpg"
        ob1.img_category = category
        ob1.img_attributes = ''
        ob1.save()
        #create image_hanger binding
        ob2 = bind()
        if category in tops:
            hanger_id =1
        elif category in outerwear:
            hanger_id =2
        elif category in bottoms:
            hanger_id =3
        else:
            hanger_id =4
        ob2.is_bind = 1
        ob2.img_id = img_info.objects.get(img_name=filename).img_id
        ob2.hanger_id = hanger_id
        ob2.img_name = filename
        ob2.save()
        #call the hanger to have the clothes placed
        # hanger_address = hanger.objects.get(hanger_id=hanger_id).hanger_address
        # new_event=Thread(target=call_hanger_light_on,args=(hanger_address,))
        # new_event.start()

        
        # print(category)
        # print(filename)
    except:
        pass
     
    # return HttpResponse("store upload "+category+'\n'+ 'hanger 3c is binded.')
    return render(request,"Home.html")
def call_hanger_light_on(hanger_address):
    resp_on=requests.get(hanger_address)
    time.sleep(5)
    hanger_address2 = hanger_address.split('/')
    hanger_address2[-1] = '0'
    hanger_address2 = ''.join(hanger_address2)
    resp_off=requests.get(hanger_address2)
    return 
    
    
    
# def finish_bind(request):
#     hanger_address="http://172.20.10.6/gpio/0"
#     try:
#         resp=requests.get(hanger_address)
#     except:
#         pass
#     return render(request,"Home.html")
###############################################
#gallery

def gallery_index(request,catename='Blazer',pidx=1):
    img_list1 = img_info.objects.filter(img_category=catename)
    img_list2 = []
    for i in range(len(img_list1)-1,-1,-1):
        img_list2.append(img_list1[i])
    pidx = int(pidx)
    page = Paginator(img_list2,8) 
    maxpages = page.num_pages 
    if pidx > maxpages:
        pidx = maxpages
    if pidx < 1:
        pidx = 1
    imgthispage = page.page(pidx) 
    print(imgthispage[0].img_content)
    pagerange = page.page_range 
    context = {'pidx':pidx,'catename':catename, 'imglist':imgthispage,'pagerange':pagerange}
    return render(request,"gallery.html",context)

def change_cate(request,catename='Blazer',pidx=1):
    img_list1 = img_info.objects.filter(img_category=catename)
    img_list2 = []
    for i in range(len(img_list1)-1,-1,-1):
        img_list2.append(img_list1[i])
    pidx = int(pidx)
    page = Paginator(img_list2,8) 
    maxpages = page.num_pages 
    if pidx > maxpages:
        pidx = maxpages
    if pidx < 1:
        pidx = 1
    imgthispage = page.page(pidx) 
    print(imgthispage[0].img_content)
    pagerange = page.page_range 
    context = {'pidx':pidx,'catename':catename, 'imglist':imgthispage,'pagerange':pagerange}
    return render(request,"gallery.html",context)







#################################################
#recommendation
def recom_index(request):
    
    return render(request,"recommedation.html")

def generate_outfit(request,style,weather):
    ##get the temperature and weather for haining from the web
    weather_add='http://d1.weather.com.cn/sk_2d/101210303.html?_=1651149854826'
    headers={
    "User-Agent": 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Referer": 
        "http://www.weather.com.cn/"
}
    resp=requests.get(weather_add,headers=headers)
    resp.encoding='utf-8'
    list = resp.text
    temp_idx1=list.index("temp")+7
    temp_idx2=list.index("tempf")-3
    temp = int(list[temp_idx1:temp_idx2])
    wcode_idx1=list.index("weathercode")+14
    wcode_idx2=list.index("limitnumber")-3
    wcode=list[wcode_idx1:wcode_idx2]
    if temp<10:
        weather='cold'
    elif temp<25:
        weather='mild'
    else:
        weather='hot'
    print(weather)
    print(temp)
    print(style)
    context={"temp":temp,'wcode':wcode,'weather':weather, 
             "outfit1a":'/static/images/empty.png', "outfit1b":'/static/images/empty.png', "outfit1c":'/static/images/empty.png', 
             "outfit2a":'/static/images/empty.png', "outfit2b":'/static/images/empty.png', "outfit2c":'/static/images/empty.png', 
             "outfit3a":'/static/images/empty.png', "outfit3b":'/static/images/empty.png', "outfit3c":'/static/images/empty.png', 
             'img1':'',
             'img2':'',
             'img3':''
             }
    ##pass the weather and style to our recommendation model and get 3 group of outfit
    image_list = img_info.objects.all()
    img1 = []
    img2 = []
    img3 = []
    
    num = random.randint(2,3)
    idx = random.randint(0,len(image_list))
    img_content = image_list[idx].img_content
    context['outfit1a'] = img_content
    img1.append(str(idx))
    idx = random.randint(0,len(image_list))
    img_content = image_list[idx].img_content
    context['outfit1b'] = img_content
    img1.append(str(idx))
    if num ==3:
        idx = random.randint(0,len(image_list))
        img_content = image_list[idx].img_content
        context['outfit1c'] = img_content
        img1.append(str(idx))
        
    
    num = random.randint(2,3)
    idx = random.randint(0,len(image_list))
    img_content = image_list[idx].img_content
    context['outfit2a'] = img_content
    img2.append(str(idx))
    idx = random.randint(0,len(image_list))
    img_content = image_list[idx].img_content
    context['outfit2b'] = img_content
    img2.append(str(idx))
    if num ==3:
        idx = random.randint(0,len(image_list))
        img_content = image_list[idx].img_content
        context['outfit2c'] = img_content
        img2.append(str(idx))
        
    
    num = random.randint(2,3)
    idx = random.randint(0,len(image_list))
    img_content = image_list[idx].img_content
    context['outfit3a'] = img_content
    img3.append(str(idx))
    idx = random.randint(0,len(image_list))
    img_content = image_list[idx].img_content
    context['outfit3b'] = img_content
    img3.append(str(idx))  
    if num ==3:
        idx = random.randint(0,len(image_list))
        img_content = image_list[idx].img_content
        context['outfit3c'] = img_content
        img3.append(str(idx))
        
    context['img1'] = str('-'.join(img1))
    context['img2'] = str('-'.join(img2))
    context['img3'] = str('-'.join(img3))
    # print(context)    
    ##
    
    
    return render(request,"outfit_display.html",context)
    
def call_hanger(request,imgid):
    #find the hanger address
    idlist = imgid.split('-')
    for id in idlist:
        imgid = int(id)
        hangerid = bind.objects.get(img_id=imgid).hanger_id
        hanger_address = hanger.objects.get(hanger_id=hangerid).hanger_address
    #call the hanger to light on 
    
        try:
        # new_event=Thread(target=call_hanger_light_on,args=(hanger_address,))
        # new_event.start()
            print(hanger_address)
            
        except:
            pass
    return render(request,"Home.html")
    
    
# def upload_success(request):
#     return render(request,'update_success.html')



    
    
    