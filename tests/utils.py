# classic keys are 32 chars long
CLASSIC_APIKEY = "this is a string that is 32 char"
# non-classic keys are 22 chars log
APIKEY = "an api key for 22 char"


def get_metric_readers(meter_provider):
    """Return the configured metric readers across OTel SDK versions.

    OpenTelemetry SDK < 1.44 stored the readers on
    ``meter_provider._sdk_config.metric_readers``; 1.44+ moved them to
    ``meter_provider._metric_readers``.
    """
    readers = getattr(meter_provider, "_metric_readers", None)
    if readers is None:
        readers = meter_provider._sdk_config.metric_readers
    return readers
