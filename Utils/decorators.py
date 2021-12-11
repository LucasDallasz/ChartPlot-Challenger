from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .exceptions import ModelDoesNotExist
from .functions import get_model

import functools

def object_exists(modelName):
    """ This decorator checks if the object exists. """
    def decorator(view):
        @functools.wraps(view)
        def wrapper(request, id, *args, **kwargs):
            Model = get_model(modelName)
            if Model is None:
                raise ModelDoesNotExist('The model does not exist.')
            try:
                (Model.objects.get(id=id)) is True
            except ObjectDoesNotExist:
                return redirect(f"{reverse('Chart:all')}?objectDoesNotExists=1")
            else:
                return view(request, id, *args, **kwargs)
        return wrapper
    return decorator