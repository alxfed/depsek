# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from .utils import (query,
                    decode,
                    default_model,
                    get_function,
                    get_func_args,
                    call_function)


def get_weather(location):
    # print(f"Executing weather tool for location: {location}")
    return {"temperature": "72F", "condition": "Sunny"}


def message(messages=None, instructions=None, tools=None, **kwargs):
    """A continuation of text with a given context and instruction.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 to ...
            max_tokens      = number of tokens
            stop            = ['stop']  array of up to 4 sequences
    """
    # instruction         = kwargs.get('system_instruction', instructions)
    # first_message       = [dict(role='system', content=instruction)] if instruction else []

    # contents can come in kwards or as an argument
    messages            = kwargs.get('messages', messages)

    # add contents and user text to the first (instruction) message
    # first_message.extend(messages)
    # instruction_and_contents = first_message

    payload = {
        'model':                    kwargs.get('model', default_model),
        'system':                   kwargs.get('system', instructions),
        'messages':                 kwargs.get('messages', messages),
        'output_config':            kwargs.get('output_config',{'effort': 'high'}),
        'thinking':                 kwargs.get('thinking', {
                                                            'type': 'enabled',
                                                            'budget_tokens': 10000,
                                                            }),
        'tool_choice':              kwargs.get('tool_choice', {'type': 'auto', 'disable_parallel_tool_use': False}),
        'max_tokens':               kwargs.get('max_tokens', 4096),
        'prompt_truncate_len':      kwargs.get('prompt_truncate_len', 100000),
        'n':                        kwargs.get('n', 1),
        'top_p':                    kwargs.get('top_p', 0.9),
        'top_k':                    kwargs.get('top_k', 10),
        'stream':                   False
    }
    if tools:
        payload['tools'] = tools
        payload['parallel_tool_calls'] = True
        payload['tool_choice'] = 'auto'

    while True:
        result = query(payload, '/messages')
        completion_message = result['content']
        thoughts, text, function_calls = decode(completion_message)
        if function_calls:
            payload['messages'].append({"role": "assistant", "content": completion_message})
            tools_results = []
            # Call all requested functions and create response messages.
            for function_call in function_calls:
                call_id = function_call.get('id')
                func_name = function_call.get('name', '')
                func_args_def = function_call.get('input', '{}')
                # Look up tool by name in globals and caller frames
                func = get_function(func_name)
                func_args = get_func_args(func_args_def)
                result = call_function(func, func_args)
                tool_message = {
                    "type": "tool_result",
                    "tool_use_id": call_id,
                    "content": result
                }
                tools_results.append(tool_message)

            # Add results to payload and make a query.
            payload['messages'].append({"role": "user", "content": tools_results})

        else:
            break

    return thoughts, text


if __name__ == '__main__':
    ...
