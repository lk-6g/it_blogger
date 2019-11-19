from django.shortcuts import get_object_or_404, redirect
from it_bloggers.models import Entry
from django.contrib.auth.decorators import login_required
from comments.forms import CommentForm
from django.http.response import HttpResponse
from .models import Comment
from django.views.decorators.csrf import csrf_exempt
from notifications.signals import notify
from django.contrib.auth.models import User

# Create your views here.

@csrf_exempt
@login_required
def new_comment(request, entry_id, parent_comment_id=None):
    entry = get_object_or_404(Entry, id=entry_id)
    
    if request.method != 'POST':
        return HttpResponse("不接受非POST请求")
        
    else:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.entry = entry
            new_comment.owner = request.user
            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.owner
                new_comment.save()
                #  给目标用户发送通知
                if not parent_comment.owner.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.owner,
                        verb='回复了你',
                        target=entry,
                        action_object=new_comment,
                        )
                # 锚定位
                redirect_url = entry.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
                return redirect(redirect_url)
            
            new_comment.save()
            #  给管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=entry,
                    action_object=new_comment,
                    )
            redirect_url = entry.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            return redirect(redirect_url)
        else:
            return HttpResponse("输入不合法，请重新输入")