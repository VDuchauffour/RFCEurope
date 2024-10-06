from BugEventManager import g_eventManager as events
import inspect


def handler(event):
    def handler_decorator(func):
        arg_names = inspect.getargspec(func)[0]

        def handler_func(args):
            return func(*args[: len(arg_names)])

        handler_func.__name__ = func.__name__
        handler_func.__module__ = func.__module__
        handler_func.func_name = func.func_name

        events.addEventHandler(event, handler_func)
        return handler_func

    return handler_decorator


def popup_handler(event_id):
    def handler_decorator(func):
        events.addCustomEvent(event_id, func.__name__, func, noop)
        return func

    return handler_decorator


def noop(*args, **kwargs):
    pass


events.addEvent("firstCity")


@handler("cityAcquiredAndKept")
def firstCityOnCityAcquiredAndKept(iPlayer, city):
    if city.isCapital():
        events.fireEvent("firstCity", city)


@handler("cityBuilt")
def firstCityOnCityBuilt(city):
    if city.isCapital():
        events.fireEvent("firstCity", city)
