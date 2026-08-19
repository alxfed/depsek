# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from .utils import (query,
                    default_model,
                    decode_output)


def respond(messages=None, instructions=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    # Receive the instruction
    instruction = kwargs.get('system_instruction', instructions)

    # Define the initial payload
    payload = {
        "model":            kwargs.get("model", default_model),
        "instructions":     instruction,
        "input":            messages,
        "previous_response_id": kwargs.get("previous_response_id", None),
        "max_output_tokens": kwargs.get("max_tokens", 132000),
        "prompt_cache_retention": "in_memory",
        "include": ["reasoning.encrypted_content"],
        "reasoning": {
            "effort": "high",
            "summary": "detailed"
        }
    }
    # Query the API
    result = query(payload, '/responses')
    thoughts, text, _ = decode_output(result.get('output', {}))

    return thoughts, text


if __name__ == "__main__":
    ...