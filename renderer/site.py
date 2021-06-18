import errno
import os
import shutil
from pathlib import Path
from typing import Union, Optional

from jinja2 import FileSystemLoader, Environment

from renderer.model import Dashboard

FILE_DIR = Path(__file__).parent.absolute()


class Site(object):
    """
    Site object used to generate the static site.

    @param template_dir: The directory where to search for template files.
    @param static_dir: The directory where to search for static files.
    @param build_dir: Where to write the generated files.
    @param encoding: Optional encoding (Default is UTF-8)
    """

    def __init__(
            self,
            input_dir: Path,
            build_dir: Union[str, Path] = "build",
            template_dir: Optional[Path] = None,
            static_dir: Optional[Path] = None,
            encoding: str = "utf-8"
    ):
        # Where to look for user files
        self.input_dir: Path = input_dir
        if not self.input_dir.is_dir():
            raise NotADirectoryError(self.input_dir)

        # The template and static directory are required to exist
        self.template_dir: Path = self._parse_relative_path(template_dir or "templates")
        if not self.template_dir.is_dir():
            raise NotADirectoryError(self.template_dir)

        self.static_dir: Path = self._parse_relative_path(static_dir or "static")
        if not self.static_dir.is_dir():
            raise NotADirectoryError(self.static_dir)

        self.build_dir: Path = Path(build_dir)

        self.encoding: str = encoding

        self.environment: Environment = self._make_environment()

    @staticmethod
    def _parse_relative_path(path: Union[str, Path]) -> Path:
        path = Path(path)
        if path.is_absolute():
            # Nothing to do for absolute paths
            return path

        # Relative path to current files folder
        return FILE_DIR.joinpath(path)

    def _make_environment(self) -> Environment:
        """
        Creates a Jinja2 Environment
        """
        # Create a file load, which will look for templates in the searchpath
        loader = FileSystemLoader(
            searchpath=self.template_dir,
            encoding=self.encoding,
            followlinks=True
        )
        environment = Environment(loader=loader)
        return environment

    def build_path(self, path: Union[str, Path]) -> Path:
        """
        Get the full path of an path relative to the current build dir.
        @param path: path relative to the build folder
        @return: Path object, that represents a full build path
        """
        path = Path(path)
        return self.build_dir.joinpath(Path(path))

    def clean_build_dir(self) -> None:
        """
        Remove the entire build folder, if it exists.
        This ensures a clean build.
        """
        try:
            shutil.rmtree(self.build_dir)
        except FileNotFoundError:
            # Do nothing, because the build directory does not exist
            pass

    def copy_static_folder(self) -> None:
        """
        Copy the entire static build directory into the build folder.
        @return:
        """
        target_dir = self.build_path("static")
        try:
            # Recursive copy
            shutil.copytree(self.static_dir, target_dir, )
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                # This may happen, so fall back to copy
                shutil.copy(self.static_dir, target_dir)
                return
            raise

    def copy_icon_folder(self) -> None:
        """
        Copy the entire icon folder into the build folder
        @return:
        """
        target_dir = self.build_path("static/icons")
        icon_dir = self.input_dir.joinpath("icons")

        if not icon_dir.is_dir():
            print("Warning: No icons dir found!")
            return

        try:
            # Recursive copy
            shutil.copytree(icon_dir, target_dir, )
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                # This may happen, so fall back to copy
                shutil.copy(icon_dir, target_dir)
                return
            raise

    def render(self, dashboard: Dashboard) -> None:
        """
        Render the html file for a given dashboard instance.
        @param dashboard: Dashboard instance
        """
        html_file = "index.html"
        tpl = self.environment.get_template(html_file)

        tpl.render(dashboard=dashboard)

        # Make sure the build path always exists
        os.makedirs(self.build_dir, exist_ok=True)

        # Open the final file in binary mode
        with open(self.build_path(html_file), "wb+") as fd:
            # Directly dump the rendered bytes
            tpl.stream(dashboard=dashboard).dump(fd, "utf-8")

    def build(self, dashboard: Dashboard) -> None:
        """
        Build the static site for a given dashboard instance.
        @param dashboard: Dashboard instance
        """
        self.clean_build_dir()
        self.render(dashboard)
        self.copy_static_folder()
        self.copy_icon_folder()
