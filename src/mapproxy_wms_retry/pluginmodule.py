import logging
import time

from mapproxy.client.http import HTTPClient
from mapproxy.config.loader import WMSSourceConfiguration, register_source_configuration
from mapproxy.config.spec import mapproxy_yaml_spec
from mapproxy.util.ext.dictspec.spec import required

SPEC = list(mapproxy_yaml_spec["sources"].values())[0].specs["wms"]
SPEC["retry"] = {
    required("error_message"): str(),
    "encoding": str(),
    "peek_size": int(),  # bytes
    "max_tentatives": int(),
}

logger = logging.getLogger("mapproxy.wms_retry")


class HTTPClientRetry(HTTPClient):
    def __init__(self, error_message, peek_size, max_tentatives):
        self.error_message = error_message
        self.peek_size = peek_size
        self.max_tentatives = max_tentatives
        super().__init__()

    def open(self, *args, **kwargs):
        for i in range(self.max_tentatives):
            result = super().open(*args, **kwargs)
            if self.error_message in result.peek(self.peek_size):
                logger.warning("Error message detected")
                time.sleep(2**i)
            else:
                return result


class wms_retry_configuration(WMSSourceConfiguration):
    source_type = ("wms_retry",)

    def source(self, params=None):
        # Custom parameters
        retry = self.conf["retry"]
        if isinstance(retry["error_message"], str):
            encoding = retry.get("encoding", "utf-8")
            retry["error_message"] = retry["error_message"].encode(encoding)
        retry.setdefault("peek_size", 100)
        retry.setdefault("max_tentatives", 10)
        # Create WMS source
        wmssource = super().source(params)
        # Replace HTTP client
        wmssource.client.http_client = HTTPClientRetry(**retry)
        return wmssource


def plugin_entrypoint():
    register_source_configuration(
        "wms_retry", wms_retry_configuration, "wms_retry", SPEC
    )
