from django import forms
from .models import Topic, Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'text', 'topic', 'tags', 'picture']
        labels = {'title':'标题：', 'text':'内容：', 'topic':'主题', 'tags':'标签', 'picture':'图片'}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}