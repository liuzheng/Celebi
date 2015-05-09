# Celebi
Release Operation and Maintenance Engineer

# Install requirements.txt

    pip install requirements.txt

# Install django-socketio
============

Note that if you've never installed gevent, you'll first need to
install the libevent development library. You may also need the Python
development library if not installed. This can be achieved on Debian
based sytems with the following commands::

    $ sudo apt-get install python-dev
    $ sudo apt-get install libevent-dev

or on OSX using `Homebrew`_ (with Xcode installed)::

    $ brew install libevent
    $ export CFLAGS=-I/brew/include

or on OSX using `macports`::

    $ sudo port install libevent
    $ CFLAGS="-I /opt/local/include -L /opt/local/lib" pip install django-socketio

The easiest way to install django-socketio is directly from PyPi using
`pip`_ by running the following command, which will also attempt to
install the dependencies mentioned above::

    $ pip install -U django-socketio

Otherwise you can download django-socketio and install it directly
from source::

    $ python setup.py install
