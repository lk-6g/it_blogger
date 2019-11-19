from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Topic, Entry
from .forms import EntryForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import markdown
from django.core.paginator import Paginator
from django.db.models import Q
from comments.models import Comment
from comments.forms import CommentForm
from django.views import View
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    # 根据评论数获取热门文章
    hot_entries = {}
    all_entries = Entry.objects.all()
    for entry in all_entries:
        comments = Comment.objects.filter(entry=entry)
        if len(comments) >= 3:
            hot_entries[entry] = entry

    search = request.GET.get('search')
    if not search:
        search = ''
    order = request.GET.get('order')
    tag = request.GET.get('tag')
    if not tag:
        tag = ''
    topic_id = request.GET.get('topic_id')
    try:
        topic = get_object_or_404(Topic, id=topic_id)
    except:
        topic = ''
    entries_list = tag_enteries_list(order, search, 0, topic, tag)
    entries = page_break(request, entries_list, 5)
    
    context = {'hot_entries':hot_entries, 'topic':topic, 'entries':entries, 'order':order, 'search': search, 'tag':tag}
    return render(request, 'it_bloggers/index.html', context)

def visitor(request, owner_id):
    owner = User.objects.get(id=owner_id)
    topics = Topic.objects.filter(owner=owner)
    per_entries = Entry.objects.filter(owner=owner)
    # 个人发文章总数
    entries_count = len(per_entries)
    # 个人全部标签
    tags = {}
    for entry in per_entries:
        for tag in entry.tags.all():
            tags[tag] = tag
    search = request.GET.get('search')
    if not search:
        search = ''
    order = request.GET.get('order')
    tag = request.GET.get('tag')
    if not tag:
        tag = ''
    topic_id = request.GET.get('topic_id')
    try:
        topic = get_object_or_404(Topic, id=topic_id)
    except:
        topic = ''
    entries_list = tag_enteries_list(order, search, owner, topic, tag)
    entries = page_break(request, entries_list, 5)
    
    context = {'owner':owner, 'topics':topics, 'tags':tags, 'topic':topic, 'entries':entries, 'entries_count':entries_count, 'order':order, 'search': search, 'tag':tag}
    return render(request, 'it_bloggers/visitor.html', context)

@login_required
def homepage(request):
    owner = request.user
    topics = Topic.objects.filter(owner=owner)
    my_entries = Entry.objects.filter(owner=owner)
    # 个人发文章总数
    entries_count = len(my_entries)
    # 个人全部标签
    tags = {}
    for entry in my_entries:
        for tag in entry.tags.all():
            tags[tag] = tag
    search = request.GET.get('search')
    if not search:
        search = ''
    order = request.GET.get('order')
    tag = request.GET.get('tag')
    if not tag:
        tag = ''
    topic_id = request.GET.get('topic_id')
    try:
        topic = get_object_or_404(Topic, id=topic_id)
    except:
        topic = ''
    entries_list = tag_enteries_list(order, search, owner, topic, tag)
    entries = page_break(request, entries_list, 5)
    
    context = {'topics':topics, 'tags':tags, 'topic':topic, 'entries':entries, 'entries_count':entries_count, 'order':order, 'search': search, 'tag':tag}
    return render(request, 'it_bloggers/homepage.html', context)

@login_required
def topics(request):
    topics_list = Topic.objects.filter(owner=request.user).order_by('-date_added')
    topics = page_break(request, topics_list, 10)
    
    context = {'topics':topics}
    return render(request, 'it_bloggers/topics.html', context)

@login_required
def entries(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    search = request.GET.get('search')
    if not search:
        search = ''
    order = request.GET.get('order')
    owner = request.user
    topic_id = request.GET.get('topic_id')
    try:
        topic = get_object_or_404(Topic, id=topic_id)
    except:
        topic = ''
    
    entries_list = get_entries_list(order, search, owner, topic)
            
    entries = page_break(request, entries_list, 10)
        
    context = {'topics':topics, 'entries':entries,'topic':topic, 'order':order, 'search': search}
    return render(request, 'it_bloggers/entries.html', context)

def entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    comments = Comment.objects.filter(entry=entry)
    
    # 浏览量 +1
    entry.read_count += 1
    entry.save(update_fields=['read_count'])
    # markdown语法拓展
    
    comment_form = CommentForm()
    
    next_entry = get_next_entry(entry_id)
    pre_entry = get_pre_entry(entry_id)
    
    context = {'entry':entry, 'comments':comments, 'comment_form':comment_form, 'next_entry':next_entry, 'pre_entry':pre_entry}
    return render(request, 'it_bloggers/entry.html', context)

# 点赞数 +1
@csrf_exempt
def increase_likes(request, entry_id):
    try:
        entry = Entry.objects.get(id=entry_id)
        entry.likes += 1
        entry.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')

@login_required
@require_POST
@csrf_exempt
def new_topic(request):
    text = request.POST["text"]
    try:
        new_topic = Topic()
        new_topic.text = text
        new_topic.owner = request.user
        new_topic.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")
    
@login_required
@require_POST
@csrf_exempt
def edit_topic(request):
    text = request.POST["text"]
    topic_id = request.POST["topic_id"]
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)
    try:
        topic.text = text
        topic.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required
def new_entry(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    
    if request.method != 'POST':
        form = EntryForm()
        
    else:
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.owner = request.user
            new_entry.save()
            form._save_m2m()
            topic_id = new_entry.topic.id
            #  转化为返回的网址字符串
            return HttpResponseRedirect('/homepage/')
        
    context = {'topics':topics, 'form':form}
    return render(request, 'it_bloggers/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    check_entry_owner(request, entry)
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    
    if request.method != 'POST':
        form = EntryForm(instance=entry)
        
    else:
        form = EntryForm(instance=entry, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            form._save_m2m()
            return HttpResponseRedirect(reverse('it_bloggers:entry', args=[entry.id]))
        
    context = {'topics':topics, 'entry':entry, 'form':form, 'tags': ' '.join([x for x in entry.tags.names()])}
    return render(request, 'it_bloggers/edit_entry.html', context)

@login_required
@require_POST
@csrf_exempt
def del_topic(request):
    topic_id = request.POST["topic_id"]
    try:
        topic = get_object_or_404(Topic, id=topic_id)
        check_topic_owner(request, topic)
        topic.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")
    
@login_required
@require_POST
@csrf_exempt
def del_entry(request):
    entry_id = request.POST["entry_id"]
    try:
        entry = get_object_or_404(Entry, id=entry_id)
        check_entry_owner(request, entry)
        entry.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")
    

def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404
    
def check_entry_owner(request, entry):
    if entry.owner != request.user:
        raise Http404
    
# 分页
def page_break(request, list_a, n):
    # 每页显示 1 篇文章
    paginator = Paginator(list_a, n)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    return paginator.get_page(page)

#  按搜索，用户，主题，热度排序条件过滤entries_list
def get_entries_list(order, search, filter_owner, filter_topic):
    #  搜索
    if search:
        if filter_owner:
            if order == 'read_count':
                entries_list = Entry.objects.filter(owner=filter_owner).filter(Q(title__icontains=search)|Q(text__icontains=search)|Q(topic__text__icontains=search)).order_by('-read_count')
            else:
                entries_list = Entry.objects.filter(owner=filter_owner).filter(Q(title__icontains=search)|Q(text__icontains=search)|Q(topic__text__icontains=search))
        else:
            if order == 'read_count':
                entries_list = Entry.objects.filter(Q(title__icontains=search)|Q(text__icontains=search)|Q(topic__text__icontains=search)).order_by('-read_count')
            else:
                entries_list = Entry.objects.filter(Q(title__icontains=search)|Q(text__icontains=search)|Q(topic__text__icontains=search))
    # 非搜索
    else:
        # 含用户
        if filter_owner:
            # 含用户，主题
            if filter_topic:
                # 含用户，主题，热度排序
                if order == 'read_count':
                    entries_list = Entry.objects.filter(owner=filter_owner).filter(topic=filter_topic).order_by('-read_count')
                # 正常排序
                else:
                    entries_list = Entry.objects.filter(owner=filter_owner).filter(topic=filter_topic)
            # 不含主题
            else:
                if order == 'read_count':
                    entries_list = Entry.objects.filter(owner=filter_owner).order_by('-read_count')
                else:
                    entries_list = Entry.objects.filter(owner=filter_owner).all()
                
        # 不含用户
        else:
            if filter_topic:
                if order == 'read_count':
                    entries_list = Entry.objects.filter(topic=filter_topic).order_by('-read_count')
                else:
                    entries_list = Entry.objects.filter(topic=filter_topic)
            else:
                if order == 'read_count':
                    entries_list = Entry.objects.order_by('-read_count')
                else:
                    entries_list = Entry.objects.all()
                
    return entries_list

# 按标签过滤entries_list（包含get_entries_list过滤条件）
def tag_enteries_list(order, search, filter_owner, filter_topic, tag):
    entries_list = get_entries_list(order, search, filter_owner, filter_topic)
    if tag:
        entries_list = entries_list.filter(tags__name__in=[tag])
    return entries_list

# 获取下一篇文章
def get_next_entry(entry_id):
    return Entry.objects.filter(id__gt=entry_id).order_by('id').first()

# 获取上一篇文章
def get_pre_entry(entry_id):
    return Entry.objects.filter(id__lt=entry_id).order_by('-id').first()