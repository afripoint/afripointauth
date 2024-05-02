import json
from rest_framework.renderers import JSONRenderer


class PhoneNumberJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context and "response" in renderer_context:
            status_code = renderer_context["response"].status_code
        else:
            status_code = None
        if isinstance(data, dict):
            errors = data.get("errors", None)
            if errors is not None:
                return super().render(data)
            else:
                return json.dumps({"status_code": status_code, "account_type": data})
        elif isinstance(data, list):
            return json.dumps(
                {"status_code": status_code, "custom_accounts_type": data}
            )
        else:
            return super().render(data)
