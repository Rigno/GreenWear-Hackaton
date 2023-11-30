from django import template

register = template.Library()

@register.simple_tag
def update_params(field, value, urlencode=None):
    url = "?{0}={1}".format(field, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda param: param.split('=')[0] != field, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = "{0}&{1}".format(url, encoded_querystring)

    return url
    