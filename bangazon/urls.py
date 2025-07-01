from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bangazonapi.models import *
from bangazonapi.views import *

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', Products, 'product')
router.register(r'productcategories', ProductCategories, 'productcategory')
router.register(r'lineitems', LineItems, 'orderproduct')
router.register(r'customers', Customers, 'customer')
router.register(r'users', Users, 'user')
router.register(r'orders', Orders, 'order')
router.register(r'cart', Cart, 'cart')
router.register(r'paymenttypes', Payments, 'payment')
router.register(r'profile', Profile, 'profile')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-token-auth', obtain_auth_token),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
