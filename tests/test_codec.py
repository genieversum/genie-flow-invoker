import base64
from typing import Any

import binascii
import json

from genie_flow_invoker.codec import JsonOutputEncoder, JsonInputDecoder


def test_json_encoding():
    o = dict(aap=10, noot="mies")
    encoder = JsonOutputEncoder()
    s = encoder._encode_output(o)

    assert s == '{"aap": 10, "noot": "mies"}'


def test_json_decoding():
    s = '{"aap": 10, "noot": "mies"}'
    decoder = JsonInputDecoder()
    o = decoder._decode_input(s)

    assert o == dict(aap=10, noot="mies")


def test_alternative_encoder():

    class BinaryEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, bytes):
                return base64.b64encode(o).decode('ascii')
            return json.JSONEncoder.default(self, o)

    class AlternativeEncoder(JsonOutputEncoder):

        @property
        def default_encoder(self):
            return BinaryEncoder

    o = dict(aap=10, noot=b"mies")
    encoder = AlternativeEncoder()
    s = encoder._encode_output(o)

    assert s == '{"aap": 10, "noot": "bWllcw=="}'


def test_alternative_decoder():

    class AlternativeDecoder(JsonInputDecoder):
        def object_pair_decode(self, object_pairs: list[tuple[str, Any]]):
            def decode_or_not(s):
                try:
                    return base64.b64decode(s.encode('ascii'))
                except (binascii.Error, AttributeError):
                    return s

            return {
                k: decode_or_not(v)
                for k, v in object_pairs
            }

    s = '{"aap": 10, "noot": "bWllcw=="}'
    decoder = AlternativeDecoder()
    o = decoder._decode_input(s)

    assert o == dict(aap=10, noot=b"mies")
