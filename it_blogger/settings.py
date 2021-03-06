"""
Django settings for it_blogger project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kpi)awi@r=)m9y%_vbc&9m5u(ho#^z4gqbi@cdte_3y)tok^he'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方登录
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 第三方登录APP
    'allauth.socialaccount.providers.github',
    
    # My apps
    'it_bloggers',
    'users',
    'comments',
    'taggit',
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'notifications',
    'notice',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'it_blogger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'it_blogger/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'it_blogger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

'''第三方登录配置'''
AUTHENTICATION_BACKENDS = (
    # Django 后台可独立于 allauth 登录
    'django.contrib.auth.backends.ModelBackend',
    # 配置 allauth 独有的认证方法，如 email 登录
    'allauth.account.auth_backends.AuthenticationBackend',
)
# 设置站点
SITE_ID = 1
# 登录成功后重定向地址
LOGIN_REDIRECT_URL = '/'

# 日志系统
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'WARNING',
            
            # 'class': 'logging.FileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': 30,
            
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# 时区
TIME_ZONE = 'Asia/Shanghai'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
LOGIN_URL = '/users/login/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# ckeditor图片上传路径
CKEDITOR_UPLOAD_PATH = 'upload/'

# 重置密码邮箱设置
# SMTP服务器，改为你的邮箱的smtp!
EMAIL_HOST = 'smtp.***.com'
# 改为你自己的邮箱名！
EMAIL_HOST_USER = '邮箱地址'
# 你的邮箱密码
EMAIL_HOST_PASSWORD = '邮箱密码'
# 发送邮件的端口
EMAIL_PORT = 25
# 是否使用 TLS
EMAIL_USE_TLS = True
# 默认的发件人
DEFAULT_FROM_EMAIL = 'IT Blogger <lk940322@163.com>'

# ckeditor富文本编辑器内置模块自定义
CKEDITOR_CONFIGS = {
    # django-ckeditor默认使用default配置
    'default': {
        # 编辑器宽度自适应
        'width':'auto',
        'height':'385px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格，全部插件
        # 'toolbar': 'full',
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            # 撤销、重做
            ['Undo', 'Redo'],
            # 表情 特殊符号 代码块 源码
            ['Smiley', 'SpecialChar', 'CodeSnippet', 'Source'], 
            # 字号及字体风格
            ['FontSize', 'Bold', 'Italic', 'Strike', 'Underline', 'RemoveFormat', 'Blockquote'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 链接
            ['Link', 'Unlink', 'Anchor'],
            # 列表
            ['NumberedList', 'BulletedList'],
            # 图片 flash 表格 底线 
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            # 样式、分级
            ['Styles', 'Format'],
            # 最大化
            ['Maximize'],
        ],
        # 加入代码块、Prism、widget、lineutils插件
        'extraPlugins': ','.join(['codesnippet', 'uploadimage', 'prism', 'widget', 'lineutils']),
    }
}
# ckeditor界面语言汉语
LANGUAGE_CODE = 'zh-cn'

# Configure Django App for Heroku.

import django_heroku

django_heroku.settings(locals())