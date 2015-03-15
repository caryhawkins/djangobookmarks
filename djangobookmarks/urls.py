import os.path
from django.conf.urls import *
from djangobookmarks.bookmarks.views import *
from django.views.generic.base import TemplateView


site_media = os.path.join(os.path.dirname(__file__), 'site_media')

urlpatterns = patterns('',
                       #Browsing
                      (r'^$', main_page),
                      (r'^user/(\w+)/$', user_page),
                       #Session Management
                      (r'^login/$', 'django.contrib.auth.views.login'),
                      (r'^logout/$', logout_page),
                      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                       {'document_root': site_media}),
                      (r'^register/$', register_page),
                      (r'^register/success/$', TemplateView, {'template': 'registration/register_success.html'}),
                       #Account Management
                      (r'save/$', bookmark_save_page),
                       )
