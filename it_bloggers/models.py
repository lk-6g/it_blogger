from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls.base import reverse

# Create your models here.
class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta():
        ordering = ('-date_added',)   
    
    def __str__(self):
        return self.text
    
class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = RichTextUploadingField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    read_count = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)
    picture = models.ImageField(upload_to='picture/%Y%m%d/', blank=True)
    likes = models.PositiveIntegerField(default=0)
    
    class Meta():
        verbose_name_plural = 'entries'
        ordering = ('-date_added',)
        
    def __str__(self):
        if len(self.text) > 50:
            return self.title[:50] + '...'
        else:
            return self.title
        
    #  获取地址
    def get_absolute_url(self):
        return reverse('it_bloggers:entry', args=[self.id])

        # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        entry = super(Entry, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.picture and not kwargs.get('update_fields'):
            image = Image.open(self.picture)
            (x, y) = image.size
            new_x = 300
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.picture.path)

        return entry