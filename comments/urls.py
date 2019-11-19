from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    # 发表评论
    path('new_comment/<entry_id>/', views.new_comment, name='new_comment'),
    # 处理二级回复
    path('new_comment/<entry_id>/<parent_comment_id>/', views.new_comment, name='comment_reply')
]