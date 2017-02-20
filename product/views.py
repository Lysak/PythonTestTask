import datetime

from django.views import generic
from django.utils import timezone

from product.models import Category, Product


class ProductsListView(generic.ListView):
    template_name = 'product/products.html'
    context_object_name = 'category_all'
    model = Category

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


class CategorySlugListView(generic.ListView):
    template_name = 'product/category_slug.html'
    context_object_name = 'product_category_all'
    model = Product

    def get_queryset(self):
        return self.model.objects.filter(category__slug=self.kwargs.get('slug'))
        # users don't know about hidden products

    def get_context_data(self, **kwargs):
        context = super(CategorySlugListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


class ProductSlugDetailView(generic.DetailView):
    template_name = 'product/product_slug.html'
    context_object_name = 'product_only'
    model = Product

    def get_object(self, queryset=None):
        return self.model.objects.get(slug=self.kwargs.get('slug'), created_at__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(ProductSlugDetailView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


class LastAddedListView(generic.ListView):
    template_name = 'product/last_added.html'
    context_object_name = 'last_added_pr'
    model = Product

    def get_queryset(self):
        time_threshold = timezone.now() - datetime.timedelta(days=1)
        return self.model.objects.filter(created_at__gte=time_threshold, created_at__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(LastAddedListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context
