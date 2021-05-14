from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import ReviewOnTenantListSerializer, ReviewOnLandlordPropertyListSerializer

from .models import ReviewOnTenant, ReviewOnLandlordProperty
from users.models import TenantProfile, LandlordProfile
from property.models import Property


class ReviewsTestCases(APITestCase):
    def setUp(self) -> None:
        self.client_ = User.objects.create_user(username='test', password='12345')
        self.client1_ = User.objects.create_user(username='test1', password='12345')
        self.client.force_authenticate(self.client_)
        self.client.force_authenticate(self.client1_)
        self.tenant_profile = TenantProfile.objects.create(
            user=self.client_,
            firstname='Tenant',
            lastname='Lastname',
            middlename='Middlename',
            birth_date='1980-04-17',
        )
        self.landlord_profile = LandlordProfile.objects.create(
            user=self.client1_,
            firstname='Landlord',
            lastname='Lastname',
            middlename='Middlename',
            birth_date='1950-06-28',
        )
        self.property = Property.objects.create(landlord=self.landlord_profile, name='my property1',
                                                address='my address1', description='no description1')
        self.data_review_on_tenant = {'title': 'title', 'description': 'description', 'rating': 4,
                                      'reviewer': self.property.pk, 'review_on': self.tenant_profile.pk}
        self.data_review_on_landlord_property = {'title': 'Some_title', 'description': 'desc', 'rating': 1,
                                                 'reviewer': self.tenant_profile.pk, 'review_on': self.property.pk}
        self.incorrect_data = {'title': 'title', 'description': 'description', 'rating': 0}
        self.review_on_tenant = ReviewOnTenant.objects.create(
            title=self.data_review_on_tenant['title'],
            description=self.data_review_on_tenant['description'],
            rating=self.data_review_on_tenant['rating'],
            reviewer=self.property,
            review_on=self.tenant_profile
        )
        self.reviews_on_landlord_property = ReviewOnLandlordProperty.objects.create(
            title=self.data_review_on_landlord_property['title'],
            description=self.data_review_on_landlord_property['description'],
            rating=self.data_review_on_landlord_property['rating'],
            reviewer=self.tenant_profile,
            review_on=self.property
        )
        self.client.login(username='test', password='12345')
        self.client.login(username='test1', password='12345')

    def test_create_reviews(self):
        review_on_tenant = self.client.post(reverse('reviews:list-create-tenant-review'), self.data_review_on_tenant)
        review_on_landlord_property = self.client.post(reverse('reviews:list-create-landlord-review'),
                                                       self.data_review_on_landlord_property)
        self.assertEqual(review_on_tenant.status_code, status.HTTP_201_CREATED)
        self.assertEqual(review_on_landlord_property.status_code, status.HTTP_201_CREATED)

    def test_list_reviews(self):
        review_on_tenant = self.client.get(reverse('reviews:list-create-tenant-review'))
        review_on_landlord_property = self.client.get(reverse('reviews:list-create-landlord-review'))
        self.assertEqual(review_on_tenant.status_code, status.HTTP_200_OK)
        self.assertEqual(review_on_landlord_property.status_code, status.HTTP_200_OK)

    def test_get_certain_reviews(self):
        response_review_on_tenant = self.client.get(reverse('reviews:delete-update-retrieve-tenant-review',
                                                            kwargs={'pk': self.review_on_tenant.pk}))
        response_review_on_landlord_property = self.client.get(reverse(
            'reviews:delete-update-retrieve-landlord-review', kwargs={'pk': self.reviews_on_landlord_property.pk})
        )
        self.assertEqual(response_review_on_tenant.status_code, status.HTTP_200_OK)
        self.assertEqual(response_review_on_landlord_property.status_code, status.HTTP_200_OK)

    def test_delete_reviews(self):
        response_review_on_tenant = self.client.delete(reverse('reviews:delete-update-retrieve-tenant-review',
                                                               kwargs={'pk': self.review_on_tenant.pk}))
        response_review_on_landlord_property = self.client.delete(
            reverse('reviews:delete-update-retrieve-landlord-review',
                    kwargs={'pk': self.reviews_on_landlord_property.pk}))
        self.assertEqual(response_review_on_tenant.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_review_on_landlord_property.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_reviews(self):
        new_data = {'description': 'really_new_description', 'rating': 5}
        response_review_on_tenant = self.client.patch(reverse('reviews:delete-update-retrieve-tenant-review',
                                                              kwargs={'pk': self.review_on_tenant.pk}), data=new_data)
        response_review_on_landlord_property = self.client.patch(
            reverse('reviews:delete-update-retrieve-landlord-review',
                    kwargs={'pk': self.reviews_on_landlord_property.pk}), data=new_data)

        self.assertEqual(response_review_on_tenant.data['description'], new_data['description'])
        self.assertEqual(response_review_on_tenant.status_code, status.HTTP_200_OK)
        self.assertEqual(response_review_on_landlord_property.data['description'], new_data['description'])
        self.assertEqual(response_review_on_landlord_property.status_code, status.HTTP_200_OK)

    def test_create_reviews_with_wrong_rating(self):
        response_review_on_tenant = self.client.post(reverse('reviews:list-create-tenant-review'), self.incorrect_data)
        response_review_on_landlord_property = self.client.post(reverse('reviews:list-create-landlord-review'),
                                                                self.incorrect_data)
        self.assertEqual(response_review_on_tenant.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_review_on_landlord_property.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reviews_list_model_data(self):
        self.client.post(reverse('reviews:list-create-tenant-review'), self.data_review_on_tenant)
        self.client.post(reverse('reviews:list-create-landlord-review'), self.data_review_on_landlord_property)

        response_review_on_tenant = self.client.get(reverse('reviews:list-create-tenant-review'))
        response_review_on_landlord_property = self.client.get(reverse('reviews:list-create-landlord-review'))
        reviews_on_tenant = ReviewOnTenant.objects.all()
        reviews_on_landlord_property = ReviewOnLandlordProperty.objects.all()
        serializer_tenant = ReviewOnTenantListSerializer(reviews_on_tenant, many=True)
        serializer_landlord_property = ReviewOnLandlordPropertyListSerializer(reviews_on_landlord_property, many=True)

        self.assertEqual(response_review_on_tenant.data['results'], serializer_tenant.data)
        self.assertEqual(response_review_on_tenant.status_code, status.HTTP_200_OK)
        self.assertEqual(response_review_on_landlord_property.data['results'], serializer_landlord_property.data)
        self.assertEqual(response_review_on_landlord_property.status_code, status.HTTP_200_OK)


class ReviewsFilteringTest(APITestCase):
    fixtures = ['fixtures/images.json',
                'fixtures/users.json',
                'fixtures/property.json',
                'fixtures/reviews.json']

    def setUp(self):
        self.client.force_authenticate(user=User)

    def test_rating_filter(self):
        response_review_on_tenant = self.client.get(reverse('reviews:list-create-tenant-review'), {'rating': 5})
        response_review_on_landlord_property = self.client.get(
            reverse('reviews:list-create-landlord-review'), {'rating': 2}
        )
        self.assertEqual(len(response_review_on_tenant.data['results']), 2)
        self.assertEqual(len(response_review_on_landlord_property.data['results']), 1)

    def test_rating_less_than_equal_filter(self):
        tenant_rating, landlord_rating = (3, 3)

        response_review_on_tenant = self.client.get(
            reverse('reviews:list-create-tenant-review'), {'rating__lte': tenant_rating}
        )
        response_review_on_landlord_property = self.client.get(
            reverse('reviews:list-create-landlord-review'), {'rating__lte':  landlord_rating}
        )
        tenant_data = response_review_on_tenant.data['results']
        landlord_data = response_review_on_landlord_property.data['results']

        for tenant_rate, landlord_rate in zip(tenant_data, landlord_data):
            self.assertLessEqual(dict(tenant_rate)['rating'], tenant_rating)
            self.assertLessEqual(dict(landlord_rate)['rating'], tenant_rating)
