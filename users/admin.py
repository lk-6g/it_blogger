from django.contrib import admin

# Register your models here.
from users.models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# 定义一个行内 admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'

# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# 已在User中关联，根据个人喜好选择注册与否
admin.site.register(Profile)