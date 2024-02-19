# MapProxy WMS Retry plugin

This MapProxy plugin tries multiple times to retrieve data from a WMS server in case an error message is detected. Wait time grows exponentially.

## Configuration

Just change `type: wms` with `type: wms_retry` and set an error message to be detected within the first 100 bytes. Here is an example:

```yaml
sources:
  flaky_wms:
    type: wms_retry
    retry:
        error_message: Overforbruk
    req:
      url: http://flaky_wms/?
```

Here is the same example with all the possible settings:

```yaml
sources:
  flaky_wms:
    type: wms_retry
    retry:
        error_message: Overforbruk
        encoding: utf-8
        peek_size: 100
        max_tentatives: 10
    req:
      url: http://flaky_wms/?
```
