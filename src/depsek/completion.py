# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from .utils import (default_model,
                    query)


def complete(text, **kwargs):
    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            n               = 1 to 128
            best_of         = 4
            frequency_penalty = -2.0 to 2.0
            presence_penalty = -2.0 to 2.0
            max_tokens      = number of tokens
            logprobs        = number up to 5
            stop            = ["stop"]  array of up to 4 sequences
            logit_bias      = map token: bias -1.0 to 1.0 (restrictive -100 to 100)
    """
    responses = []
    payload = {
        "model":            kwargs.get("model", default_model),
        "prompt":           kwargs.get("prompt", text),
        "response_format":  kwargs.get('response_format', {'type': 'text'}),
        "reasoning_effort": kwargs.get("reasoning_effort", "high"),
        "reasoning_history":kwargs.get("reasoning_history", "interleaved"),
        "thinking":         kwargs.get("thinking", None),
        "max_tokens":       kwargs.get("max_tokens", 5),
        "n":                kwargs.get("n", 1),
        "stop":             kwargs.get("stop_sequences", ["stop"]),
        # "seed":             kwargs.get("seed", None),
        "frequency_penalty":kwargs.get("frequency_penalty", 0),
        "presence_penalty": kwargs.get("presence_penalty", 0),
        # "logit_bias":       kwargs.get("logit_bias", None),
        "logprobs":         kwargs.get("logprobs", None),
        # "top_logprobs":     kwargs.get("top_logprobs", None),
        "temperature":      kwargs.get("temperature", 1),
        "top_p":            kwargs.get("top_p", 1),
        'top_k':            kwargs.get('top_k', 50),
        'stream':           False,
        # "user":             kwargs.get("user", None)
    }

    responses = query(payload, '/completions')
    response = responses['choices'][0]
    text = response['text']
    thoughts = ''

    return thoughts, text


if __name__ == '__main__':
    ...