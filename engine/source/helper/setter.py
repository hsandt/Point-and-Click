def set_behaviour(instance, method_name, method):
    setattr(instance, method_name, method.__get__(instance))  # we don't precise class, it's enough here
