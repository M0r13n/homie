from renderer.model import load_dashboard
from renderer.site import Site

if __name__ == "__main__":
    dashboard = load_dashboard("example/example.yaml")
    site = Site()
    site.build(dashboard)
