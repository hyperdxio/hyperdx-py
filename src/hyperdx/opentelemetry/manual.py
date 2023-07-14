import os

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from hyperdx.opentelemetry.options import HyperDXOptions


def decode_body(body):
    try:
        if isinstance(body, bytes):
            return body.decode("utf-8")
        return body
    except Exception as e:
        return body


def _instrument_requests(
    options: HyperDXOptions,
    tracer_provider: TracerProvider,
    meter_provider: MeterProvider,
):
    try:
        from opentelemetry.instrumentation.requests import RequestsInstrumentor

        def request_hook(span, request_obj):
            if request_obj.headers:
                for k, v in request_obj.headers.items():
                    span.set_attribute("http.request.header.%s" % k.lower(), v)
            if request_obj.body:
                span.set_attribute("http.request.body", decode_body(request_obj.body))

        def response_hook(span, request_obj, response):
            if response.headers:
                for k, v in response.headers.items():
                    span.set_attribute("http.response.header.%s" % k.lower(), v)
            if response.text:
                span.set_attribute("http.response.body", response.text)

        RequestsInstrumentor().instrument(
            excluded_urls=",".join(options.get_all_endpoints()),
            meter_provider=meter_provider,
            request_hook=request_hook,
            response_hook=response_hook,
            tracer_provider=tracer_provider,
        )
    except ImportError as e:
        pass


# FIXME: capture headers + body
def _instrument_urllib(
    options: HyperDXOptions,
    tracer_provider: TracerProvider,
    meter_provider: MeterProvider,
):
    try:
        from http import client
        from opentelemetry.instrumentation.urllib import urllibinstrumentor
        from urllib.request import Request

        def request_hook(span, request_obj: Request):
            for header in request_obj.header_items():
                k, v = header
                span.set_attribute("http.request.header.%s" % k.lower(), v)
            if request_obj.data:
                span.set_attribute("http.request.body", decode_body(request_obj.data))

        def response_hook(span, request_obj, response: client.HTTPResponse):
            for k, v in response.headers.items():
                span.set_attribute("http.response.header.%s" % k.lower(), v)
            # if response.text:
            #     span.set_attribute("http.response.body", response.text)

        urllibinstrumentor().instrument(
            excluded_urls=",".join(options.get_all_endpoints()),
            meter_provider=meter_provider,
            request_hook=request_hook,
            response_hook=response_hook,
            tracer_provider=tracer_provider,
        )
    except ImportError as e:
        pass


def _instrument_flask(
    options: HyperDXOptions,
    tracer_provider: TracerProvider,
    meter_provider: MeterProvider,
):
    try:
        from opentelemetry.instrumentation.flask import FlaskInstrumentor

        FlaskInstrumentor().instrument(
            excluded_urls=",".join(options.get_all_endpoints()),
            meter_provider=meter_provider,
            tracer_provider=tracer_provider,
        )
    except ImportError as e:
        pass


def _instrument_fastapi(
    options: HyperDXOptions,
    tracer_provider: TracerProvider,
    meter_provider: MeterProvider,
):
    try:
        from opentelemetry.instrumentation.fastapi import (
            FastAPIInstrumentor,
            Span as FastAPISpan,
        )

        def client_response_hook(span: FastAPISpan, message: dict):
            if span and span.is_recording():
                if "body" in message:
                    span.set_attribute("http.response.body", decode_body(message["body"]))

        FastAPIInstrumentor().instrument(
            client_response_hook=client_response_hook,
            excluded_urls=",".join(options.get_all_endpoints()),
            meter_provider=meter_provider,
            tracer_provider=tracer_provider,
        )
    except ImportError as e:
        pass


def configure_custom_env_vars(options: HyperDXOptions, resource: Resource):
    os.environ["OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_CLIENT_REQUEST"] = os.getenv(
        "OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_CLIENT_REQUEST", ".*"
    )
    os.environ["OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_CLIENT_RESPONSE"] = os.getenv(
        "OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_CLIENT_RESPONSE", ".*"
    )
    os.environ["OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST"] = os.getenv(
        "OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST", ".*"
    )
    os.environ["OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE"] = os.getenv(
        "OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE", ".*"
    )
    os.environ["OTEL_PYTHON_LOG_CORRELATION"] = os.getenv(
        "OTEL_PYTHON_LOG_CORRELATION", "true"
    )


def instrument_custom_libs(
    options: HyperDXOptions,
    resource: Resource,
    tracer_provider: TracerProvider,
    meter_provider: MeterProvider,
):
    _instrument_requests(options, tracer_provider, meter_provider)
    _instrument_flask(options, tracer_provider, meter_provider)
    _instrument_fastapi(options, tracer_provider, meter_provider)
