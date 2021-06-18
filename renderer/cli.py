import argparse
from pathlib import Path


def path(path_str: str) -> Path:
    p = Path(path_str)
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"{path_str} is not a directory")
    return p


def file(file_str: str) -> Path:
    p = Path(file_str)
    if p.is_absolute() and not p.is_file():
        raise argparse.ArgumentTypeError(f"{p.name} could not be found.")
    return p


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Builds a simple static site.")

    parser.add_argument(
        "-o",
        "--out",
        default="build",
        dest="build_dir",
        help="Define an output dir. Default is build",
        type=str
    )

    subparsers = parser.add_subparsers(help="Commands", dest="command", required=True)

    build_parser = subparsers.add_parser("build")

    build_parser.add_argument(
        "-d",
        "--directory",
        default=Path.cwd(),
        help="Define an input file directory (default is cwd)",
        type=path
    )

    build_parser.add_argument(
        "-f",
        "--file",
        dest="input_file",
        help="Define the input file. Default dashboard.yaml",
        type=file,
        default="dashboard.yaml"
    )

    subparsers.add_parser("server")

    namespace = parser.parse_args()

    if namespace.command == "build":
        # Validate relative file names
        if not namespace.input_file.is_absolute():
            input_file: Path = namespace.directory.joinpath(namespace.input_file)
            if not input_file.is_file():
                parser.error(f"{input_file.name} was not found in {input_file.parent}")

            namespace.input_file = input_file

    return namespace
