import platform
from hyperdx.opentelemetry.options import HyperDXOptions
from hyperdx.opentelemetry.resource import create_resource
from hyperdx.opentelemetry.version import __version__


def test_default_resource():
    options = HyperDXOptions()
    resource = create_resource(options)
    assert resource._attributes["service.name"] == "unknown_service:python"
    assert "service.version" not in resource._attributes
    assert resource._attributes["hyperdx.distro.version"] == __version__
    assert resource._attributes["hyperdx.distro.runtime_version"] == platform.python_version(
    )


def test_can_set_service_name():
    options = HyperDXOptions(service_name="my-service")
    resource = create_resource(options)
    assert resource._attributes["service.name"] == "my-service"
    assert resource._attributes["hyperdx.distro.version"] == __version__
    assert resource._attributes["hyperdx.distro.runtime_version"] == platform.python_version(
    )


def test_can_set_service_version():
    options = HyperDXOptions(service_version="1.2.3")
    resource = create_resource(options)
    assert resource._attributes["service.version"] == "1.2.3"
