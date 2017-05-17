import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from django.utils import timezone

from product.forms import CommentForm
from product.models import Category, Product, Comment


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
    paginate_by = 3

    def get_queryset(self, **args):
        sorted_by = ('liked_by', '-liked_by')
        if self.request.GET.get('sort') in sorted_by:
            sort = self.request.GET.get('sort')
        else:
            sort = 'name'
        return self.model.objects.filter(category__slug=self.kwargs.get('slug'),
                                         created_at__lte=timezone.now()).order_by(sort)
        # users don't know about hidden products

    def get_context_data(self, **kwargs):
        context = super(CategorySlugListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['sort'] = self.request.GET.get('sort')
        return context


class ProductSlugDetailView(generic.DetailView):
    template_name = 'product/product_slug.html'
    context_object_name = 'product_only'
    model = Product

    def get_object(self, queryset=None):
        return self.model.objects.get(slug=self.kwargs.get('slug'), created_at__lte=timezone.now())

    def get_context_data(self, **kwargs):
        comment_form = CommentForm
        context = super(ProductSlugDetailView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        time_threshold = timezone.now() - datetime.timedelta(days=1)
        context['comments'] = Comment.objects.filter(comments_id=self.object, created_at__gte=time_threshold,
                                                     created_at__lte=timezone.now()).order_by('-created_at')
        context['form'] = comment_form
        return context


class LastAddedListView(generic.ListView):
    template_name = 'product/last_added.html'
    context_object_name = 'last_added_pr'
    model = Product
    paginate_by = 3

    def get_queryset(self):
        time_threshold = timezone.now() - datetime.timedelta(days=18)
        return self.model.objects.filter(created_at__gte=time_threshold,
                                         created_at__lte=timezone.now()).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(LastAddedListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


def product_like(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    if current_user.is_authenticated:
        if current_user in product.liked_by.all():
            product.liked_by.remove(current_user)
            messages.info(request, 'Product unliked.')
        else:
            product.liked_by.add(current_user)
            messages.info(request, 'Product liked.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def addcomment(request, product_id):
    if request.POST and ('pause' not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments = Product.objects.get(id=product_id)
            form.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
            if form.is_valid():
                form.save()
                messages.success(request, 'Comment sended.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



