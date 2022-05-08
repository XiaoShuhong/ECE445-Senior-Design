# import inWhat



def __init():
    global user_define
    user_define = {}
    user_define['style_name']= ['LADYLIKE','VIBRANT','GIRLY','CASUAL']
    user_define['backimg'] = ["/static/images/ladylike.jpg","/static/images/vibrant.png","/static/images/girly.jpg","/static/images/casual.jpg"]
    user_define['id'] = ['LADYLIKE','VIBRANT','GIRLY','CASUAL']
    user_define['style_avaliable']=[]   #每个style对应三种weather， 三个值 true/false
    fill_style_avaliable()
    ##
    user_define['style_avaliable'][0] = 'false'
    
    
def get_user_define(key):
    return user_define[key]

def add_user_define(key,value):
    user_define[key].append(value)

def fill_style_avaliable():
    for i in user_define['style_name']:
        for j in range(3):
            user_define['style_avaliable'].append('true')
            

def init_write_style():
    # user_define['container1'] = []
    # user_define['container2'] = []
    # user_define['container3'] = []
    
    user_define['temp_container1'] = []
    user_define['temp_container2'] = []
    user_define['temp_container3'] = []
    
def get_idx(key,value):
    for i in range(len(user_define[key])) :
        if user_define[key][i] == value:
            return i
def set_value(key,idx,value):
    user_define[key][idx]=value
    
    





    
    

    