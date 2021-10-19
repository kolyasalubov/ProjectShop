from django.test import TestCase
from UserApp.forms import RegisterForm, EditForm, LoginForm
from UserApp.tests.factories import UserFactory


class TestForms(TestCase):
    def test_RegisterForm_valid_data(self):
        user = UserFactory.build()
        form = RegisterForm(data={
            'email' : user.email,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'phone_number' : user.phone_number,
            'birth_date' : user.birth_date,
            'password1' : 'ValidPassword1@',
            'password2' : 'ValidPassword1@'
        })

        self.assertTrue(form.is_valid())
        print(form.errors)
        
    def test_RegisterForm_invalid_data(self):
        form = RegisterForm(data={
            'email' : '',
            'first_name' : '',
            'last_name' : '',
            'phone_number' : '',
            'birth_date' : '',
            'password1' : '',
            'password2' : ''
        })

        self.assertFalse(form.is_valid())

    def test_RegisterForm_no_data(self):
        form = RegisterForm(data={})

        self.assertFalse(form.is_valid())

    def test_EditForm_valid(self):
        user = UserFactory.build()
        form = EditForm(data={
            'phone_number' : user.phone_number,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'birth_date' : user.birth_date

        })
        self.assertTrue(form.is_valid())

    def test_EditForm_invalid_data(self):
        form = EditForm(data={
            'phone_number' : '',
            'first_name' : '',
            'last_name' : '',
            'birth_date' : ''
        })

        self.assertFalse(form.is_valid())

    def test_EditForm_no_data(self):
        form = EditForm(data={})

        self.assertFalse(form.is_valid())

    def test_LoginForm_valid_email(self):
        user = UserFactory()
        form = LoginForm(data={
            'username' : user.email,
            'password' : '1234'
        })

        self.assertTrue(form.is_valid())

    def test_LoginForm_valid_phone(self):
        user = UserFactory()
        form = LoginForm(data={
            'username' : user.phone_number,
            'password' : 'ValidPassword1@'
        })

        self.assertTrue(form.is_valid())

    def test_LoginForm_valid_email(self):
        user = UserFactory()
        form = LoginForm(data={
            'username' : user.email,
            'password' : 'ValidPassword1@'
        })

        self.assertTrue(form.is_valid())
    
    def test_LoginForm_invalid_data(self):
        user = UserFactory()
        form = LoginForm(data={
            'username' : '',
            'password' : ''
        })
        self.assertFalse(form.is_valid())

    def test_LoginForm_no_data(self):
        user = UserFactory()
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
