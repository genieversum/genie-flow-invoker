from dependency_injector import containers, providers

from genie_flow_invoker.invoker import VerbatimInvoker, AzureOpenAIChatInvoker, \
    AzureOpenAIChatJSONInvoker, WeaviateSimilaritySearchInvoker
from genie_flow_invoker.factory import InvokerFactory
from genie_flow_invoker.invoker import APIInvoker
from genie_flow_invoker.invoker import Neo4jInvoker


class GenieFlowInvokerContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    builtin_registry = providers.Dict(
        verbatim=providers.Object(VerbatimInvoker),
        azure_openai_chat=providers.Object(AzureOpenAIChatInvoker),
        azure_openai_chat_json=providers.Object(AzureOpenAIChatJSONInvoker),
        weaviate_similarity=providers.Object(WeaviateSimilaritySearchInvoker),
        api=providers.Object(APIInvoker),
        neo4j=providers.Object(Neo4jInvoker),
    )

    invoker_factory = providers.Factory(
        InvokerFactory,
        config=config,
        builtin_registry=builtin_registry,
    )
