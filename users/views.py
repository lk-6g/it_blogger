from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.urls.base import reverse
from .forms import ProfileForm, RegisterForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

def logout_view(ruquest):
    logout(ruquest)
    return HttpResponseRedirect(reverse('it_bloggers:index'))

def register(request):
    if request.method != 'POST':
        form = RegisterForm()
        
    else:
        form = RegisterForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('it_bloggers:index'))
        
    context = {'form':form}
    return render(request, 'users/register.html', context)
    
@login_required
def profile_edit(request, owner_id):
    user = get_object_or_404(User, id=owner_id)
    if request.user != user:
        return HttpResponse("你没有权限修改此用户信息。")
    
    if Profile.objects.filter(user_id=owner_id).exists():
        profile = Profile.objects.get(user_id=owner_id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method != 'POST':
        form = ProfileForm()
        
    else:
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_cd = form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            return HttpResponseRedirect(reverse('it_bloggers:index'))
        
    context = {'profile':profile, 'user': user, 'form':form}
    return render(request, 'users/profile_edit.html', context)