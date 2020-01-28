from unittest import TestCase

from parameterized import parameterized
import pytest

import models.user as module
from tests import OhmTestCase


class UserTest(OhmTestCase):
    def test_get_multi(self):
        assert self.chuck.get_multi("PHONE") == ['+14086441234', '+14086445678']
        assert self.justin.get_multi("PHONE") == []

    def test_is_below_tier_on_user(self):
        # Initial data sets Chuck as Carbon
        assert self.chuck.is_below_tier("Silver")
        # Migration 20200128094752_adjust_test_users sets Justin as Silver
        assert not self.justin.is_below_tier("Silver")


class IsBelowTierTest(TestCase):
    @parameterized.expand([
        ('Gold', 'Gold', False),
        ('Gold', 'Silver', False),
        ('Gold', 'Platinum', True),
        ('Silver', 'Platinum', True),
    ])
    def test_is_below_tier(self, user_tier, threshold_tier, expected):
        assert module._is_below_tier(user_tier, threshold_tier) == expected

    @parameterized.expand([
        ('not a tier, buddy', 'Gold'),
        ('Gold', 'not a tier either'),
        ('gold', 'platinum'), # lowercase = not OK
    ])
    def test_is_below_tier_invalid_inputs_blows_up(self, user_tier, threshold_tier):
        with pytest.raises(KeyError):
            module._is_below_tier(user_tier, threshold_tier)