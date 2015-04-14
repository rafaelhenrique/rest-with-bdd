import behave
from purl import URL
from ensure import ensure
import requests
from functools import wraps
import os


def get_environ_variable(f):
    @wraps(f)
    def wrapper(context, **kwargs):
        decoded_kwargs = {}
        #import ipdb; ipdb.set_trace()
        for key, value in kwargs.items():
            if value.startswith('$'):
                value = os.environ.get(value[1:], '')
            decoded_kwargs[key] = value
        return f(context, **decoded_kwargs)
    return wrapper


def append_path(url, url_path_segment):
    target = URL(url_path_segment)
    url = url.add_path_segment(target.path())
    if target.query():
        url = url.query(target.query())
    return url.as_string()


@behave.given('I am using server "{server}"')
@get_environ_variable
def using_server(context, server):
    context.server = URL(server)


@behave.given('I set base URL to "{base_url}"')
@get_environ_variable
def set_base_url(context, base_url):
    context.server = context.server.add_path_segment(base_url)


@behave.given('I set "{var}" header to "{value}"')
@get_environ_variable
def set_header(context, var, value):
    # We must keep the headers as implicit ascii to avoid encoding failure when
    # the entire HTTP body is constructed by concatenating strings.
    context.headers[var.encode('ascii')] = value.encode('ascii')


@behave.when('I make a GET request to "{resource}"')
@get_environ_variable
def get_request(context, resource):
    url = append_path(context.server, resource)
    context.response = requests.get(
        url, headers=context.headers, auth=context.auth)


@behave.then('the response status should be {status}')
def response_status(context, status):
    ensure(context.response.status_code).equals(int(status))


@behave.then('I should see this title "{title}" of book')
@get_environ_variable
def get_title_of_book(context, title):
    ensure(context.response.json()['book']['title']).equals(str(title))
