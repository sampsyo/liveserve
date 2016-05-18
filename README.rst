liveserve
=========

A tiny command-line script for `python-livereload`_.

Compared to the `livereload` script that ships with the original package, this
tool adds:

* Serve from a non-watched directory.
* Watch multiple directories.
* Run a shell command when files change.

Together, this makes it suited for serving pages that need to be built from
source: documentation, static sites, and so on.

.. _python-livereload: https://github.com/lepture/python-livereload


Usage
-----

::

    liveserve [-h HOST] [-p PORT] [-w PATH ...] [-c COMMAND] [DIR]

* `-h` or `--host`: The server's hostname.
* `-p` or `--port`: The server's port.
* `-w` or `--watch`: A file or directory to watch for changes. Specify as many
  as you like; if none are specified, defaults to the server root.
* `-x` or `--exec`: A shell command to execute when files change.
* `-i` or `--ignore`: Exclude files from the watch list using a glob pattern.
* `-S` or `--no-serve`: Do not start a Web server; just watch for changes and
  execute commands.
* The optional positional argument the directory to serve. Defaults to the
  working directory.


Credits
-------

By `Adrian Sampson`_. The license is `MIT`_.

.. _Adrian Sampson: http://adriansampson.net/
.. _MIT: http://choosealicense.com/licenses/mit/
