from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TrabajoAII.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'TrabajoAII_app.views.cover'),
    url(r'^login', 'TrabajoAII_app.views.login'),
    url(r'^logout', 'TrabajoAII_app.views.logout'),
    url(r'^search', 'TrabajoAII_app.views.search'),
    url(r'^results', 'TrabajoAII_app.views.results'),
    url(r'^offers', 'TrabajoAII_app.views.offers'),
    url(r'^contact', 'TrabajoAII_app.views.contact'),
#     url(r'^list_items', 'TrabajoAII_app.views.list_items'),
#     url(r'^list_users', 'TrabajoAII_app.views.list_users'),
#     url(r'^recommend', 'TrabajoAII_app.views.recommend'),
    url(r'^admin/', include(admin.site.urls)),
)
