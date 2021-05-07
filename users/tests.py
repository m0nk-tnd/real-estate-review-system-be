from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import TenantProfile, LandlordProfile

from .models import TenantProfile
from .serializers import RegisterSerializer
from django.db import IntegrityError


class ProfilesCreateTest(APITestCase):
    def setUp(self):
        self.client_ = User.objects.create_user(username='test_username', password='12345')
        self.data_ = {
            'user': self.client_.pk,
            'firstname': 'Name',
            'lastname': 'Lastname',
            'middlename': 'Middlename',
            'birth_date': '1990-06-28',
        }

    def test_create_profiles(self) -> None:
        response_tenant_profile = self.client.post(reverse('users:list-create-tenant'), self.data_)
        response_landlord_profile = self.client.post(reverse('users:list-create-landlord'), self.data_)
        self.assertEqual(response_tenant_profile.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_landlord_profile.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_profiles(self) -> None:
        self.data_.update({'firstname': ''})
        response_tenant_profile = self.client.post(reverse('users:list-create-tenant'), self.data_)
        response_landlord_profile = self.client.post(reverse('users:list-create-landlord'), self.data_)
        self.assertEqual(response_tenant_profile.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_landlord_profile.status_code, status.HTTP_400_BAD_REQUEST)


class ProfilesListGetTest(APITestCase):
    def setUp(self) -> None:
        self.client1 = User.objects.create_user(username='testuser', password='12345')
        self.client2 = User.objects.create_user(username='testuser1', password='12345')
        self.tenant_profile = TenantProfile.objects.create(
            user=self.client1, firstname='Ivan', lastname='Ivanov',
            middlename='Ivanovich', birth_date='2000-07-15'
        )
        self.landlord_profile = LandlordProfile.objects.create(
            user=self.client2, firstname='Andrey', lastname='Andreev',
            middlename='Andreevich', birth_date='1985-01-30'
        )

    def test_get_existing_profiles(self) -> None:
        response_tenant_profile = self.client.get(reverse('users:retrieve-update-delete-tenant',
                                                          kwargs={'pk': self.tenant_profile.pk}))
        response_landlord_profile = self.client.get(reverse('users:retrieve-update-delete-landlord',
                                                            kwargs={'pk': self.landlord_profile.pk}))
        self.assertEqual(response_tenant_profile.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tenant_profile.user.username, self.client1.username)

        self.assertEqual(response_landlord_profile.status_code, status.HTTP_200_OK)
        self.assertEqual(self.landlord_profile.user.username, self.client2.username)

    def test_get_nonexistent_profiles(self) -> None:
        non_existent_id = 3
        response_tenant_profile = self.client.get(reverse('users:retrieve-update-delete-tenant',
                                                          kwargs={'pk': non_existent_id}))  # tenant с id=3
        response_landlord_profile = self.client.get(reverse('users:retrieve-update-delete-landlord',
                                                            kwargs={'pk': non_existent_id}))  # landlord с id=3
        self.assertEqual(response_tenant_profile.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_landlord_profile.status_code, status.HTTP_404_NOT_FOUND)


class ProfilesUpdateTest(APITestCase):
    fixtures = ['fixtures/users.json']

    def test_update_profiles(self) -> None:
        data_to_update = {'firstname': "Anton", 'middlename': 'Antonovich', 'birth_date': '1988-03-25'}
        response_tenant_profile = self.client.patch(reverse('users:retrieve-update-delete-tenant',
                                                            kwargs={'pk': 1}), data=data_to_update)
        response_landlord_profile = self.client.patch(reverse('users:retrieve-update-delete-landlord',
                                                              kwargs={'pk': 2}), data=data_to_update)
        self.assertEqual(response_tenant_profile.status_code, status.HTTP_200_OK)
        self.assertEqual(response_tenant_profile.data['firstname'], data_to_update['firstname'])
        self.assertEqual(response_tenant_profile.data['middlename'], data_to_update['middlename'])
        self.assertEqual(response_tenant_profile.data['birth_date'], data_to_update['birth_date'])

        self.assertEqual(response_landlord_profile.status_code, status.HTTP_200_OK)
        self.assertEqual(response_landlord_profile.data['firstname'], data_to_update['firstname'])
        self.assertEqual(response_landlord_profile.data['middlename'], data_to_update['middlename'])
        self.assertEqual(response_landlord_profile.data['birth_date'], data_to_update['birth_date'])

    def test_update_profiles_with_invalid_data(self) -> None:
        invalid_data = {'firstname': '', 'middlename': 101}
        response_tenant_profile = self.client.patch(reverse('users:retrieve-update-delete-tenant',
                                                            kwargs={'pk': 2}), data=invalid_data)
        response_landlord_profile = self.client.patch(reverse('users:retrieve-update-delete-landlord',
                                                              kwargs={'pk': 1}), data=invalid_data)
        self.assertEqual(response_tenant_profile.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_landlord_profile.status_code, status.HTTP_400_BAD_REQUEST)


class ProfilesDeleteTest(APITestCase):
    fixtures = ['fixtures/users.json']

    def test_delete_tenant_profile(self) -> None:
        tenants_count = TenantProfile.objects.all().count()
        landlord_count = LandlordProfile.objects.all().count()
        response_tenant_profile = self.client.delete(reverse('users:retrieve-update-delete-tenant',
                                                             kwargs={'pk': 2}))
        response_landlord_profile = self.client.delete(reverse('users:retrieve-update-delete-landlord',
                                                               kwargs={'pk': 3}))
        self.assertEqual(response_tenant_profile.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TenantProfile.objects.all().count(), tenants_count - 1)

        self.assertEqual(response_landlord_profile.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(LandlordProfile.objects.all().count(), landlord_count - 1)


class ProfilesFilteringTest(APITestCase):
    fixtures = ['fixtures/users.json']

    def test_birth_date_range(self) -> None:
        date_from = '1982-01-01'
        date_until = '1993-01-01'
        response = self.client.get(reverse('users:list-create-tenant'),
                                   {'birth_date__range': f'{date_from},{date_until}'})
        for i in response.data['results']:
            self.assertGreaterEqual(dict(i)['birth_date'], date_from)
            self.assertLessEqual(dict(i)['birth_date'], date_until)

    def test_firstname_equality(self) -> None:
        name = 'Артем'
        user_in_db = 'Артем Теряев'
        response = self.client.get(reverse('users:list-create-tenant'), {'firstname': name})
        user = dict(response.data['results'][0])
        self.assertEqual(user['firstname'] + ' ' + user['lastname'], user_in_db)

    def test_firstname_contains(self) -> None:
        contains = 'сим'
        user_in_db = 'Максим Зотов'
        response = self.client.get(reverse('users:list-create-tenant'), {'firstname__icontains': contains})
        user = dict(response.data['results'][0])
        self.assertEqual(user['firstname'] + ' ' + user['lastname'], user_in_db)


class UserRegisterTest(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'test_username',
            'firstname': 'Sergey',
            'lastname': 'Zlatko',
            'middlename': 'Middlename',
            'birth_date': '1980-03-10',
            'password': '12345',
            'password2': '12345',
            'email': 'ser@gmail.com',
            'is_tenant': 'True',
            'is_landlord': 'False',
        }

        self.user_data_2 = {
            'username': 'test_username_2',
            'firstname': 'Pavel',
            'lastname': 'Berg',
            'middlename': 'Middlename',
            'birth_date': '1980-03-10',
            'password': '12345',
            'password2': '12345',
            'email': 'pav@gmail.com',
            'is_tenant': 'True',
            'is_landlord': 'True',
        }

    def test_user_can_register(self):
        response_register_profile = self.client.post(reverse('register'), self.user_data, format="json")
        self.assertEqual(response_register_profile.status_code, 200, response_register_profile.data)

    def test_user_cannot_register_with_no_data(self):
        response_register_profile = self.client.post(reverse('register'))
        self.assertEqual(response_register_profile.status_code, 400)
    
    def test_two_users(self):
        response_register_profile = self.client.post(reverse('register'), self.user_data, format="json")
        response_register_profile_2 = self.client.post(reverse('register'), self.user_data_2, format="json")
        self.assertEqual(response_register_profile.status_code, 200)

    def test_two_identical_users(self):
        with self.assertRaises(IntegrityError):
            self.client.post(reverse('register'), self.user_data, format="json")
            self.client.post(reverse('register'), self.user_data, format="json")
