# HyperDX OpenTelemetry Distro for Python

[![OSS Lifecycle](https://img.shields.io/osslifecycle/hyperdxio/hyperdx-opentelemetry-python)](https://github.com/hyperdxio/home/blob/main/hyperdx-oss-lifecycle-and-practices.md)
[![PyPi](https://img.shields.io/pypi/v/hyperdx-opentelemetry)](https://pypi.org/project/hyperdx-opentelemetry/)

> **Deprecated:** `hyperdx-opentelemetry` is no longer maintained, and the
> ClickStack SDKs do not cover Python. Use the upstream
> [OpenTelemetry Python zero-code instrumentation](https://opentelemetry.io/docs/zero-code/python/)
> instead. Install it with
> `pip install opentelemetry-distro opentelemetry-exporter-otlp` and
> `opentelemetry-bootstrap -a install`, then start your app with
> `opentelemetry-instrument python app.py`. It exports traces, metrics, and
> `logging` records over OTLP. To move your configuration:
>
> - `HYPERDX_API_KEY` becomes `OTEL_EXPORTER_OTLP_HEADERS=authorization=<key>`.
> - `HYPERDX_API_ENDPOINT` becomes `OTEL_EXPORTER_OTLP_ENDPOINT`. The upstream
>   distro defaults to gRPC and this package defaulted to HTTP, so set
>   `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf` when the endpoint is OTLP/HTTP
>   (port 4318).
> - `OTEL_SERVICE_NAME` is unchanged.
> - For `HYPERDX_ENABLE_ADVANCED_NETWORK_CAPTURE`, set
>   `OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_{CLIENT,SERVER}_{REQUEST,RESPONSE}`
>   to a comma-separated list of the header names to capture. Avoid `.*`, which
>   also records authorization and cookie headers. Upstream has no setting to
>   capture request or response bodies.

> This project is a fork from https://github.com/honeycombio/honeycomb-opentelemetry-python

**STATUS: this library is BETA.**
You're welcome to try it, and let us know your feedback in the issues!

This is HyperDX's Distribution of OpenTelemetry for Python.
It makes getting started with OpenTelemetry and HyperDX easier!

Latest release built with:

- [OpenTelemetry version 1.27.0/0.48b0](https://github.com/open-telemetry/opentelemetry-python/releases/tag/v1.27.0)

## Requirements

- Python 3.8 or higher

## Getting Started

HyperDX's Distribution of OpenTelemetry for Python allows you to streamline configuration and to instrument as quickly and easily as possible.

- [Documentation](https://www.hyperdx.io/docs/install/python)

## License

[Apache 2.0 License](./LICENSE).
