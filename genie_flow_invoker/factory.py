from queue import Queue
from typing import Optional, Type

from genie_flow_invoker import GenieInvoker, InvokersPool


class InvokerFactory:

    def __init__(
        self,
        config: Optional[dict],
        builtin_registry: dict[str, Type[GenieInvoker]] = None,
    ):
        self.config = config or dict()
        self._registry: dict[str, Type[GenieInvoker]] = builtin_registry or dict()

    def register_invoker(self, invoker_name: str, invoker_class: Type[GenieInvoker]):
        """
        Register your own invoker. It then becomes usable in any `meta.yaml` directive in a
        template directory.

        :param invoker_name: The name of the invoker, as it will appear in the `meta.yaml`
        :param invoker_class: The invoker class to register.
        """
        if invoker_name in self._registry:
            raise ValueError(f"'{invoker_name}' is already registered")
        self._registry[invoker_name] = invoker_class

    def create_invoker(self, invoker_config: dict) -> GenieInvoker:
        """
        Create a new invoker, as specified by `invoker_config`. Uses the application's
        configuration as a base. Any configuration specified in `invoker_config` takes
        precedence over any other configuration specified in the application's configuration.

        :param invoker_config: The invoker config to create.
        :return: The created invoker.
        :raises ValueError: If the invoker is not registered or the invoker is invalid.
        """
        try:
            invoker_type = invoker_config["type"]
        except KeyError:
            raise ValueError(f"Invalid invoker config: {invoker_config}")

        try:
            cls = self._registry[invoker_type]
        except KeyError:
            raise ValueError(f"Unknown invoker type: {invoker_type}")

        config = self.config[invoker_type] if invoker_type in self.config.keys() else dict()
        config.update(invoker_config)
        return cls.from_config(config)

    def create_invoker_pool(self, pool_size: int, config: dict) -> InvokersPool:
        assert pool_size > 0, f"Should not create invoker pool of size {pool_size}"

        queue = Queue()
        for _ in range(pool_size):
            queue.put(self.create_invoker(config))

        return InvokersPool(queue)
