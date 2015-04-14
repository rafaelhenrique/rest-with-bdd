import os

default_env = {
    'TEST_SERVER': 'http://localhost:5000',
    'TEST_URL': 'library/api/',
    'TEST_TITLE': 'Python Cookbook',
}


def before_scenario(context, scenario):
    # Seed empty HTTP headers so steps do not need to check and create.
    context.headers = {}

    # Seed empty Jinja2 template data so steps do not need to check and create.
    context.template_data = {}

    # Default repeat attempt counts and delay for polling GET.
    context.n_attempts = 10
    context.pause_between_attempts = 0.05

    # Do not authenticate by dafault
    context.auth = None


def before_all(context):
    for k, v in default_env.items():
        os.environ.setdefault(k, v)
        print("setting {0} {1}".format(k, v))
