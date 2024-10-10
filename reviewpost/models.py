from django.db import models
from django.contrib.auth.models import User
from vercel_storage import blob
# Create your models here.
class ReviewModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title =models.CharField(max_length = 100)
    content = models.TextField()
    useful_num = models.IntegerField(null = True, blank = True, default = 0)
    product_image = models.ImageField(upload_to='',null = True, blank=True)
    product_image_url = models.URLField(null=True,blank=True)
    def save(self, *args, **kwargs):
       if self.product_image:
           resp = blob.put(
               pathname=self.product_image.name,
               body=self.product_image,
               options={'token': settings.vercel_blob_token}
           )
           self.product_image = None
           self.product_image_url = resp['url'] 
       # 通常の保存処理を実行
       super().save(*args, **kwargs)