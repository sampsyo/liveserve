"""A simple command-line LiveReload server using the excellent
`python-livereload` library.
"""

import click
import livereload

__version__ = '1.0.0'


@click.command()
@click.option('--host', '-h', default='127.0.0.1',
              help='Hostname to run the server on')
@click.option('--port', '-p', default=35729,
              help='Port to run the server on')
@click.argument('servedir', default='.',
                type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('--watch', '-w', multiple=True, type=click.Path(),
              help='File or directory to watch')
@click.option('--exec', '-x', 'command',
              help='Run a shell command on change')
def liveserve(host, port, servedir, watch, command):
    """Run a LiveReload HTTP server.
    """
    # If the user doesn't give us any explicit files to watch, watch the
    # served directory.
    if not watch:
        watch = (servedir,)

    # Set up and run the server.
    server = livereload.Server()
    for path in watch:
        if command:
            server.watcher.watch(path, livereload.shell(command))
        else:
            server.watcher.watch(path)
    server.serve(host=host, port=port, root=servedir)


if __name__ == '__main__':
    liveserve()
