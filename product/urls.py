from django.conf.urls import url

from . import views
#
# app_name = 'product'

urlpatterns = [
    url(r'^$', views.ProductsListView.as_view(), name='products'),
    url(r'^last_added/$', views.LastAddedListView.as_view(), name='last_added'),
    url(r'^(?P<slug>[\w-]+)/$', views.CategorySlugListView.as_view(), name='category_slug'),
    url(r'^(?P<pk>[\w-]+)/(?P<slug>[\w-]+)/$', views.ProductSlugDetailView.as_view(), name='product_slug'),
    # url(r'^$', views.products, name='products'),
    # url(r'^last_added/$', views.last_added, name='last_added'),
    # url(r'^(?P<slug>[\w-]+)/$', views.category_slug, name='category_slug'),
    # url(r'^(?P<pk>[\w-]+)/(?P<slug>[\w-]+)/$', views.product_slug, name='product_slug'),
]
