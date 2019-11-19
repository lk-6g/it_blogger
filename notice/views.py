# Create your views here.

from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from it_bloggers.models import Entry

# 通知列表
class CommentNoticeListView(LoginRequiredMixin, ListView):
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/list.html'
    # 登录重定向
    login_url = '/users/login/'

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()
    
    def get_context_data(self, **kwargs):
        all_notices = self.request.user.notifications.all()
        # 获取原有的上下文
        context = super().get_context_data(**kwargs)
        # 增加新上下文
        context['all_notices'] = all_notices
        return context

# 更新未读通知
class CommentNoticeUpdateView(View):
    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            entry = Entry.objects.get(id=request.GET.get('entry_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(entry)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')