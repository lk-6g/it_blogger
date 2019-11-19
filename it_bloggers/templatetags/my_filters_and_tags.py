from django import template
from django.utils import timezone
import math, markdown

register = template.Library()

@register.filter()
def lower(value):
    return value.lower()
    
# 过滤图片
@register.filter(name='transferImg')
def transferImg(value):
    val = str(value)
    v_start = '<img'
    v_end = '>'
    i = val.find(v_start)
    while i != -1:
        j = val.find(v_end, i)
        v = val[i:(j+1)]
        if v:
            val = val.replace(v, "【图片】")
        else:
            v = val[i:(len(val))]
            val = val.replace(v, "【图片】")
        i = val.find(v_start)
    return val
    
# 过滤代码块、标签<pre>内容
@register.filter(name='transferCode')
def transferCode(value):
    val = str(value)
    v_start = '<pre'
    v_end = '</pre>'
    i = val.find(v_start)
    while i != -1:
        j = val.find(v_end, i)
        v = val[i:(j+6)]
        if v:
            val = val.replace(v, "【代码块 / 文本 / 其他...】")
        else:
            v = val[i:(len(val))]
            val = val.replace(v, "【代码块 / 文本 / 其他...】")
        i = val.find(v_start)
    return val
    
# 获取相对时间
@register.filter(name='time_since_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if diff.days >= 1 and diff.days < 30:
        return str(diff.days) + "天前"

    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return value.strftime("%Y-%m-%d")
    
# mark_down语法过滤器
@register.filter(name='mk_filter')
def mk_filter(value):
    md = markdown.Markdown(
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 目录扩展
        'markdown.extensions.toc',
        ])
    return md.convert(value)

# 减一
@register.filter(name='minus')
def minus(value, n):
    n = int(n)
    value = int(value)
    return value - n

# 以长度n过滤并在结尾加...
@register.filter(name='max_len')
def max_len(value, n):
    n = int(n)
    if len(value) > n:
        value = str(value[0:n]) + '...'
    else:
        value = str(value)
    return value