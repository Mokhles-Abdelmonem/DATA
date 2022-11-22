from django.shortcuts import render

class HandelError:
    """
    Decorator for class based views
    """
    @staticmethod
    def error_decorator(function):
        def wrapper(self, request, *args, **kwargs):
            # try:
            return function(self, request, *args, **kwargs)
            # except Exception as e:
            #     print(e)
            #     return render(request, 'home/page-500.html')

        return wrapper


def error_decorator(function):
    """
    Decorator for functions views
    """
    def wrapper(request, *args, **kwargs):
        try:
            return function(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return render(request, 'home/page-500.html')
    return wrapper