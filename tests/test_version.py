# -*- coding: utf-8 -*-
from django.test import TestCase

from django_stripe import get_version


class DjangoStripeVersionTests(TestCase):

    def test_patch_number_is_str(self):
        result = get_version((0, 1, 'pre'))

        self.assertEqual(result, '0.1_pre')

    def test_patch_number_is_int(self):
        result = get_version((0, 1, 0))

        self.assertEqual(result, '0.1.0')

    def test_no_patch_number(self):
        result = get_version((0, 1))

        self.assertEqual(result, '0.1')
