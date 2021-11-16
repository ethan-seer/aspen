from aspen.storage import options


def build_source(storage_type, source, credentials):
    """Builds the Read or Write storage object
    storage_type: Read or write
    source: list of args
    credentials: global credentials
    """

    storage = None

    source_present, *_ = source

    if source_present:

        try:
            (
                source_method,
                source_format,
                source_name,
                credentials,
            ) = source
        except:
            source_method, source_format, source_name = source

        method_option = options(method=source_method)

        return storage_type(
            destination=source_name,
            method=method_option,
            extension=source_format,
            service_account=credentials,
        )
