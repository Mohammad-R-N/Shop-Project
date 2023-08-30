from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from users.admin import CustomUserAdmin

User = get_user_model()

class CustomUserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()

        self.admin = CustomUserAdmin(User, self.site)

        self.user1 = User.objects.create_user(
            phone_number='09022631021',
            password='test_password',
            first_name='John',
            last_name='Doe',
            is_staff=True
        )

        self.user2 = User.objects.create_user(
            phone_number='09123456789',
            password='test_password',
            first_name='Jane',
            last_name='Doe',
            is_staff=False
        )

    def test_list_display(self):
        self.assertEqual(
            list(self.admin.get_list_display(None)),
            ['phone_number', 'first_name', 'last_name', 'is_staff']
        )

    def test_search_fields(self):
        self.assertEqual(
            self.admin.get_search_fields(None),
            ('phone_number', 'first_name', 'last_name')
        )

    def test_ordering(self):
        self.assertEqual(
            self.admin.get_ordering(None),
            ('phone_number',)
        )

    def test_fieldsets(self):
        request = self.factory.get('/')
        request.user = self.user1

        fieldsets = list(self.admin.get_fieldsets(request, self.user1))
        self.assertEqual(
            fieldsets,
            [
                (None, {'fields': ('phone_number', 'password')}),
                ('Personal info', {'fields': ('first_name', 'last_name')}),
                (
                    'Permissions',
                    {
                        'fields': (
                            'is_active',
                            'is_staff',
                            'is_superuser',
                            'groups',
                            'user_permissions',
                        ),
                    },
                ),
                ('Important dates', {'fields': ('lastlogin', 'date_joined')}),
            ]
        )

        fieldsets = list(self.admin.get_fieldsets(request, self.user2))
        self.assertEqual(
            fieldsets,
            [
                (None, {'fields': ('phone_number', 'password')}),
                ('Personal info', {'fields': ('first_name', 'last_name')}),
                (
                    'Permissions',
                    {
                        'fields': (
                            'is_active',
                            'is_staff',
                            'is_superuser',
                            'groups',
                            'user_permissions',
                        ),
                    },
                ),
                ('Important dates', {'fields': ('lastlogin', 'date_joined')}),
            ]
        )

    def test_add_fieldsets(self):
        add_fieldsets = list(self.admin.add_fieldsets)
        self.assertEqual(
            add_fieldsets,
            [
                (
                    None,
                    {'classes': ('wide',), 'fields': ('phone_number', 'password1', 'password2')}
                )
            ]
        )