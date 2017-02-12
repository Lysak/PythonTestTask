import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Product


class BasicTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_products_page_view(self):
        response = self.client.get('/products/')
        # page received correctly
        self.assertEqual(response.status_code, 200)

    def test_get_product_view(self):
        products_for_test = Product.objects.create(name='product', description='prod_desc', created_at=timezone.now(),
                                                   price=30, slug='product_slug')
        # product created
        self.assertEqual(products_for_test.pk, 1)

        category_for_test = Product.objects.create(name='category', description='category_desc',
                                                   created_at=timezone.now(), price=30, slug='category_slug')
        # category created
        self.assertEqual(category_for_test.pk, 2)

        product_link = "/products/{}/{}/".format(category_for_test.slug, products_for_test.slug)
        response = self.client.get(product_link)
        # page received correctly
        self.assertEqual(response.status_code, 200)


class LastAddedViewTests(TestCase):
    """
    Testing LastAdded view
    """

    # work +
    def test_latest_added_view_no_access_without_login(self):
        """
        If not login, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('last_added'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'If you want to watch this page, you need login.')
        self.assertQuerysetEqual(response.context['last_added_pr'], [])

    # work +
    def test_latest_added_view_no_product(self):
        """
        If no product exist, an appropriate message should be displayed.
        """
        self.client.force_login(User.objects.get_or_create(username='test')[0])
        response = self.client.get(reverse('last_added'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No items are available.')
        self.assertQuerysetEqual(response.context['last_added_pr'], [])

    # work +
    def test_latest_added_with_a_past_product(self):
        """
        Products with a created_at in the past should be displayed on the last_added page.
        """
        self.client.force_login(User.objects.get_or_create(username='test')[0])
        time = timezone.now() - datetime.timedelta(days=30)
        Product.objects.create(name='Past', description='past', created_at=time, price=30)
        response = self.client.get(reverse('last_added'))
        self.assertContains(response, "No items are available.", status_code=200)
        self.assertQuerysetEqual(response.context['last_added_pr'], [])

    # work +
    def test_latest_added_view_with_a_future_product(self):
        """
        Products with a created_at in the future should not be displayed on the latest_added page.
        """
        self.client.force_login(User.objects.get_or_create(username='test')[0])
        time = timezone.now() + datetime.timedelta(days=30)
        Product.objects.create(name='Future', description='future', created_at=time, price=30)
        response = self.client.get(reverse('last_added'))
        self.assertContains(response, "No items are available.", status_code=200)
        self.assertQuerysetEqual(response.context['last_added_pr'], [])

    def test_latest_added_with_future_product_and_past_product(self):
        """
        Even if both latest 24h product and future product exist, only latest 24h created product
        should be displayed.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        Product.objects.create(name='Now', description='now', created_at=timezone.now(), price=30)
        Product.objects.create(name='Past', description='past', created_at=time, price=30)
        response = self.client.get(reverse('last_added'))
        self.assertQuerysetEqual(
            response.context['last_added_pr'], ['<Product: Now>'])

    def test_latest_added_view_with_two_latest_24h_product(self):
        """
        The last_added page may display multiple product.
        """
        time = timezone.now() - datetime.timedelta(hours=2)
        Product.objects.create(name='Now1', description='now', created_at=timezone.now(), price=30)
        Product.objects.create(name='Now2', description='now', created_at=time, price=30)
        response = self.client.get(reverse('last_added'))
        self.assertQuerysetEqual(
            response.context['last_added_pr'], ['<Product: Now2>', '<Product: Now1>'], ordered=False)
