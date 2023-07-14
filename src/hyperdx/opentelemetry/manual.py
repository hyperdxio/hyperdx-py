import os

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


def _instrument_requests(tracer_provider: TracerProvider):
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
            tracer_provider=tracer_provider,
            request_hook=request_hook,
            response_hook=response_hook,
        )
    except ImportError as e:
        pass


def _instrument_flask(tracer_provider: TracerProvider):
    try:
        from opentelemetry.instrumentation.flask import FlaskInstrumentor

        FlaskInstrumentor().instrument(tracer_provider=tracer_provider)
    except ImportError as e:
        pass


def _instrument_fastapi(tracer_provider: TracerProvider):
    try:
        from opentelemetry.instrumentation.fastapi import (
            FastAPIInstrumentor,
            Span as FastAPISpan,
        )

        def client_response_hook(span: FastAPISpan, message: dict):
            if "body" in message:
                span.set_attribute("http.response.body", decode_body(message["body"]))

        FastAPIInstrumentor().instrument(
            tracer_provider=tracer_provider, client_response_hook=client_response_hook
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
    options: HyperDXOptions, resource: Resource, tracer_provider: TracerProvider
):
    _instrument_requests(tracer_provider)
    _instrument_flask(tracer_provider)
    _instrument_fastapi(tracer_provider)
