# -*- coding: utf-8 -*-

from django.test import TestCase

from mock import patch
from django_dynamic_fixture import G
from override_settings import override_settings

from .models import Recipient, get_user_model
from .forms import RecipientsMixin, ContactMixin


class RecipientMixinTests(TestCase):

    def test_settings_recipients(self):
        """
        Ensure that the contact list consists of site manager email addresses
        """
        Recipient.objects.all().delete()
        managers = (('Bubba', 'bubba@gump.com'),)
        mix = RecipientsMixin()
        with override_settings(MANAGERS=managers):
            self.assertEqual(mix.recipient_list(), ['bubba@gump.com'])

    def test_database_recipients(self):
        """
        Ensure that the contact list consists of specified user email addresses
        """
        user1 = G(get_user_model(), is_staff=True)
        user2 = G(get_user_model(), is_staff=True)
        recipient1 = G(Recipient, user=user1)
        recipient2 = G(Recipient, user=user2)

        mix = RecipientsMixin()
        self.assertEqual(mix.recipient_list(),
                [user1.email, user2.email])


class EmailTests(TestCase):

    def test_ascii_subject(self):
        """Ensure the subject method cleans for UnicodeEncodeError"""
        with patch.object(ContactMixin, 'get_message_dict') as mocked:
            mocked.return_value = {'from_email': 'bubba@gump.com',
                    'message': 'Howdy', 'recipient_list': ['forrest@gump.com'],
                    'subject': 'רשלנות רפואית'}
            contacter = ContactMixin()
            contacter.send()


class ContactMixinTests(TestCase):

    def test_adding_attribute(self):
        """Ensure that a keyword matching an attribute updates it"""

        class TestBase(object):
            def __init__(self, *args, **kwargs):
                pass

        class TestForm(ContactMixin, TestBase):
            pass

        contacter = TestForm(subject_template_name="subject.txt")
        self.assertEqual(contacter.get_subject_template_name(), "subject.txt")
        contacter = TestForm(from_email="shuggah@lagunitas.com")
        self.assertEqual(contacter.from_email, "shuggah@lagunitas.com")
