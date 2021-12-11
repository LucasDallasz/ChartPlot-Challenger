import django.apps


def get_model(modelName):
    """ This function returns a model if find by name."""
    models = django.apps.apps.get_models()
    for model in models:
        if model.__name__ == modelName:
            return model
    return None