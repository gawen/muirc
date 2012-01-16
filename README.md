The ``muirc`` module
====================

``muirc`` is a minimalist & efficient Python module to parse & create IRC messages. It does the job, and only the job, in a Pythonic way.

Parse & create IRC messages
---------------------------

The module's name is ``muirc``.

    import muirc

The main function is ``transform``, which can either parse a raw IRC message and returns an dictionary whose keys are the fields of the message ...

    >>> muirc.translate("PRIVMSG #irc :Hello, World! :-)\r\n")
    {'nick': None, 'host': None, 'command': 'PRIVMSG', 'user': None, 'params': ['#irc', 'Hello, World! :-)']}

... or parse a dictionary with IRC message's fields and returns a raw IRC message.

    >>> muirc.translate({'nick': None, 'host': None, 'command': 'PRIVMSG', 'user': None, 'params': ['#irc', 'Hello, World! :-)']})
    'PRIVMSG #irc :Hello, World! :-)\r\n'

Applying ``transform`` twice returns the same object

    >>> muirc.translate(muirc.translate("PRIVMSG #irc :Hello, World! :-)\r\n"))
    'PRIVMSG #irc :Hello, World! :-)\r\n'

    >>> muirc.translate(muirc.translate({'nick': None, 'host': None, 'command': 'PRIVMSG', 'user': None, 'params': ['#irc', 'Hello, World! :-)']}))
    {'nick': None, 'host': None, 'command': 'PRIVMSG', 'user': None, 'params': ['#irc', 'Hello, World! :-)']}

Some more advance example

    >>> muirc.translate(":nick!user@host PRIVMSG #irc :Hello, World! :-)")
    {'nick': 'nick', 'host': 'host', 'command': 'PRIVMSG', 'user': 'user', 'params': ['#irc', 'Hello, World! :-)']}

    >>> muirc.translate(muirc.translate(":nick!user@host PRIVMSG #irc :Hello, World! :-)"))
    ':nick!user@host PRIVMSG #irc :Hello, World! :-)\r\n'

Connect to IRC server
---------------------

A ``Connection`` class is provided to interact with an IRC node. It can be used either to build a IRC client or server.

Create a connection giving a 2-tuple ``(host, port)``.

    >>> conn = muirc.Connection(("irc.freenode.net", 6667))

Proxy methods are provided to easily send IRC messages. The case is not important.

    >>> conn.nick("muirc")
    >>> conn.UsEr("a", "a", "a", "a")

This class provides an iterator interface which yields a parsed object every time a IRC message is received. This option provides an easy&pythonic way to create an simple IRC client.

The following example connects to FreeNode, join #muirc and send a hello world message.

    >>> state = "wait_motd"
    >>> for message in conn:
    ...     if state == "wait_motd":
    ...         # 376 => MOTD ends
    ...         if message["command"] == "376":
    ...             state = "end_motd"
    ...
    ...     # Join #muirc
    ...     if state == "end_motd":
    ...         conn.join("#muirc")
    ...         state = "wait_join"
    ...
    ...     # Wait for join ack
    ...     if state == "wait_join":
    ...         if message["command"] == "JOIN":
    ...                state = "hello_world"
    ...
    ...     # Send "Hello, World! :-)" to the #muirc channel
    ...     if state == "hello_world":
    ...         conn.privmsg("#muirc", "Hello, World! :-)")
    ...         state = "quit"
    ...
    ...     # Quit
    ...     if state == "quit":
    ...         conn.quit("Bye, World! :-(")
    ...         print "OK"
    ...         break
    OK
