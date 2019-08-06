from django.shortcuts import redirect


def login_decorator(original_function):
    def wrapper_function(request, *param):
        try:
            request.session['authadmin']
        except KeyError:
            return redirect('/manager/login?result=nologin')

        return original_function(request, *param)
    return wrapper_function
