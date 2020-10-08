from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=124)
    email = models.CharField(max_length=124)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class ImageUpload(models.Model):
    pic = models.ImageField(upload_to='texttoimage')

        
        

    