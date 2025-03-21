import uuid

from genie_flow_invoker.doc_proc import DocumentChunk, NAMESPACE_DOC_PROC


def test_document_chunk():
    document = DocumentChunk(
        content="Aap Noot Mies",
        original_span=(0, 12),
        hierarchy_level=0,
        parent_id=None,
    )

    expected_chunk_id = str(uuid.uuid5(NAMESPACE_DOC_PROC, "Aap Noot Mies"))

    assert document.chunk_id == expected_chunk_id
    assert document.original_span == (0, 12)
    assert document.hierarchy_level == 0
    assert document.parent_id is None
