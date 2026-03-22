# alectocore-sdk

Official Python SDK for Alecto Core.

## Requirements
- Python 3.9+
- Alecto Core key

## Install
```bash
pip install alectocore-sdk
```

## Quickstart
```python
from alectocore_sdk import AlectoCoreClient

client = AlectoCoreClient(api_key="ak_live_xxx")
out = client.moderate({"text": "you are an idiot"})
print(out["request_id"], out["action"], out["score"])
```

## Supported methods
- `moderate(body)`
- `moderate_handle(body)`
- `moderate_batch(body)`
- `moderate_structured(body)`
- `categories()`
- `feedback(body)`
- `queue(limit=100)`
- `resolve_queue_item(request_id, body)`

## Errors
API errors raise `AlectoCoreError` with:
- `status` HTTP status
- `data` parsed error response (if available)

## Base URL override
```python
client = AlectoCoreClient(
    api_key="ak_live_xxx",
    base_url="http://localhost:8080"
)
```
