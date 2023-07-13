import platform
from opentelemetry.sdk.resources import Resource
from hyperdx.opentelemetry.options import HyperDXOptions
from hyperdx.opentelemetry.version import __version__


def create_resource(options: HyperDXOptions):
    """
    Configures and returns a new OpenTelemetry Resource.

    Args:
        options (HyperDXOptions): the HyperDX options to configure with
        resource (Resource): the resource to use with the new resource

    Returns:
        MeterProvider: the new Resource
    """
    attributes = {
        "service.name": options.service_name,
        "hyperdx.distro.version": __version__,
        "hyperdx.distro.runtime_version": platform.python_version()
    }
    if options.service_version:
        attributes["service.version"] = options.service_version
    return Resource.create(attributes)
