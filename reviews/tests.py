from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import (
    TenantReviewDetailSerializer, TenantReviewListSerializer,
    LandlordReviewDetailSerializer,
)
from .models import TenantReview, LandlordReview


class TenantReviewTestCases(APITestCase):
    def setUp(self) -> None:
        self.data = {'title': 'title', 'description': 'description', 'rating': 4}
        self.incorrect_data = {'title': 'title', 'description': 'description', 'rating': 0}
        self.client_ = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

    def test_create_tenant_review(self):
        response = self.client.post(reverse('reviews:create-tenant-review'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_tenant_review(self):
        response = self.client.get(reverse('reviews:list-tenant-review'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_certain_tenant_review(self):
        tenant_review = TenantReview.objects.create(title='new_review', description='description', rating=4)
        response = self.client.get(reverse('reviews:delete-update-retrieve-tenant-review',
                                           kwargs={'pk': tenant_review.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tenant_review(self):
        tenant_review = TenantReview.objects.create(title='some_title', description='description', rating=1)
        response = self.client.delete(reverse('reviews:delete-update-retrieve-tenant-review',
                                              kwargs={'pk': tenant_review.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_tenant_review(self):
        tenant_review = TenantReview.objects.create(title='some_title', description='description', rating=1)
        new_data = {'description': 'really_new_description', 'rating': 5}
        response = self.client.patch(reverse('reviews:delete-update-retrieve-tenant-review',
                                             kwargs={'pk': tenant_review.pk}), data=new_data)

        self.assertEqual(response.data['description'], new_data['description'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review_with_wrong_rating(self):
        response = self.client.post(reverse('reviews:create-tenant-review'), self.incorrect_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tenant_review_list_model_data(self):
        TenantReview.objects.create(title='some_title', description='description', rating=1)
        TenantReview.objects.create(title='title', description='who_knows', rating=5)
        response = self.client.get(reverse('reviews:list-tenant-review'))
        reviews = TenantReview.objects.all()
        serializer = TenantReviewListSerializer(reviews, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SerializersTestCases(APITestCase):
    def test_tenant_review_model_fields(self):
        tenant_review = TenantReview.objects.create(title='title', description='desct', rating=5)
        serializer = TenantReviewDetailSerializer(tenant_review)
        for field_name in serializer.data:
            self.assertEqual(serializer.data[field_name],
                             getattr(tenant_review, field_name))

    def test_landlord_review_model_fields(self):
        landlord_review = LandlordReview.objects.create(title='title_title', description='description', rating=1)
        serializer = LandlordReviewDetailSerializer(landlord_review)
        for field_name in serializer.data:
            self.assertEqual(serializer.data[field_name],
                             getattr(landlord_review, field_name))
