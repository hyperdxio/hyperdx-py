from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GRPCSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter,
)

from hyperdx.opentelemetry.baggage import BaggageSpanProcessor
from hyperdx.opentelemetry.options import HyperDXOptions
from hyperdx.opentelemetry.resource import create_resource
from hyperdx.opentelemetry.trace import create_tracer_provider

"""
Our Tracer Provider expects a series of span processors.

BaggageSpanProcessor (no export)
BatchSpanProcessor (hyperdx Exporter)
SimpleSpanProcessor (Console Exporter)
SimpleSpanProcessor (Local Vis Exporter)

"""


def test_returns_tracer_provider_with_batch_and_baggage_span_processors():
    options = HyperDXOptions()
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 2
    assert any(
        isinstance(span_processor, BaggageSpanProcessor)
        for span_processor in active_span_processors
    )
    assert any(
        isinstance(span_processor, BatchSpanProcessor)
        for span_processor in active_span_processors
    )


def test_grpc_protocol_configures_grpc_span_exporter_on_batch_span_processor():
    options = HyperDXOptions(traces_exporter_protocol="grpc")
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 2
    (baggage, batch) = active_span_processors
    assert isinstance(batch, BatchSpanProcessor)
    assert isinstance(batch.span_exporter, GRPCSpanExporter)


def test_http_protocol_configures_http_span_exporter_on_batch_span_processor():
    options = HyperDXOptions(traces_exporter_protocol="http/protobuf")
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 2
    (baggage, batch) = active_span_processors
    assert isinstance(batch, BatchSpanProcessor)
    assert isinstance(batch.span_exporter, HTTPSpanExporter)


def test_setting_debug_adds_console_exporter_on_simple_span_processor():
    options = HyperDXOptions(debug=True)
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 3

    (baggage, batch, console) = active_span_processors
    assert isinstance(console, SimpleSpanProcessor)
    assert isinstance(console.span_exporter, ConsoleSpanExporter)
