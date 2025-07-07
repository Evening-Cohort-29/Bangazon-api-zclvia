"""View module for handling requests about stores"""

from bangazonapi.models import Customer, Product, Store
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .product import ProductSerializer


class SellerSerializer(serializers.ModelSerializer):
    """JSON serializer for seller (customer user) information"""

    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Customer
        fields = ("id", "first_name", "last_name")


class StoreSerializer(serializers.ModelSerializer):
    """JSON serializer for stores"""

    seller = SellerSerializer(source="customer", read_only=True)
    seller_name = serializers.CharField(read_only=True)
    product_count = serializers.IntegerField(read_only=True)
    products = ProductSerializer(many=True, read_only=True, source="customer.products")

    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "description",
            "seller",
            "seller_name",
            "product_count",
            "products",
            "created_date",
        )
        depth = 1


class StoreListSerializer(serializers.ModelSerializer):
    """JSON serializer for stores list (without products for performance)"""

    seller = SellerSerializer(source="customer", read_only=True)
    seller_name = serializers.CharField(read_only=True)
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Store
        fields = ("id", "name", "description", "seller", "seller_name", "product_count")


class Stores(ViewSet):
    """Request handlers for Stores in the Bangazon Platform"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """
        @api {POST} /stores POST new store
        @apiName CreateStore
        @apiGroup Store

        @apiHeader {String} Authorization Auth token
        @apiParam {String} name Store name
        @apiParam {String} description Store description
        """
        try:
            customer = Customer.objects.get(user=request.auth.user)

            # Check if customer already has a store
            if hasattr(customer, "store"):
                return Response(
                    {"message": "Customer already has a store"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_store = Store()
            new_store.customer = customer
            new_store.name = request.data["name"]
            new_store.description = request.data["description"]
            new_store.save()

            serializer = StoreSerializer(new_store, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """
        @api {GET} /stores/:id GET store
        @apiName GetStore
        @apiGroup Store
        """
        try:
            store = Store.objects.get(pk=pk)
            serializer = StoreSerializer(store, context={"request": request})
            return Response(serializer.data)
        except Store.DoesNotExist:
            return Response(
                {"message": "Store not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        @api {PUT} /stores/:id UPDATE store
        @apiName UpdateStore
        @apiGroup Store
        """
        try:
            store = Store.objects.get(pk=pk)

            # Ensure the current user owns this store
            if store.customer.user != request.auth.user:
                return Response(
                    {"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
                )

            store.name = request.data["name"]
            store.description = request.data["description"]
            store.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Store.DoesNotExist:
            return Response(
                {"message": "Store not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        @api {GET} /stores GET all stores with products
        @apiName ListStores
        @apiGroup Store
        """
        try:
            # Only get stores that have products for sale
            stores = Store.objects.filter(customer__products__isnull=False).distinct()

            # Check if we need full product data or just the list
            include_products = (
                request.query_params.get("include_products", "true").lower() == "true"
            )

            if include_products:
                serializer = StoreSerializer(
                    stores, many=True, context={"request": request}
                )
            else:
                serializer = StoreListSerializer(
                    stores, many=True, context={"request": request}
                )

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
