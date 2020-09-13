
# Create your models here.
from django.db import models
from django.core.validators import FileExtensionValidator
import os
# Create your models here.

class Document(models.Model):
    document = models.ImageField(upload_to='images', null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def getName(self):
        fpath = self.document.path
        imageName = os.path.basename(fpath)
        return imageName

