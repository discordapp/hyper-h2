# -*- coding: utf-8 -*-
"""
test_basic_logic
~~~~~~~~~~~~~~~~

Test the basic logic of the h2 state machines.
"""
import h2.connection

from hyperframe import frame


class TestBasicConnection(object):
    """
    Basic connection tests.
    """
    example_request_headers = [
        (':authority', 'example.com'),
        (':path', '/'),
        (':scheme', 'https'),
        (':method', 'GET'),
    ]

    def test_begin_connection(self):
        c = h2.connection.H2Connection()
        frames = c.send_headers_on_stream(1, self.example_request_headers)
        assert len(frames) == 1

    def test_sending_some_data(self):
        c = h2.connection.H2Connection()
        frames = c.send_headers_on_stream(1, self.example_request_headers)
        frames.append(c.send_data_on_stream(1, b'test', end_stream=True))
        assert len(frames) == 2

    def test_receive_headers_frame(self):
        f = frame.HeadersFrame(1)
        f.data = b'fake headers'
        f.flags = set(['END_STREAM', 'END_HEADERS'])

        c = h2.connection.H2Connection()
        assert c.receive_frame(f) is None