from django.conf.urls import patterns, url
# from views import *

urlpatterns = patterns('app.views',
       url(r'^$', 'Index'),
       )