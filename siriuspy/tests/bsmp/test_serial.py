#!/usr/bin/env python-sirius

"""Test serial module."""

from unittest import TestCase
from unittest.mock import Mock
from siriuspy.bsmp import SerialErrMsgShort, SerialErrPckgLen
from siriuspy.bsmp import Message, Package, Channel, SerialError
from siriuspy.util import check_public_interface_namespace


class TestBSMPMessage(TestCase):
    """Test BSMP Message class."""

    api = (
        'message',
        'stream',
        'cmd',
        'size',
        'payload',
    )

    def test_api(self):
        """Test API."""
        self.assertTrue(check_public_interface_namespace(Message, self.api))

    def test_init(self):
        """Test constructor that creates object from stream."""
        stream = ['\x01', '\x00', '\x03', '\x02', '\n', '\x00']
        m = Message(stream)
        # Check properties
        self.assertEqual(m.cmd, 0x01)
        self.assertEqual(m.payload, [chr(2), chr(10), chr(0)])
        # Convert message to stream
        self.assertEqual(m.stream, stream)

    def test_small_message(self):
        """Test message with stream impossibly small."""
        with self.assertRaises(SerialErrMsgShort):
            Message(['\x11', '\x00'])

    def test_message_with_no_load(self):
        """Test constructor with no load."""
        m = Message.message(cmd=0x00)
        self.assertEqual(m.cmd, 0x00)
        self.assertEqual(m.payload, [])

    def test_message_with_load(self):
        """Test constructor with load."""
        m = Message.message(cmd=0x10, payload=[1, ])
        self.assertEqual(m.cmd, 0x10)
        self.assertEqual(m.payload, [1, ])

    def test_message_with_extraneous_load(self):
        """Test constructor with loads that are not list."""
        loads = [1, 'string', (1, 2, 3), 63.7]
        for load in loads:
            with self.assertRaises(TypeError):
                Message.message(cmd=0x10, payload=load)

    def test_message_with_big_load(self):
        """Test constructor with load bigger than 65535."""
        load = [0 for _ in range(65536)]
        with self.assertRaises(ValueError):
            Message.message(cmd=0x10, payload=load)

    def test_conv_to_stream(self):
        """Test conversion from message to stream."""
        # Example in 3.8.2 of BSMP protocol document
        curve_id = chr(0x07)
        blk_n = [chr(0x40), chr(0x00)]
        blk_load = [chr(0xdd) for _ in range(16384)]
        load = [curve_id] + blk_n + blk_load
        m = Message.message(cmd=0x41, payload=load)

        expected_stream = [chr(0x41), chr(0x40), chr(0x03)] + load

        self.assertEqual(m.stream, expected_stream)


class TestBSMPPackage(TestCase):
    """Test BSMP Package class."""

    # Tuples with address, message and checksum
    data = [
        (1, 0x10, [chr(3)], ['\x01', '\x10', '\x00', '\x01', '\x03',
         chr(235)], 235),
        (0, 0x11, [chr(3), chr(255), chr(255)],
         ['\x00', '\x11', '\x00', '\x03', '\x03', '\xFF', '\xFF', chr(235)],
         235),
        (2, 0x20, [chr(4), chr(1), chr(187), chr(187)],
         ['\x02', '\x20', '\x00', '\x04', '\x04', '\x01', '\xBB', '\xBB',
          chr(95)], 95),
        (3, 0x22, [chr(2), chr(1), chr(187), chr(187), chr(1),
         chr(187), chr(187), chr(1), chr(187), chr(187), chr(1), chr(187),
         chr(187), chr(204)],
         ['\x03', '\x22', '\x00', '\x0E', '\x02', '\x01', '\xBB', '\xBB',
          '\x01', '\xBB', '\xBB', '\x01', '\xBB', '\xBB', '\x01', '\xBB',
          '\xBB', '\xCC', chr(35)], 35),
    ]

    api = (
        'package',
        'address',
        'message',
        'checksum',
        'stream',
        'calc_checksum',
        'verify_checksum',
    )

    def test_api(self):
        """Test API."""
        self.assertTrue(check_public_interface_namespace(Package, self.api))

    def test_package(self):
        """Test constructor."""
        address = 1
        m = Message.message(0x00)
        p = Package.package(address=address, message=m)

        self.assertEqual(p.address, address)
        self.assertEqual(p.message, m)

    def test_package_stream(self):
        """Test constructor that creates object from stream."""
        for d in self.data:
            stream = d[3]
            p = Package(stream)
            self.assertEqual(p.address, d[0])
            self.assertEqual(p.message.cmd, d[1])
            self.assertEqual(p.message.payload, d[2])

    def test_parse_small_stream(self):
        """Test constructor that tries to parse strem smaller than 5."""
        stream = ['\x02', '\x00', '\x00', chr(254)]
        with self.assertRaises(SerialErrPckgLen):
            Package(stream)

    def test_checksum(self):
        """Test checksum value."""
        for d in self.data:
            p = Package.package(d[0], Message.message(d[1], payload=d[2]))
            self.assertEqual(p.checksum, d[4])

    def test_conv_to_stream(self):
        """Test conversion of package to stream."""
        for d in self.data:
            p = Package.package(d[0], Message.message(d[1], payload=d[2]))
            self.assertEqual(p.stream, d[3])

    def test_verify_checksum(self):
        """Verify checksum sucessfully."""
        for d in self.data:
            stream = d[3]
            self.assertTrue(Package.verify_checksum(stream))

    def test_verify_false_checksum(self):
        """Verify checksums fail."""
        for d in self.data:
            stream, checksum = d[3][:-1], ord(d[3][-1])
            stream += [chr(checksum + 1)]
            self.assertFalse(Package.verify_checksum(stream))


class TestBSMPChannel(TestCase):
    """Test Channel class of BSMP package."""

    api = (
        'LOCK',
        'pru',
        'address',
        'read',
        'write',
        'request',
        'size_counter',
        'size_counter_reset',)

    def setUp(self):
        """Common setup for all tests."""
        self.serial = Mock()
        self.channel = Channel(self.serial, 1)

    def test_api(self):
        """Test API."""
        self.assertTrue(check_public_interface_namespace(Channel, self.api))

    def test_read_calls_serial_method(self):
        """Test UART_read is called."""
        response = Message.message(0x11, payload=[chr(10)])
        self.serial.UART_read.return_value = \
            Package.package(0x01, response).stream
        self.channel.read()
        self.serial.UART_read.assert_called_once()

    def test_read(self):
        """Test read method."""
        response = Message.message(0x11, payload=[chr(10)])
        self.serial.UART_read.return_value = \
            Package.package(0x01, response).stream
        recv = self.channel.read()
        self.assertEqual(recv.cmd, response.cmd)
        self.assertEqual(recv.payload, response.payload)

    def test_write_calls_serial_method(self):
        """Test write calls UART_write."""
        message = Message.message(0x10, payload=[chr(1)])
        expected_stream = \
            Package.package(self.channel.address, message).stream
        self.channel.write(message, 1000)
        self.serial.UART_write.assert_called_with(
            expected_stream, timeout=1000)

    def test_request(self):
        """Test request."""
        response = Message.message(0x11, payload=[chr(10)])
        self.serial.UART_read.return_value = \
            Package.package(0x01, response).stream
        recv = self.channel.request(
            Message.message(0x01, payload=[chr(1)]), timeout=1)
        self.assertEqual(recv.cmd, response.cmd)
        self.assertEqual(recv.payload, response.payload)

    def test_request_fail(self):
        """Test exception is raised when serial fails."""
        self.serial.UART_read.return_value = None
        with self.assertRaises(SerialError):
            self.channel.request(Message.message(0x10, payload=[chr(10)]))
