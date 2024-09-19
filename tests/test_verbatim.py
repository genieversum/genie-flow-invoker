from genie_flow_invoker.invoker.verbatim import VerbatimInvoker

def test_verbatim():
    invoker = VerbatimInvoker()
    text = "The Quick Brown Fox Jumped over the lazy dog."

    result = invoker.invoke(text)
    assert result == text
