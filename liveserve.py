"""A simple command-line LiveReload server using the excellent
`python-livereload` library.
"""

import click
import livereload
from fnmatch import fnmatch

__version__ = '1.1.0'


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
def liveserve(host, port, servedir, watch, command, ignore):
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
        watchargs['ignore'] = lambda path: fnmatch(path, pat)

    # Set up and run the server.
    server = livereload.Server()
    for path in watch:
        server.watcher.watch(path, **watchargs)
    server.serve(host=host, port=port, root=servedir)


if __name__ == '__main__':
    liveserve()
