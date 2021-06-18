import http
import http.server
import socketserver
import sys
from pathlib import Path

from renderer.cli import parse_args
from renderer.model import load_dashboard
from renderer.site import Site


def build(input_file: Path, input_directory: Path, build_dir: Path) -> int:
    dashboard = load_dashboard(input_file)
    site = Site(input_directory, build_dir=build_dir)
    site.build(dashboard)
    print("Build files were written to:", site.build_dir.absolute())
    return 0


def serve(build_dir: Path, host: str = "127.0.0.1", port: int = 5000) -> int:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=build_dir, **kwargs)

    with socketserver.TCPServer((host, port), Handler) as httpd:
        print(f"Serving on http://{host}:{port}")

        try:
            httpd.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            httpd.server_close()
            httpd.socket.close()

    return 0


def main() -> int:
    namespace = parse_args()

    command = namespace.command
    if command == "build":
        return build(namespace.input_file, namespace.directory, namespace.build_dir)
    elif command == "server":
        return serve(namespace.build_dir)
    else:
        print(f"Invalid command: {command}", file=sys.stderr)
        return -2


if __name__ == "__main__":
    sys.exit(main())
