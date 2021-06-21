from pathlib import Path
from typing import Union
from urllib.parse import urlparse, urlunparse

import related  # type: ignore


@related.immutable
class Host(object):
    name = related.StringField()
    host = related.StringField()
    note = related.StringField(required=False)
    icon = related.StringField(required=False)
    badge = related.StringField(required=False)

    @property
    def href(self) -> str:
        scheme, netloc, path, params, query, fragment = urlparse(self.host)

        if not scheme:
            scheme = "https"

        return urlunparse([scheme, netloc, path, params, query, fragment])


@related.immutable
class Category(object):
    title = related.StringField()
    hosts = related.SequenceField(Host)


@related.immutable
class Dashboard(object):
    title = related.StringField()
    categories = related.SequenceField(Category)


def load_dashboard(yaml_file: Union[str, Path], encoding="utf-8") -> Dashboard:
    """
    De-serialize a YAML file into a Dashboard instance.
    @param yaml_file:
    @param encoding: Optional file encoding of the input file
    @return: De-serialized Dashboard instance
    """
    # Make sure the file exists
    yaml_file = Path(yaml_file)
    if not yaml_file.is_file():
        raise FileNotFoundError(yaml_file)

    with open(yaml_file, "r", encoding=encoding) as fd:
        dashboard_dict = related.from_yaml(fd.read())
        dashboard = related.to_model(Dashboard, dashboard_dict)
        return dashboard
