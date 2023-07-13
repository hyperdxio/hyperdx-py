from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter as HTTPOTLPLogExporter,
)
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter as GRPCOTLPLogExporter,
)


def create_logger_provider(options: HyperDXOptions, resource: Resource):
    """
    Configures and returns a new LoggerProvier to send logs telemetry.

    Args:
        options (HyperDXOptions): the HyperDX options to configure with
        resource (Resource): the resource to use with the new logger provider

    Returns:
        LoggerProvider: the new logger provider
    """

    logger_provider = LoggerProvider()

    if options.logs_exporter_protocol == "grpc":
        exporter = GRPCOTLPLogExporter(
            endpoint=options.get_logs_endpoint(),
            credentials=options.get_logs_endpoint_credentials(),
            headers=options.get_logs_headers(),
        )
    else:
        exporter = HTTPOTLPLogExporter(
            endpoint=options.get_logs_endpoint(),
            headers=options.get_logs_headers(),
        )
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

    if options.debug:
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(ConsoleLogExporter())
        )

    return logger_provider
