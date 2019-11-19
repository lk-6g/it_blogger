from django.db import models
from it_bloggers.models import Entry
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Comment(MPTTModel):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = RichTextUploadingField()
    date_added = models.DateTimeField(auto_now_add=True)
    # 评论树形结构
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # 记录二级评论回复给谁
    reply_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers')
    
    # 替换Meta
    # class Meta:
    #     ordering = ('date_added',)
    class MPTTMeta:
        order_insertion_by = ['date_added']
        
    def __str__(self):
        return self.text[:20]
