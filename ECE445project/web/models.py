from django.db import models

# Create your models here.
class hanger(models.Model):
    hanger_id = models.AutoField(primary_key=True)
    hanger_address = models.CharField(max_length=50)   
    is_bind = models.IntegerField(max_length=1)    
    hanger_status = models.IntegerField(max_length=1)  

    def toDict(self):
        return {'hanger_id':self.hanger_id,'hanger_address':self.hanger_address,'is_bind':self.is_bind,'hanger_status':self.hanger_status}

    class Meta:
        db_table = "hanger_status"  
        
class img_info(models.Model):
    img_id = models.AutoField(primary_key=True)
    img_name = models.CharField(max_length=500)   
    img_content = models.CharField(max_length=255)
    img_category = models.CharField(max_length=255)   
    img_attributes = models.CharField(max_length=200)  
    
    def toDict(self):
        return {'img_id':self.img_id,'img_name':self.img_name,'img_content':self.img_content,'img_category':self.img_category,'img_attributes':self.img_attributes}

    class Meta:
        db_table = "img_info"  
        
class bind(models.Model):
    bind_id = models.AutoField(primary_key=True)
    is_bind = models.IntegerField(max_length=1)   
    img_id = models.IntegerField()
    hanger_id = models.IntegerField()    
    img_name = models.CharField(max_length=500)  

    def toDict(self):
        return {'bind_id':self.bind_id,'is_bind':self.is_bind,'img_id':self.img_id,'hanger_id':self.hanger_id,'img_name':self.img_name}

    class Meta:
        db_table = "img_hanger_bind"  