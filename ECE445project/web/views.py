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
from web import recommendation_model as recom_model

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
        # print(candidate1,candidate2,candidate3)
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
    # print(imgthispage[0].img_content)
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
    # print(imgthispage[0].img_content)
    pagerange = page.page_range 
    context = {'pidx':pidx,'catename':catename, 'imglist':imgthispage,'pagerange':pagerange}
    return render(request,"gallery.html",context)





def get_weather():
    weather_add='http://d1.weather.com.cn/sk_2d/101210303.html?_=1651806576347'
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
    # print(temp)
    return weather

#################################################
#recommendation
def recom_index(request):
    weather = get_weather()
    # print(weather)
    context = {"user_style":[], "weather":weather}
    for i in range(len(recom_model.get_user_define("style_name"))):
        one = dict()
        one["Style_Name"] = recom_model.get_user_define("style_name")[i]
        one["backimg"] = recom_model.get_user_define("backimg")[i]
        one["id"] = recom_model.get_user_define('id')[i]
        style_ava = recom_model.get_user_define('style_avaliable')
        one['cold_ava'] = style_ava[i*3]
        one['mild_ava'] = style_ava[i*3+1]
        one['hot_ava'] = style_ava[i*3+2]
        context["user_style"].append(one)
    for e in context["user_style"]:
        print(e["Style_Name"])
    
    
    
    # context={"style_name":recom_model.get_user_define["Style_Name"],"backimg":recom_model.get_user_define["backimg"]}
    return render(request,"recommedation.html",context)

def add_new_style(request):
    # value = recom_model.get_value()
    try:
        style_name = request.POST.get("Style_Name",None)
        recom_model.add_user_define('style_name',style_name)
        bkg_img = "/static/images/self-define.jpg"
        recom_model.add_user_define('backimg',bkg_img)
        id = style_name
        recom_model.add_user_define('id',id)
        for _ in range(3):
            recom_model.add_user_define('style_avaliable','false')
        
    except:
        pass
    # context = {"style_name":recom_model.get_user_define["Style_Name"],"backimg":recom_model.get_user_define["backimg"]}
    # print(value)
    return recom_index(request)
    
def write_style(request,style,weather_type):
    print(style)
    context = {"style":style,"weather_type":weather_type}
    return render(request,"write_style.html",context)
def write_style2(request,style,weather_type,outfit_type):
    recom_model.init_write_style()
    outfit_type = int(outfit_type)
    tops=['Blouse','Hoodie','Sweater','Tank','Tee']
    outerwear=['Blazer','Coat','Jacket','Parka',]
    bottoms=['Chinos','Culottes','Cutoffs','Jeans','Jeggings','Joggers','Shorts','Skirt']
    all_body=['Dress','Romper']
    top_list = []
    bot_list = []
    out_list = []
    all_list = []
    for e in tops:
        toplist=img_info.objects.filter(img_category=e)
        seq1 = get_random_seq(len(toplist))
    for e in bottoms:
        botlist=img_info.objects.filter(img_category=e)
        seq2 = get_random_seq(len(botlist))
    for e in outerwear:
        outlist=img_info.objects.filter(img_category=e)
        seq3 = get_random_seq(len(outlist))
    for e in all_body:
        alllist=img_info.objects.filter(img_category=e)
        seq4 = get_random_seq(len(alllist))
    
    if outfit_type == 1:
        for i in seq1:
            top_list.append(toplist[i])
            recom_model.add_user_define('temp_container1',toplist[i].img_name)
       
        for i in seq2:
            bot_list.append(botlist[i])
            recom_model.add_user_define('temp_container2',botlist[i].img_name)
        
        context={"container1":top_list,"container2":bot_list,"style":style,"weather_type":weather_type,"outfit_type":outfit_type}
    elif outfit_type == 2: 
        for i in seq1:
            top_list.append(toplist[i])
            recom_model.add_user_define('temp_container1',toplist[i].img_name)
        for i in seq2:
            bot_list.append(botlist[i])
            recom_model.add_user_define('temp_container2',botlist[i].img_name)
        for i in seq3:
            out_list.append(outlist[i])
            recom_model.add_user_define('temp_container3',outlist[i].img_name)
        context={"container1":top_list,"container2":bot_list,"container3":out_list,"style":style,"weather_type":weather_type,"outfit_type":outfit_type}
    elif outfit_type == 3:
        for i in seq4:
            all_list.append(alllist[i])
            recom_model.add_user_define('temp_container1',alllist[i].img_name)
        context={"container1":all_list,"style":style,"weather_type":weather_type,"outfit_type":outfit_type}
    else:
        for i in seq3:
            out_list.append(outlist[i])
            recom_model.add_user_define('temp_container1',outlist[i].img_name)
        for i in seq4:
            all_list.append(alllist[i])
            recom_model.add_user_define('temp_container2',alllist[i].img_name)
        context={"container1":all_list,"container2":out_list,"style":style,"weather_type":weather_type,"outfit_type":outfit_type}
    # print(weather_type)
    # print(style)
    return render(request,"write_style2.html",context)

def get_random_seq(n):
    i = 0
    seq = []
    while i<12:
        idx = random.randint(0,n)
        if idx not in seq:
            seq.append(idx)
            i+=1
    return seq
        
def finish_write_style(request,style,weather_type,outfit_type):
    # print(style)
    # print(weather_type)
    # print(outfit_type)
    outfit_type = int(outfit_type)
    top_list = []
    bot_list = []
    out_list = []
    all_list = []
    if outfit_type == 1:
        tops = recom_model.get_user_define('temp_container1')
        for e in tops:
            status=request.POST.get(e,None)
            if status!= None:
                top_list.append(e)
        bot = recom_model.get_user_define('temp_container2')
        for e in bot:
            status=request.POST.get(e,None)
            if status!= None:
                bot_list.append(e)
        print(top_list)
        print(bot_list)
    elif outfit_type == 2: 
        tops = recom_model.get_user_define('temp_container1')
        for e in tops:
            status=request.POST.get(e,None)
            if status!= None:
                top_list.append(e)
        bot = recom_model.get_user_define('temp_container2')
        for e in bot:
            status=request.POST.get(e,None)
            if status!= None:
                bot_list.append(e)
        outw =  recom_model.get_user_define('temp_container3')
        for e in outw:
            status=request.POST.get(e,None)
            if status!= None:
                out_list.append(e)
        print(top_list)
        print(bot_list)
        print(out_list)
        
    elif outfit_type == 3: 
        alllist = recom_model.get_user_define('temp_container1')
        for e in alllist:
            status=request.POST.get(e,None)
            if status!= None:
                all_list.append(e)
        print(all_list)
    else:
        outw =  recom_model.get_user_define('temp_container1')
        for e in outw:
            status=request.POST.get(e,None)
            if status!= None:
                out_list.append(e)
        alllist = recom_model.get_user_define('temp_container2')
        for e in alllist:
            status=request.POST.get(e,None)
            if status!= None:
                all_list.append(e)
        print(out_list)
        print(all_list)
    style_id = recom_model.get_idx('style_name',style)
    if weather_type =='cold':
        offset = int(0)
    elif weather_type =='mild':
        offset = int(1)
    else:
        offset = int(2)
    print(style_id)
    id = int(3*style_id+offset)
    # print(id)
    # print('\n')
    print(style)
    recom_model.set_value('style_avaliable',id,'true')
    return recom_index(request)

    
    
def generate_outfit(request,style,weather):
    ##get the temperature and weather for haining from the web
    weather = get_weather()
    # print(weather)
    context={'weather':weather, 
             "outfit1a":'/static/images/empty.png', "outfit1b":'/static/images/empty.png', "outfit1c":'/static/images/empty.png', 
             "outfit2a":'/static/images/empty.png', "outfit2b":'/static/images/empty.png', "outfit2c":'/static/images/empty.png', 
             "outfit3a":'/static/images/empty.png', "outfit3b":'/static/images/empty.png', "outfit3c":'/static/images/empty.png', 
             'img1':'',
             'img2':'',
             'img3':''
             }
    ##get the user-choosed weather
    try:
        u_c=request.POST.get("Cold",None) 
        u_m=request.POST.get("Mild",None) 
        u_h=request.POST.get("Hot",None) 
        if u_c !=None:
            u_weather = "cold"
        elif u_m !=None:
            u_weather = "mild"
        elif u_h !=None:
            u_weather = "hot"
        else:
            u_weather = weather
        # print(u_c,u_m,u_h)
        # print(u_weather)
        
        
    except:
        pass
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



    
    
    