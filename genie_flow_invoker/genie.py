from abc import ABC, abstractmethod
from typing import Optional

from genie_flow_invoker.error_config import OnErrorConfig, RetryConfig, compile_exception_list


class GenieInvoker(ABC):
    """
    The super class of all Genie Invokers. The standard interface to invoke large language models,
    database retrievals, etc.

    This is an abstraction around calls that take a text content and pass that to a lower level
    service for processing. The returned value is always a result string.

    This class is subclassed with specific classes for external services.
    """
    _on_error_config: Optional[OnErrorConfig] = None
    _retry_config: Optional[RetryConfig] = None

    @classmethod
    def from_config_with_error_handling(
            cls,
            config: dict,
            on_error: Optional[str | dict],
            retry: Optional[dict]
    ):
        """
        Create a new instance of the invoker with optional error handling and retry configs.
        The configs are set on the resulting invoker after the `from_config` method is used
        to create an instance.

        `on_error` can be either a string or a dictionary. If it is a string, then it will
        be used as a template to render the result when the invoker errors out. If a dict,
        then it needs to have a key 'event' for the event to be sent when the invoker errors
        out. That dict can optionally have a 'content' key that will be a template that is
        rendered as parameter to the sending that event.

        `retry` is an optional dictionary that contains the following keys:
        * `autoretry_for`: a list of FQNs of classes to trigger a retry for
        * `max_retries`: the maximum number of times the invoker will be retried for
        * `retry_backoff`: a boolean or float specifying if an exponential backoff should be
                         applied with base 1 second (boolean) or the given base number of
                         seconds.
        * `retry_backoff_max`: the max number of seconds to backoff.
        * `retry_jitter`: the random number to subtract from the backoff


        :param config: the configuration dictionary for the invoker
        :param on_error: optionally, either a string or a dictionary
        :param retry: an optional dictionary
        :return: a new instance of the invoker
        """
        on_error_config: Optional[OnErrorConfig] = None
        if on_error is not None:
            if isinstance(on_error, str):
                on_error_config = OnErrorConfig(event=None, content=on_error)
            else:
                on_error_config = OnErrorConfig(
                    event=on_error.get("event"),
                    content=on_error.get("content", None),
                )

        retry_config: Optional[RetryConfig] = None
        if retry is not None:
            retry_for = retry.get("autoretry_for", None),
            retry_exceptions = compile_exception_list(retry_for) if retry is not None else None
            retry_config = RetryConfig(
                autoretry_for=retry_exceptions,
                max_retries=retry.get("max_retries", None),
                retry_backoff=retry.get("retry_backoff", None),
                retry_backoff_max=retry.get("retry_backoff_max", None),
                retry_jitter=retry.get("retry_jitter", None),
            )

        invoker = cls.from_config(config)
        invoker._on_error_config = on_error_config
        invoker._retry_config = retry_config
        return invoker

    @classmethod
    @abstractmethod
    def from_config(cls, config: dict):
        raise NotImplementedError()

    @abstractmethod
    def invoke(self, content: str) -> str:
        """
        Invoke the underlying service with the supplied content and dialogue.

        :param content: The text content to invoke the underlying service. The format of
        this string is Invoker dependent. Some may simply expect a string, others may
        need to get a structured document as string - for instance a JSON string - that
        incorporates the values that one needs to pass.
        :return: The result string.
        """
        raise NotImplementedError()
