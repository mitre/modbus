from abc import ABC, abstractmethod


class Context:
    """
    Client context object.
    """

    def __init__(self, client=None):
        self.client = client
        # Type of transport
        self.transport = None  # TODO: make enum
        # Whether or not the last action failed
        self.last_failed = False
        # Recent results
        self.results = list()
        # Dictionary of currently running jobs
        self.jobs = {}


class ActionClientInterface(ABC):
    """
    Interface for protocol clients to implement.
    """

    def __init__(self):
        self._context = Context()

    @property
    def context(self):
        return self._context

    @property
    def client(self):
        return self._context.client

    @abstractmethod
    def connect(self):
        """Connects the client object."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        """Disconnects the client object."""
        raise NotImplementedError

    @abstractmethod
    def send(self, payload):
        """Sends the raw payload over the client's protocol layer."""
        raise NotImplementedError

    @classmethod
    def add_action(cls, function_name, function_ptr, overwrite=False):
        """
        Add an action to the given class as a function of that class
        using the provided function name and pointer.
        Additionally, include it in the class' action_map class variable.
        """
        if not getattr(cls, function_name, False) or overwrite:
            setattr(cls, function_name, function_ptr)
        if function_name not in cls.action_map:
            cls.action_map[function_name] = function_ptr

    @classmethod
    def action(cls, func):
        """Decorator to add an action using its function name."""

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        # Register function
        cls.add_action(func.__name__, func)
        return wrapper

    @classmethod
    def named_action(cls, name):
        """Decorator to add an action using a provided name."""

        def decorator(func, action_name=name):
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)

            # Register function
            cls.add_action(action_name, func)
            return wrapper

        return decorator

    def get(self, name):
        """Returns an action function pointer by name."""
        # Polymorphic, will get the action_map of the object's class
        return self.action_map.get(
            name, None
        )  # TODO: Raise exception instead of returning None?
