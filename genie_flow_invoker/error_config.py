from typing import TypedDict, Optional, Union, List, Type

from genie_flow_invoker.class_utils import get_class_from_fully_qualified_name


class OnErrorConfig(TypedDict):
    event: Optional[str]
    content: Optional[str]


class RetryConfig(TypedDict):
    autoretry_for: Optional[List[Type[Exception]]]
    max_retries: Optional[int]
    retry_backoff: Optional[bool | float]
    retry_backoff_max: Optional[float]
    retry_jitter: Optional[float]


def compile_exception_list(retry_for: List[str]) -> List[Type[Exception]]:
    result: List[Type[Exception]] = []
    for retry_fqn in retry_for:
        retry_exception = get_class_from_fully_qualified_name(retry_fqn)
        if not issubclass(retry_exception, Exception):
            raise ValueError(
                f"The class {retry_fqn} is not a subclass of {Exception.__class__}"
            )
        result.append(retry_exception)
    return result
