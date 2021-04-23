from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import TenantProfile
from serializers import RegisterSerializer

class TenantProfileCreateTest(APITestCase):
    def setUp(self):
        self.client_ = User.objects.create_user(username='test_username', password='12345')
        self.data_ = {
            'user': self.client_.pk,
            'firstname': 'Name',
            'lastname': 'Lastname',
            'middlename': 'Middlename',
            'birth_date': '1990-06-28',
        }

    def test_create_tenant_profile(self) -> None:
        response = self.client.post(reverse('users:list-create-tenant'), self.data_)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_tenant_profile(self) -> None:
        self.data_.update({'firstname': ''})
        response = self.client.post(reverse('users:list-create-tenant'), self.data_)
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
        response = self.client.get(reverse('users:retrieve-update-delete-tenant',
                                           kwargs={'pk': self.tenant1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tenant1.user.username, self.client1.username)
        self.assertEqual(response.data['firstname'], self.tenant1.firstname)

    def test_get_all_existing_tenants_profiles(self) -> None:
        response = self.client.get(reverse('users:list-create-tenant'))
        self.assertEqual(TenantProfile.objects.all().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_tenant_profile(self) -> None:
        non_existent_id = 3
        response = self.client.get(reverse('users:retrieve-update-delete-tenant',
                                           kwargs={'pk': non_existent_id}))  # пользователь с id=3
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
        response = self.client.patch(reverse('users:retrieve-update-delete-tenant',
                                             kwargs={'pk': self.tenant.pk}), data=data_to_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['firstname'], data_to_update['firstname'])
        self.assertEqual(response.data['middlename'], data_to_update['middlename'])
        self.assertEqual(response.data['birth_date'], data_to_update['birth_date'])

    def test_update_tenant_profile_with_invalid_data(self) -> None:
        invalid_data = {'firstname': ''}
        response = self.client.patch(reverse('users:retrieve-update-delete-tenant',
                                             kwargs={'pk': self.tenant.pk}), data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TenantProfileDeleteTest(APITestCase):
    def setUp(self) -> None:
        self.client_ = User.objects.create_user(username='test', password='12345')
        self.tenant = TenantProfile.objects.create(
            user=self.client_, firstname='Ivan', lastname='Ivanov',
            middlename='Ivanovich', birth_date='2000-07-15'
        )

    def test_delete_tenant_profile(self) -> None:
        response = self.client.delete(reverse('users:retrieve-update-delete-tenant',
                                              kwargs={'pk': self.tenant.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TenantProfile.objects.all().count(), 0)


class TenantProfileFilteringTest(APITestCase):
    fixtures = ['fixtures/users.json']

    def test_birth_date_range(self) -> None:
        date_from = '1982-01-01'
        date_until = '1993-01-01'
        response = self.client.get(reverse('users:list-create-tenant'),
                                   {'birth_date__range': f'{date_from},{date_until}'})
        for i in response.data:
            self.assertGreaterEqual(dict(i)['birth_date'], date_from)
            self.assertLessEqual(dict(i)['birth_date'], date_until)

    def test_firstname_equality(self) -> None:
        name = 'Артем'
        user_in_db = 'Артем Теряев'
        response = self.client.get(reverse('users:list-create-tenant'), {'firstname': name})
        user = dict(response.data[0])
        self.assertEqual(user['firstname'] + ' ' + user['lastname'], user_in_db)

    def test_firstname_contains(self) -> None:
        contains = 'сим'
        user_in_db = 'Максим Зотов'
        response = self.client.get(reverse('users:list-create-tenant'), {'firstname__icontains': contains})
        user = dict(response.data[0])
        self.assertEqual(user['firstname'] + ' ' + user['lastname'], user_in_db)

class UserRegisterTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('api/v1/register')

        self.user_data = {
            'username': "test",
            'firstname': "Sergey",
            'lastname': "Zlatko",
            'birth_date': "1980-03-10",
            'password': "12345",
            'password2': "12345",
            'email': "ser@gmail.com"
        }

    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.asserEqual(response.status_code, 400)

