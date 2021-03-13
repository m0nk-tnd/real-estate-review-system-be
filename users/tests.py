import json

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from .models import TenantProfile


class TenantProfileCreateTest(APITestCase):
    def setUp(self):
        self.client_ = User.objects.create_user(username='test', password='12345')
        self.data_ = {
            'user': self.client_.pk,
            'firstname': 'Name',
            'lastname': 'Lastname',
            'middlename': 'Middlename',
            'birth_date': '1990-06-28',
        }

    def test_create_tenant_profile(self) -> None:
        response = self.client.post('/profile/tenant/create', self.data_)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_tenant_profile(self) -> None:
        self.data_.update({'middlename': ''})
        response = self.client.post('/profile/tenant/create', json.dumps(self.data_))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TenantProfileListGetTest(APITestCase):
    def setUp(self) -> None:
        self.client1 = User.objects.create_user(username='testuser', password='12345')
        self.client2 = User.objects.create_user(username='testuser1', password='12345')
        self.tenant1 = TenantProfile.objects.create(
            user=self.client1, firstname='Ivan', lastname='Ivanov',
            middlename='Ivanovich', birth_date='2000-07-15'
        )
        self.tenant2 = TenantProfile.objects.create(
            user=self.client2, firstname='Andrey', lastname='Andreev',
            middlename='Andreevich', birth_date='1985-01-30'
        )

    def test_get_existing_tenant_profile(self) -> None:
        response = self.client.get(f'/profile/tenant/{self.tenant1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tenant1.user.username, self.client1.username)
        self.assertEqual(response.data['firstname'], self.tenant1.firstname)

    def test_get_all_existing_tenants_profiles(self) -> None:
        response = self.client.get(f'/profile/tenant')
        self.assertEqual(TenantProfile.objects.all().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_tenant_profile(self) -> None:
        response = self.client.get('/profile/tenant/3')  # пользователь с id=3
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TenantProfileUpdateTest(APITestCase):
    def setUp(self) -> None:
        self.client_ = User.objects.create_user(username='test', password='12345')
        self.tenant = TenantProfile.objects.create(
            user=self.client_, firstname='Ivan', lastname='Ivanov',
            middlename='Ivanovich', birth_date='2000-07-15'
        )

    def test_update_tenant_profile(self) -> None:
        data_to_update = {'firstname': "Anton", 'middlename': 'Antonovich', 'birth_date': '1988-03-25'}
        response = self.client.patch(f'/profile/tenant/{self.tenant.pk}', data=data_to_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['firstname'], data_to_update['firstname'])
        self.assertEqual(response.data['middlename'], data_to_update['middlename'])
        self.assertEqual(response.data['birth_date'], data_to_update['birth_date'])

    def test_update_tenant_profile_with_invalid_data(self) -> None:
        invalid_data = {'firstname': ''}
        response = self.client.patch(f'/profile/tenant/{self.tenant.pk}', data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TenantProfileDeleteTest(APITestCase):
    def setUp(self) -> None:
        self.client_ = User.objects.create_user(username='test', password='12345')
        self.tenant = TenantProfile.objects.create(
            user=self.client_, firstname='Ivan', lastname='Ivanov',
            middlename='Ivanovich', birth_date='2000-07-15'
        )

    def test_delete_tenant_profile(self) -> None:
        response = self.client.delete(f'/profile/tenant/{self.tenant.pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TenantProfile.objects.all().count(), 0)
