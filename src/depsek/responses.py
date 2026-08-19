# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from .utils import (query,
                    default_model,
                    get_function,
                    get_func_args,
                    call_function,
                    decode_output)


def get_weather(location):
    # print(f"Executing weather tool for location: {location}")
    return {"temperature": "72F", "condition": "Sunny"}


def respond(messages=None, instructions=None, tools=None, **kwargs):
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
    # Tools if there are some
    if tools:
        payload['tools'] = tools
        payload['parallel_tool_calls'] = True
        payload['max_tool_calls'] = kwargs.get("max_tool_calls", None)
        payload['tool_choice'] = 'auto'

    while True:
        # Query the API
        result = query(payload, '/responses')
        # id of the response
        response_id = result['id']
        thoughts, text, function_calls = decode_output(result.get('output', {}))

        if function_calls:
            function_outputs_messages = []
            for function_call in function_calls:
                call_id = function_call.get('call_id')
                func_name = function_call.get('name')
                func_args_str = function_call.get('arguments', {})

                # Look up tool by name in globals and in caller frames
                func = get_function(func_name)
                func_args = get_func_args(func_args_str)
                result = call_function(func, func_args)

                tool_message = {
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": result
                }
                function_outputs_messages.append(tool_message)

            # Now that all responses have been gathered
            # we can change the payload and send them back
            payload['previous_response_id'] = response_id
            payload['input'] = function_outputs_messages
        else:
            break

    return thoughts, text


if __name__ == "__main__":
    ...