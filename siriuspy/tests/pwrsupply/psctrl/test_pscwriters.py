"""Test fields module."""
from unittest import TestCase

from siriuspy.pwrsupply.psctrl.pscwriters import Setpoint


class TestSetpointMatch(TestCase):
    """Test setpoint match."""

    def test_match_sp(self):
        """Test sp."""
        self.assertTrue(Setpoint.match('Fake-SP'))

    def test_match_sel(self):
        """Test sel."""
        self.assertTrue(Setpoint.match('Fake-Sel'))

    def test_match_cmd(self):
        """Test cmd."""
        self.assertTrue(Setpoint.match('Fake-Cmd'))

    def test_match_strange(self):
        """Test strange fields."""
        self.assertFalse(Setpoint.match('Fake-RB'))
        self.assertFalse(Setpoint.match('Fake-Sts'))


class TestCmdSetpoint(TestCase):
    """Test setpoint class."""

    def setUp(self):
        """Define common setup."""
        self.field = 'Fake-Cmd'
        self.dbase = {'type': 'int', 'value': 0}
        self.setpoint = Setpoint(self.field, self.dbase)

    def test_apply_returns_false(self):
        """Test apply setpoint with value 0 returns false."""
        self.assertFalse(self.setpoint.apply(0))
        self.assertFalse(self.setpoint.apply(-1))

    def test_apply_returns_true(self):
        """Test apply setpoint with value > 0 returns True."""
        self.assertTrue(self.setpoint.apply(1))
        self.assertTrue(self.setpoint.apply(10))

    def test_apply_increment_value(self):
        """Test apply increments setpoint by 1."""
        self.assertEqual(self.setpoint.value, 0)
        self.setpoint.apply(1)
        self.assertEqual(self.setpoint.value, 1)
        self.setpoint.apply(1)
        self.assertEqual(self.setpoint.value, 2)


class TestPSetpoint(TestCase):
    """Test setpoints sp."""

    def setUp(self):
        """Common setup."""
        self.field = 'Fake-SP'
        self.dbase = {'type': 'float',
                   'value': 0.0,
                   'lolo': -10.0,
                   'hihi': 10.0}
        self.setpoint = Setpoint(self.field, self.dbase)

    def test_init(self):
        """Test constructor."""
        self.assertEqual(self.setpoint.value, 0.0)
        self.assertEqual(self.setpoint.field, self.field)
        self.assertEqual(self.setpoint.database, self.dbase)
        self.assertFalse(self.setpoint.is_cmd)
        self.assertEqual(self.setpoint.type, 'float')
        self.assertIsNone(self.setpoint.count)
        self.assertEqual(self.setpoint.enums, None)
        self.assertEqual(self.setpoint.low, -10.0)
        self.assertEqual(self.setpoint.high, 10.0)

    def test_apply_above_limit(self):
        """Test apply setpoint with value above limit returns false."""
        self.assertEqual(self.setpoint.value, 0.0)
        self.assertFalse(self.setpoint.apply(11.0))
        self.assertEqual(self.setpoint.value, 0.0)

    def test_apply_below_limit(self):
        """Test apply setpoint with value below limit returns false."""
        self.assertEqual(self.setpoint.value, 0.0)
        self.assertFalse(self.setpoint.apply(-11.0))
        self.assertEqual(self.setpoint.value, 0.0)

    def test_apply_returns_true(self):
        """Test apply setpoint with value > 0 returns True."""
        self.assertEqual(self.setpoint.value, 0.0)
        self.assertTrue(self.setpoint.apply(9.0))
        self.assertEqual(self.setpoint.value, 9.0)


class TestSelSetpoint(TestCase):
    """Test sel setpoints."""

    def setUp(self):
        """Common setup."""
        self.field = 'Fake-Sel'
        self.dbase = {'type': 'enum',
                   'value': 0,
                   'enums': ('StateA', 'StateB', 'StateC')}
        self.setpoint = Setpoint(self.field, self.dbase)

    def test_init(self):
        """Test constructor."""
        self.assertEqual(self.setpoint.value, 0)
        self.assertEqual(self.setpoint.field, self.field)
        self.assertEqual(self.setpoint.database, self.dbase)
        self.assertFalse(self.setpoint.is_cmd)
        self.assertEqual(self.setpoint.type, 'enum')
        self.assertIsNone(self.setpoint.count)
        self.assertEqual(self.setpoint.enums, ('StateA', 'StateB', 'StateC'))
        self.assertEqual(self.setpoint.low, None)
        self.assertEqual(self.setpoint.high, None)

    def test_apply_above_limit(self):
        """Test apply setpoint out of range."""
        self.assertEqual(self.setpoint.value, 0)
        self.assertFalse(self.setpoint.apply(4))
        self.assertEqual(self.setpoint.value, 0)

    def test_apply_below_limit(self):
        """Test apply setpoint out of range."""
        self.assertEqual(self.setpoint.value, 0)
        self.assertFalse(self.setpoint.apply(-1))
        self.assertEqual(self.setpoint.value, 0)

    def test_apply(self):
        """Test apply with value in range."""
        self.assertEqual(self.setpoint.value, 0)
        self.setpoint.apply(1)
        self.assertEqual(self.setpoint.value, 1)
