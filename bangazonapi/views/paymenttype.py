"""View module for handling requests about customer payment types"""

from bangazonapi.models import Customer, Payment
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Payment

    Arguments:
        serializers
    """

    class Meta:
        model = Payment
        url = serializers.HyperlinkedIdentityField(
            view_name="payment", lookup_field="id"
        )
        fields = (
            "id",
            "url",
            "merchant_name",
            "account_number",
            "expiration_date",
            "create_date",
        )


class Payments(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized payment instance
        """
        new_payment = Payment()
        new_payment.merchant_name = request.data["merchant_name"]
        new_payment.account_number = request.data["account_number"]
        new_payment.expiration_date = request.data["expiration_date"]
        new_payment.create_date = request.data["create_date"]
        customer = Customer.objects.get(user=request.auth.user)
        new_payment.customer = customer
        new_payment.save()

        serializer = PaymentSerializer(new_payment, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment type

        Returns:
            Response -- JSON serialized payment_type instance
        """
        try:
            payment_type = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment_type, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single payment type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Payment.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to payment type resource

        Returns only the payment types belonging to the authenticated user
        """
        # Get the customer associated with the authenticated user
        customer = Customer.objects.get(user=request.auth.user)

        # Filter payment types to only include those belonging to this customer
        payment_types = Payment.objects.filter(customer=customer)

        serializer = PaymentSerializer(
            payment_types, many=True, context={"request": request}
        )
        return Response(serializer.data)
