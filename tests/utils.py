import inject


@inject.params(settings="settings")
def override_settings(settings, **kwargs):
    test_settings = settings.model_copy(deep=True)
    for key, val in kwargs.items():
        setattr(test_settings, key, val)
    return test_settings
