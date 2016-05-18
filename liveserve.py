"""A simple command-line LiveReload server using the excellent
`python-livereload` library.
"""

import click
import livereload
import fnmatch
import os
import time

__version__ = '1.2.0'

POLL_DELAY = 1.0


def fnmatch_any(filename, pattern):
    """Test whether `filename` or any of its parent directories match
    the glob pattern.
    """
    while filename:
        # Try the current filename.
        if fnmatch.fnmatch(filename, pattern):
            return True

        # Try its parent directory.
        parent = os.path.dirname(filename)
        if parent == filename:
            break
        filename = parent

    # No matches.
    return False


@click.command()
@click.option('--host', '-h', default='127.0.0.1', metavar='HOST',
              help='Hostname to run the server on')
@click.option('--port', '-p', default=35729, metavar='PORT',
              help='Port to run the server on')
@click.argument('servedir', default='.', metavar='DIR',
                type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('--watch', '-w', multiple=True, type=click.Path(),
              help='File or directory to watch')
@click.option('--exec', '-x', 'command', metavar='COMMAND',
              help='Run a shell command on change')
@click.option('--ignore', '-i', metavar='PATTERN', multiple=True,
              help='Ignore paths with a glob pattern')
@click.option('--no-serve', '-S', 'serve', is_flag=True, default=True,
              help='Do not start an HTTP server')
def liveserve(host, port, servedir, watch, command, ignore, serve):
    """Run a LiveReload HTTP server.
    """
    # If the user doesn't give us any explicit files to watch, watch the
    # served directory.
    if not watch:
        watch = (servedir,)

    # Keyword arguments to `server.watcher.watch`.
    watchargs = {}
    if command:
        watchargs['func'] = livereload.shell(command)
    for pat in ignore:
        watchargs['ignore'] = lambda path: fnmatch_any(path, pat)

    # Set up the server, if any, or just create a watcher.
    if serve:
        server = livereload.Server()
        watcher = server.watcher
    else:
        watcher = livereload.watcher.get_watcher_class()()

    # Bind the watcher.
    for path in watch:
        watcher.watch(path, **watchargs)

    # Finally, launch the server (or watcher).
    if serve:
        server.serve(host=host, port=port, root=servedir)
    else:
        if not watcher.start(lambda: None):
            # Filesystem events not available; use polling.
            while True:
                path, _ = watcher.examine()
                if path:
                    print('changed:', path)
                time.sleep(POLL_DELAY)


if __name__ == '__main__':
    liveserve()
