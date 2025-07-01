from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers"""
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer', lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'phone_number', 'address')
        depth = 1


class Customers(ViewSet):

    def update(self, request, pk=None):
        """
        @api {PUT} /customers/:id PUT changes to customer profile
        @apiName UpdateCustomer
        @apiGroup Customer

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {id} id Customer Id to update
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        customer = Customer.objects.get(user=request.auth.user)
        customer.user.last_name = request.data["last_name"]
        customer.user.email = request.data["email"]
        customer.address = request.data["address"]
        customer.phone_number = request.data["phone_number"]
        customer.user.save()
        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
