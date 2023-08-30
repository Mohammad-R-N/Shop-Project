from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Category, Product


class TestMenuView(TestCase):

    def setUp(self):
        self.client= Client()
        self.menu_url = reverse('menu')
        self.category = Category.objects.create( name = "category 1", photo = 'test.png')
        self.category2 = Category.objects.create( name = "category 2", photo = 'test.png')
        self.product = Product.objects.create( name = "product 1", price = 10.12 , category_menu = self.category, photo = 'product.png', status = 'active', )
        self.product2 = Product.objects.create( name = "product 2", price = 10.12 , category_menu = self.category, photo = 'product.png', status = 'active', )
        self.product3 = Product.objects.create( name = "product 3", price = 10.12 , category_menu = self.category2, photo = 'product.png', status = 'active', )
    
    def test_menu_view_GET(self):
        response = self.client.get(self.menu_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu.html')

    def test_menu_view_GET_context(self):
        response = self.client.get(self.menu_url)
        self.assertIn(self.product, response.context["product"])
        self.assertIn(self.category, response.context["category"])

    def test_menu_view_POST_context_if_all(self):
        response = self.client.post(self.menu_url, {"all": "true"})
        
        self.assertEqual(response.context["category"].count(), 2)
        self.assertEqual(response.context["product"].count(), 3)

    def test_menu_view_POST_context_if_not_all(self):
        response = self.client.post(self.menu_url, {"category 1": "true"})

        self.assertEqual(response.context["category"].count(), 2)
        self.assertEqual(response.context["product"].count(), 2)

    def test_menu_view_post_context_without_cookie(self):
        response = self.client.post(self.menu_url, {"product 2": "true", "quantity": 5})
        
        self.assertTemplateUsed(response, 'menu/menu.html')
        self.assertEqual(response.context["category"].count(), 2)
        self.assertEqual(response.context["product"].count(), 3)

    def test_menu_view_post_context_with_cookie(self):
        response = self.client.post(self.menu_url, {"product 3": "true", "quantity": 4})
        
        self.assertTemplateUsed(response, 'menu/menu.html')
        self.assertEqual(response.context["category"].count(), 2)
        self.assertEqual(response.context["product"].count(), 3)

    def test_menu_view_post_set_cookie(self):
        context = {"product 3": "true", "quantity": 4}
        response = self.client.post(self.menu_url, context )
       
        self.assertEqual(response.cookies['product'].value, '-product 3=4')

    def test_menu_view_post_set_cookie_with_multiple_products(self):
        context = {"product 3": "true", "quantity": 4}
        context1 = {"product 2": "true", "quantity": 3}

        response = self.client.post(self.menu_url, context )
        response = self.client.post(self.menu_url, context1 )
       
        self.assertEqual(response.cookies['product'].value, '-product 3=4-product 2=3')
 

class TestSearchProducts(TestCase):
    def setUp(self):
        self.client= Client() 
        self.search_product_url = reverse('search_products')
        self.category = Category.objects.create( name = "category 1", photo = 'test.png')
        self.product1 = Product.objects.create( name = "product 1", price = 20.12 , category_menu = self.category,photo = 'product.png', status = 'active', )
        self.product2 = Product.objects.create( name = "product 2", price = 10.12 , category_menu = self.category,photo = 'product.png', status = 'active', )

    def test_search_product_GET(self):
        response = self.client.get(self.search_product_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/search_results.html')
        

    def test_search_product_with_query_context(self):
        query1 = "product 1"
        response = self.client.get(self.search_product_url, {"query": query1 })
        
        self.assertContains(response, query1)
        self.assertIn(self.product1, response.context["results"])
        self.assertNotIn(self.product2, response.context["results"])


    def test_search_product_with_empty_query_context(self):
        query1 = ""
        response = self.client.get(self.search_product_url, {"query": query1 })
        self.assertEqual(len(response.context["results"]), 0)



class TestProductPopup(TestCase):
    def setUp(self):
        self.client= Client() 
        self.category = Category.objects.create( name = "category 1", photo = 'test.png')
        self.product = Product.objects.create( name = "product 1", price = 10.12 , category_menu = self.category,photo = 'product.png', status = 'active', )
        self.product_popup_url = reverse('product_popup', kwargs={'product_id': 1})

    def test_product_popup_GET(self):
        response = self.client.get(self.product_popup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/product_detail.html')

    def test_product_popup_context(self):
        response = self.client.get(self.product_popup_url)
        self.assertEqual(response.context['product'], self.product)