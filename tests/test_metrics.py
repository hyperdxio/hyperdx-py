from opentelemetry.sdk.metrics import MeterProvider

from hyperdx.opentelemetry.options import HyperDXOptions
from hyperdx.opentelemetry.resource import create_resource
from hyperdx.opentelemetry.metrics import create_meter_provider

from tests.utils import get_metric_readers


def test_returns_meter_provider():
    options = HyperDXOptions()
    resource = create_resource(options)
    meter_provider = create_meter_provider(options, resource)
    assert isinstance(meter_provider, MeterProvider)
    assert len(get_metric_readers(meter_provider)) == 1


def test_setting_debug_adds_console_exporter():
    options = HyperDXOptions(debug=True)
    resource = create_resource(options)
    meter_provider = create_meter_provider(options, resource)
    assert isinstance(meter_provider, MeterProvider)
    assert len(get_metric_readers(meter_provider)) == 2
