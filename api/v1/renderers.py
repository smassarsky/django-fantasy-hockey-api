from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        if type(data) == ReturnList:
            response = {
                'count': len(data),
                'items': data
            }
        else:
            response = data
        return super(CustomJSONRenderer, self).render(response, media_type, renderer_context)