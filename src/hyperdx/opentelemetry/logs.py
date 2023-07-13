import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter as HTTPOTLPLogExporter,
)
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter as GRPCOTLPLogExporter,
)

from hyperdx.opentelemetry.options import HyperDXOptions


def set_logging_handler(options: HyperDXOptions):
    """
    Configures and returns a new LoggingHandler to send logs telemetry.

    Returns:
        LoggingHandler: the new logger handler
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

    set_logger_provider(logger_provider)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

    if options.debug:
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(ConsoleLogExporter())
        )

    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)
