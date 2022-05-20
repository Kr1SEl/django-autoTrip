from django import template

register = template.Library()


@register.simple_tag
def trip_filter_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filter_querystring = filter(lambda x: x.split(
            '=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filter_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url
