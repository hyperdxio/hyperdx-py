from opentelemetry.sdk.environment_variables import (
    OTEL_EXPORTER_OTLP_ENDPOINT,
    OTEL_EXPORTER_OTLP_INSECURE,
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT,
    OTEL_EXPORTER_OTLP_METRICS_INSECURE,
    OTEL_EXPORTER_OTLP_TRACES_INSECURE,
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
    OTEL_SERVICE_NAME,
)
from tests.utils import APIKEY

from hyperdx.opentelemetry.options import (
    DEBUG,
    DEFAULT_API_ENDPOINT,
    EXPORTER_PROTOCOL_GRPC,
    EXPORTER_PROTOCOL_HTTP_PROTO,
    HyperDXOptions,
    HYPERDX_API_ENDPOINT,
    HYPERDX_API_KEY,
    HYPERDX_DATASET,
    HYPERDX_ENABLE_LOCAL_VISUALIZATIONS,
    HYPERDX_METRICS_APIKEY,
    HYPERDX_METRICS_DATASET,
    HYPERDX_TRACES_APIKEY,
    SAMPLE_RATE
)

EXPECTED_ENDPOINT = "expected endpoint"


def test_defaults():
    options = HyperDXOptions()
    assert options.traces_apikey is None
    assert options.metrics_apikey is None
    assert options.get_traces_endpoint() == "https://in-otel.hyperdx.io"
    assert options.get_metrics_endpoint() == "https://in-otel.hyperdx.io"
    assert options.service_name == "unknown_service:python"
    assert options.dataset is None
    assert options.metrics_dataset is None
    assert options.enable_local_visualizations is False
    assert options.traces_exporter_protocol is EXPORTER_PROTOCOL_GRPC
    assert options.metrics_exporter_protocol is EXPORTER_PROTOCOL_GRPC


def test_can_set_service_name_with_param():
    options = HyperDXOptions(service_name="my-service")
    assert options.service_name == "my-service"


def test_can_set_service_name_with_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_SERVICE_NAME, "my-service")
    options = HyperDXOptions()
    assert options.service_name == "my-service"


def test_can_set_generic_api_endpoint_with_envvar(monkeypatch):
    monkeypatch.setenv(HYPERDX_API_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions()
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_can_set_generic_api_endpoint_with_param():
    options = HyperDXOptions(endpoint=EXPECTED_ENDPOINT)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_can_set_traces_endpoint_with_param():
    options = HyperDXOptions(traces_endpoint=EXPECTED_ENDPOINT)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_can_set_traces_endpoint_with_traces_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions()
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_can_set_traces_endpoint_with_endpoint_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions()
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_traces_endpoint_set_from_generic_env_beats_params(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(
        endpoint="generic param",
        traces_endpoint="specific param"
    )
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_traces_endpoint_specific_env_beats_params(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(
        endpoint="generic param",
        traces_endpoint="specific param"
    )
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_traces_endpoint_set_from_specific_param_beats_generic_param():
    options = HyperDXOptions(
        endpoint="generic param",
        traces_endpoint=EXPECTED_ENDPOINT
    )
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_traces_endpoint_set_from_traces_env_beats_params(
        monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, "generic env")
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(
        endpoint="generic param",
        traces_endpoint="specific param"
    )
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_can_set_metrics_endpoint_with_param():
    options = HyperDXOptions(metrics_endpoint=EXPECTED_ENDPOINT)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_can_set_metrics_endpoint_with_metrics_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions()
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_can_set_metrics_endpoint_with_endpoint_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions()
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_get_traces_endpoint_returns_endpoint_when_traces_endpoint_not_set():
    options = HyperDXOptions(endpoint=EXPECTED_ENDPOINT)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_get_metrics_endpoint_returns_endpoint_when_metrics_endpoint_not_set():
    options = HyperDXOptions(endpoint=EXPECTED_ENDPOINT)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_can_set_apikey_with_param():
    options = HyperDXOptions(apikey=APIKEY)
    assert options.traces_apikey == APIKEY
    assert options.metrics_apikey == APIKEY


def test_can_set_apikey_with_envvar(monkeypatch):
    monkeypatch.setenv(HYPERDX_API_KEY, APIKEY)
    options = HyperDXOptions()
    assert options.traces_apikey == APIKEY
    assert options.metrics_apikey == APIKEY


def test_can_set_traces_apikey_with_param():
    options = HyperDXOptions(traces_apikey=APIKEY)
    assert options.traces_apikey == APIKEY


def test_can_set_traces_apikey_with_envvar(monkeypatch):
    monkeypatch.setenv(HYPERDX_TRACES_APIKEY, APIKEY)
    options = HyperDXOptions()
    assert options.traces_apikey == APIKEY


def test_can_set_metrics_apikey_with_param():
    options = HyperDXOptions(metrics_apikey=APIKEY)
    assert options.metrics_apikey == APIKEY


def test_can_set_metrics_apikey_with_envvar(monkeypatch):
    monkeypatch.setenv(HYPERDX_METRICS_APIKEY, APIKEY)
    options = HyperDXOptions()
    assert options.metrics_apikey == APIKEY


def test_default_sample_rate_is_1():
    options = HyperDXOptions()
    assert options.sample_rate == 1


def test_can_set_sample_rate_with_param():
    options = HyperDXOptions(sample_rate=123)
    assert options.sample_rate == 123


def test_can_set_sample_rate_of_zero_param():
    options = HyperDXOptions(sample_rate=0)
    assert options.sample_rate == 0


def test_can_set_sample_rate_of_zero_envar(monkeypatch):
    monkeypatch.setenv(SAMPLE_RATE, "0")
    options = HyperDXOptions()
    assert options.sample_rate == 0


def test_can_set_sample_rate_with_envvar(monkeypatch):
    monkeypatch.setenv(SAMPLE_RATE, "321")
    options = HyperDXOptions()
    assert options.sample_rate == 321


def test_sample_rate_from_env_beats_param(monkeypatch):
    monkeypatch.setenv(SAMPLE_RATE, "50")
    options = HyperDXOptions(sample_rate=25)
    assert options.sample_rate == 50


def test_invalid_sample_rate_envvar_uses_default(monkeypatch):
    monkeypatch.setenv(SAMPLE_RATE, "nonsense")
    options = HyperDXOptions()
    assert options.sample_rate == 1


def test_invalid_sample_rate_param_uses_default():
    options = HyperDXOptions(sample_rate="nonsense")
    assert options.sample_rate == 1


def test_default_debug_is_false():
    options = HyperDXOptions()
    assert options.debug is False


def test_can_set_debug_with_param():
    options = HyperDXOptions(debug=True)
    assert options.debug is True


def test_can_set_debug_with_envvar(monkeypatch):
    monkeypatch.setenv(DEBUG, "TRUE")
    options = HyperDXOptions()
    assert options.debug is True


def test_debug_from_env_beats_param(monkeypatch):
    monkeypatch.setenv(DEBUG, "TRUE")
    options = HyperDXOptions(debug=False)
    assert options.debug is True


def test_traces_endpoint_insecure_defaults_to_false():
    options = HyperDXOptions()
    assert options.traces_endpoint_insecure is False


def test_can_set_traces_insecure_with_generic_param():
    options = HyperDXOptions(endpoint_insecure=True)
    assert options.traces_endpoint_insecure is True


def test_can_set_traces_insecure_with_traces_param():
    options = HyperDXOptions(traces_endpoint_insecure=True)
    assert options.traces_endpoint_insecure is True


def test_traces_insecure_set_with_specific_param_beats_generic():
    options = HyperDXOptions(
        endpoint_insecure=False,
        traces_endpoint_insecure=True
    )
    assert options.traces_endpoint_insecure is True


def test_can_set_traces_insecure_with_generic_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_INSECURE, "TRUE")
    options = HyperDXOptions()
    assert options.traces_endpoint_insecure is True


def test_can_set_traces_insecure_with_traces_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_TRACES_INSECURE, "TRUE")
    options = HyperDXOptions()
    assert options.traces_endpoint_insecure is True


def test_traces_insecure_generic_env_beats_params(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_INSECURE, "TRUE")
    options = HyperDXOptions(
        endpoint_insecure=False,
        traces_endpoint_insecure=False
    )
    assert options.traces_endpoint_insecure is True


def test_traces_insecure_specific_env_beats_generic_env_and_params(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_INSECURE, "FALSE")
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_TRACES_INSECURE, "TRUE")
    options = HyperDXOptions(
        endpoint_insecure=False,
        traces_endpoint_insecure=False
    )
    assert options.traces_endpoint_insecure is True


def test_metrics_endpoint_insecure_defaults_to_false():
    options = HyperDXOptions()
    assert options.metrics_endpoint_insecure is False


def test_can_set_metrics_insecure_with_generic_param():
    options = HyperDXOptions(endpoint_insecure=True)
    assert options.metrics_endpoint_insecure is True


def test_can_set_metrics_insecure_with_traces_param():
    options = HyperDXOptions(metrics_endpoint_insecure=True)
    assert options.metrics_endpoint_insecure is True


def test_metrics_insecure_specific_param_beats_generic_param():
    options = HyperDXOptions(
        endpoint_insecure=False,
        metrics_endpoint_insecure=True
    )
    assert options.metrics_endpoint_insecure is True


def test_can_set_metrics_insecure_with_generic_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_INSECURE, "TRUE")
    options = HyperDXOptions()
    assert options.metrics_endpoint_insecure is True


def test_can_set_metrics_insecure_with_traces_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_METRICS_INSECURE, "TRUE")
    options = HyperDXOptions()
    assert options.metrics_endpoint_insecure is True


def test_metrics_insecure_generic_env_beats_params(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_INSECURE, "TRUE")
    options = HyperDXOptions(
        endpoint_insecure=False,
        metrics_endpoint_insecure=False
    )
    assert options.metrics_endpoint_insecure is True


def test_metrics_insecure_specific_env_beats_generic_env_and_params(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_INSECURE, "FALSE")
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_METRICS_INSECURE, "TRUE")
    options = HyperDXOptions(
        endpoint_insecure=False,
        metrics_endpoint_insecure=False
    )
    assert options.metrics_endpoint_insecure is True


def test_metrics_endpoint_set_from_generic_env_beats_params(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(
        endpoint="generic param",
        metrics_endpoint="specific param"
    )
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_metrics_endpoint_specific_env_beats_params(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(
        endpoint="generic param",
        metrics_endpoint="specific param"
    )
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_metrics_endpoint_set_from_specific_param_beats_generic_param():
    options = HyperDXOptions(
        endpoint="generic param",
        metrics_endpoint=EXPECTED_ENDPOINT
    )
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_metrics_endpoint_set_from_metrics_env_beats_params(
        monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, "generic env")
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(
        endpoint="generic param",
        metrics_endpoint="specific param"
    )
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_can_set_dataset_with_param():
    options = HyperDXOptions(dataset="my-dataset")
    assert options.dataset == "my-dataset"


def test_can_set_dataset_with_envvar(monkeypatch):
    monkeypatch.setenv(HYPERDX_DATASET, "my-dataset")
    options = HyperDXOptions()
    assert options.dataset == "my-dataset"


def test_can_set_metrics_dataset_with_param():
    options = HyperDXOptions(metrics_dataset="my-metrics-dataset")
    assert options.metrics_dataset == "my-metrics-dataset"


def test_can_set_metrics_dataset_with_envvar(monkeypatch):
    monkeypatch.setenv(HYPERDX_METRICS_DATASET, "my-metrics-dataset")
    options = HyperDXOptions()
    assert options.metrics_dataset == "my-metrics-dataset"


def test_can_set_enable_local_visualizations_with_param():
    options = HyperDXOptions(enable_local_visualizations=True)
    assert options.enable_local_visualizations is True


def test_can_set_enable_local_visualizations_with_envvar(monkeypatch):
    monkeypatch.setenv(HYPERDX_ENABLE_LOCAL_VISUALIZATIONS, "TRUE")
    options = HyperDXOptions()
    assert options.enable_local_visualizations is True


def test_local_vis_from_env_beats_param(monkeypatch):
    monkeypatch.setenv(HYPERDX_ENABLE_LOCAL_VISUALIZATIONS, "TRUE")
    options = HyperDXOptions(enable_local_visualizations=False)
    assert options.enable_local_visualizations is True


def test_get_traces_endpoint_with_grpc_protocol_returns_correctly_formatted_endpoint(monkeypatch):
    # grpc
    protocol = EXPORTER_PROTOCOL_GRPC

    # default endpoint
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_traces_endpoint() == DEFAULT_API_ENDPOINT

    # generic endpoint param
    options = HyperDXOptions(
        exporter_protocol=protocol, endpoint=EXPECTED_ENDPOINT)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT

    # traces endpoint param
    options = HyperDXOptions(
        exporter_protocol=protocol, traces_endpoint=EXPECTED_ENDPOINT)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT

    # generic endpoint env
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT

    # traces endpoint env
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_get_traces_endpoint_with_http_proto_protocol_returns_correctly_formatted_endpoint(monkeypatch):
    # http
    protocol = EXPORTER_PROTOCOL_HTTP_PROTO

    # default endpoint
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_traces_endpoint() == DEFAULT_API_ENDPOINT + "/v1/traces"

    # generic endpoint param
    options = HyperDXOptions(
        exporter_protocol=protocol, endpoint=EXPECTED_ENDPOINT)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT + "/v1/traces"

    # traces endpoint param
    options = HyperDXOptions(
        exporter_protocol=protocol, traces_endpoint=EXPECTED_ENDPOINT)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT

    # generic endpoint env
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT + "/v1/traces"

    # traces endpoint env
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_traces_endpoint() == EXPECTED_ENDPOINT


def test_get_metrics_endpoint_with_grpc_protocol_returns_correctly_formatted_endpoint(monkeypatch):
    # grpc
    protocol = EXPORTER_PROTOCOL_GRPC

    # default endpoint
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_metrics_endpoint() == DEFAULT_API_ENDPOINT

    # generic endpoint param
    options = HyperDXOptions(
        exporter_protocol=protocol, endpoint=EXPECTED_ENDPOINT)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT

    # metrics endpoint param
    options = HyperDXOptions(
        exporter_protocol=protocol, metrics_endpoint=EXPECTED_ENDPOINT)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT

    # generic endpoint env
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT

    # metrics endpoint env
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_get_metrics_endpoint_with_http_proto_protocol_returns_correctly_formatted_endpoint(monkeypatch):
    # http
    protocol = EXPORTER_PROTOCOL_HTTP_PROTO

    # default endpoint
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_metrics_endpoint() == DEFAULT_API_ENDPOINT + "/v1/metrics"

    # generic endpoint param
    options = HyperDXOptions(
        exporter_protocol=protocol, endpoint=EXPECTED_ENDPOINT)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT + "/v1/metrics"

    # metrics endpoint param
    options = HyperDXOptions(
        exporter_protocol=protocol, metrics_endpoint=EXPECTED_ENDPOINT)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT

    # generic endpoint env
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT + "/v1/metrics"

    # metrics endpoint env
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, EXPECTED_ENDPOINT)
    options = HyperDXOptions(exporter_protocol=protocol)
    assert options.get_metrics_endpoint() == EXPECTED_ENDPOINT


def test_debug_sets_log_level_to_debug():
    options = HyperDXOptions(debug=True)
    assert options.log_level == "DEBUG"


def test_debug_with_custom_log_level_sets_log_level_to_debug():
    options = HyperDXOptions(debug=True, log_level="INFO")
    assert options.log_level == "DEBUG"
