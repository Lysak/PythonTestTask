from django.conf.urls import url

from . import views


from .views import *


urlpatterns = [
    url(r'^addcomment/(?P<product_id>\d+)/$', addcomment),
    url(r'^addlike/(?P<product_id>\d+)/$', product_like),
    url(r'^$', views.ProductsListView.as_view(), name='products'),
    url(r'^last_added/$', views.LastAddedListView.as_view(), name='last_added'),
    url(r'^(?P<slug>[\w-]+)/$', views.CategorySlugListView.as_view(), name='category_slug'),
    url(r'^(?P<pk>[\w-]+)/(?P<slug>[\w-]+)/$', views.ProductSlugDetailView.as_view(), name='product_slug'),

]
