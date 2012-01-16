#!/usr/bin/env python

__author__ = "Gawen Arab"
__copyright__ = "Copyright 2012, Gawen Arab"
__credits__ = ["Gawen Arab"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Gawen Arab"
__email__ = "g@wenarab.com"
__status__ = "Production"

import re
import socket
import select
import threading

__all__ = ["translate", "Connection"]

IRC_RE = re.compile(r"(:(?P<nick>[^ !@]+)(\!(?P<user>[^ @]+))?(\@(?P<host>[^ ]+))? )?(?P<command>[^ ]+) (?P<params1>([^:]*))(?P<params2>(:.*)?)")

def translate(m):
    if isinstance(m, basestring):
        # str -> msg
        m = IRC_RE.match(m.strip())

        if not m:
            return None

        m = m.groupdict()

        m["params"] = m.pop("params1").split()
        if m["params2"]:    m["params"] += [m["params2"][1:]]
        m.pop("params2")

        return m

    else:
        # msg -> str
        def gen():
            if m.get("nick", None):
                yield ":" + m["nick"]
                if m.get("user", None):   yield "!" + m["user"]
                if m.get("host", None):   yield "@" + m["host"]
                yield " "

            yield m["command"]
            
            if m.get("params", None):
                for param in m["params"][:-1]:  yield " " + param

                yield " "
                if " " in m["params"][-1]:  yield ":"
                yield m["params"][-1]

            yield "\r\n"

        return "".join(gen())

class Connection(object):
    def __new__(cls, o):
        if isinstance(o, cls) or o is None:
            return o
        
        self = super(Connection, cls).__new__(cls)
        
        if isinstance(o, (tuple, list, )) and len(o) == 2:
            o = socket.create_connection(o)

        assert isinstance(o, socket.socket)
        self.s = o
        self.s_in = self.s.makefile("r")
        self.s_out = self.s.makefile("w")
        self.write_lock = threading.Lock()

        return self

    def _send(self, m):
        self.s_out.write(translate(m))
        self.s_out.flush()

    def _recv(self, timeout = None):
        if timeout is not None and self.sock not in select.select([self.sock], [], [], timeout)[0]:
            return None

        m = self.s_in.readline()
        return translate(m.strip()) if m else None

    def send(self, **m):
        """ Sends a IRC message. """
        with self.write_lock:
            return self._send(m)

    def recv(self, timeout = None):
        """ Receives a parsed IRC message. """
        return self._recv(timeout = timeout)

    def iter(self, timeout = None):
        """ Iterator interface providing an easy way to create process loops. """
        while True:
            r = self.recv(timeout)
            if not r: break
            yield r

    def __iter__(self):
        return self.iter()

    def __getattr__(self, command):
        """ If method is not found, returns a function proxy to send IRC commands. """
        def command_proxy(*args, **kwargs):
            return self.send(
                nick = kwargs.get("nick", None),
                user = kwargs.get("user", None),
                host = kwargs.get("host", None),
                command = command.upper(),
                params = args,
            )

        command_proxy.func_name = command
        return command_proxy

