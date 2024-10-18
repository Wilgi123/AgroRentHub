# in a new file pipelines.py in your app
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = {
        'username': details['username'],
        'email': details['email'],
    }
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }