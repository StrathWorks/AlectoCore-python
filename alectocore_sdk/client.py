import json
import urllib.request
import urllib.error
import urllib.parse


class AlectoCoreError(Exception):
    def __init__(self, message, status=None, data=None):
        super().__init__(message)
        self.status = status
        self.data = data


class AlectoCoreClient:
    def __init__(self, api_key, base_url="https://api.alectocore.com"):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def moderate(self, body):
        return self._request("POST", "/v1/moderate", body)

    def moderate_handle(self, body):
        return self._request("POST", "/v1/moderate/handle", body)

    def moderate_batch(self, body):
        return self._request("POST", "/v1/moderate/batch", body)

    def moderate_structured(self, body):
        return self._request("POST", "/v1/moderate/structured", body)

    def categories(self):
        return self._request("GET", "/v1/categories")

    def feedback(self, body):
        return self._request("POST", "/v1/feedback", body)

    def queue(self, limit=100):
        qs = urllib.parse.urlencode({"limit": limit})
        return self._request("GET", f"/v1/queue?{qs}")

    def resolve_queue_item(self, request_id, body):
        if not request_id:
            raise ValueError("request_id is required")
        rid = urllib.parse.quote(request_id, safe="")
        return self._request("POST", f"/v1/queue/{rid}/resolve", body)

    def _request(self, method, path, body=None):
        url = f"{self.base_url}{path}"
        payload = None if body is None else json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url=url, method=method, data=payload)
        req.add_header("Authorization", f"Bearer {self.api_key}")
        req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req) as res:
                raw = res.read().decode("utf-8")
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8")
            data = None
            if raw:
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    data = {"raw": raw}
            message = (data or {}).get("error", f"HTTP {e.code}")
            raise AlectoCoreError(message, e.code, data) from e
