from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Store, Category, Products
from rest_framework.authtoken.models import Token

User = get_user_model()

class StoreTests(APITestCase):

    def setUp(self):
        # Set up the client and initial user
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create initial data
        self.store = Store.objects.create(name='Test Store', owner=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.product = Products.objects.create(
            name='Test Product',
            description='Product description',
            price=100,
            # stock=10,
            category=self.category
        )

    def test_create_store(self):
        url = reverse('store-create')
        data = {
        'name': 'New Store',
        'description': 'This is George\'s new store', 
        'owner': self.user.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Store.objects.count(), 2)  # Check the count
        self.assertEqual(Store.objects.get(id=2).name, 'New Store')

    def test_list_stores(self):
        url = reverse('store-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if we have 1 store

    def test_retrieve_store(self):
        url = reverse('store-detail', kwargs={'pk': self.store.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.store.name)

    def test_update_store(self):
        url = reverse('store-detail', kwargs={'pk': self.store.id})
        data = {'name': 'Updated Store'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.store.refresh_from_db()
        self.assertEqual(self.store.name, 'Updated Store')

    def test_delete_store(self):
        url = reverse('store-detail', kwargs={'pk': self.store.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Store.objects.count(), 0)  # Ensure it is deleted

class CategoryTests(APITestCase):

    def setUp(self):
        # Set up the client and initial user
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a category
        # self.category = Category.objects.create(name='Test Category')
        self.store = Store.objects.create(name='Test Store', owner=self.user)
        self.category = Category.objects.create(name='Test Category', store=self.store.id)

        self.product = Products.objects.create(
            name='Test Product',
            description='Product description',
            price=100,
            # stock=10,
            category=self.category
        )

    def test_create_category(self):
        url = reverse('category-create')
        data = {'name': 'New Category'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)  # Check the count
        self.assertEqual(Category.objects.get(id=2).name, 'New Category')

    def test_retrieve_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    def test_update_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.id})
        data = {'name': 'Updated Category'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_delete_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)  # Ensure it is deleted

class ProductTests(APITestCase):

    def setUp(self):
        # Set up the client and initial user
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create initial data
        self.store = Store.objects.create(name='Test Store', owner=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.product = Products.objects.create(
            name='Test Product',
            description='Product description',
            price=100,
            # stock=10,
            category=self.category
        )

    def test_create_product(self):
        url = reverse('product-create')
        data = {
            'name': 'New Product',
            'description': 'New description',
            'price': 200,
            # 'stock': 20,
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Products.objects.count(), 2)  # Check the count
        self.assertEqual(Products.objects.get(id=2).name, 'New Product')

    def test_retrieve_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        data = {'name': 'Updated Product', 'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Products.objects.count(), 0)  # Ensure it is deleted

    def test_list_products_by_category(self):
        url = reverse('products-by-category', kwargs={'category_id': self.category.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check the count

    def test_search_products(self):
        url = reverse('product-search')
        response = self.client.get(url, {'search': 'Test Product'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check the count
        self.assertEqual(response.data[0]['name'], 'Test Product')
