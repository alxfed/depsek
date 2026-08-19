# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import json
from os import environ
from .utils import (query,
                    default_model,
                    get_function,
                    get_func_args,
                    call_function)


def get_weather(location):
    print(f"Executing weather tool for location: {location}")
    return {"temperature": "72F", "condition": "Sunny"}
#
#
# def query(payload):
#     # Convert data dictionary to JSON and encode it to bytes
#     data_bytes = json.dumps(payload).encode('utf-8')
#     # Create the Request object
#     req = urllib.request.Request(
#         f'{api_base}/chat/completions',
#         data=data_bytes,
#         headers=headers,
#         method="POST")
#     # Try to query
#     try:
#         # Execute the request
#         with urllib.request.urlopen(req, timeout=3000) as response:
#             response_data = response.read().decode('utf-8')
#             output = json.loads(response_data)
#         return output
#
#     except urllib.error.HTTPError as e:
#         # Handle HTTP errors (e.g., 401 Unauthorized, 400 Bad Request)
#         error_info = e.read().decode('utf-8', errors='ignore')
#         print(f"HTTP Error {e.code}: {e.reason}")
#         print(f"Error Details: {error_info}")
#         return {}
#
#     except urllib.error.URLError as e:
#         # Handle network/connection errors
#         print(f"Failed to reach the server: {e.reason}")
#         return {}


def chat_complete(messages=None, instructions=None, tools=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    # Receive the instruction
    instruction = kwargs.get('system_instruction', instructions)
    first_message = [dict(role='system', content=instruction)] if instruction else []

    # add contents and user text to the first (instruction) message
    first_message.extend(messages)
    instruction_and_contents = first_message

    # Define the initial payload
    payload = {
        "model":            kwargs.get("model", default_model),
        "messages":         instruction_and_contents,
        "max_tokens":       kwargs.get("max_tokens", 132000),
        "reasoning_effort": "max",
    }
    # Tools if there are some
    if tools:
        payload['tools'] = tools
        payload['tool_choice'] = 'auto'

    while True:
        # Query the API
        result = query(payload, '/chat/completions')
        message = result['choices'][0]['message']
        instruction_and_contents.append(message)
        thoughts = message['reasoning_content']
        text = message['content']
        function_calls = message.get('tool_calls', [])

        if function_calls:
            for function_call in function_calls:
                call_id = function_call.get('id')
                func = function_call.get('function')
                func_name = func.get('name')
                func_args_str = func.get('arguments', '{}')

                try:
                    if isinstance(func_args_str, str):
                        func_args = json.loads(func_args_str)
                    else:
                        func_args = func_args_str
                except Exception as e:
                    func_args = {}
                    print(f"Error parsing tool arguments for {func_name}: {e}")

                # Look up tool by name in globals and caller frames
                func = globals().get(func_name)
                # if not func:
                #     import inspect
                #     frame = inspect.currentframe().f_back
                #     while frame:
                #         if func_name in frame.f_globals:
                #             func = frame.f_globals[func_name]
                #             break
                #         frame = frame.f_back

                if func and callable(func):
                    try:
                        tool_result = func(**func_args)
                        if isinstance(tool_result, (dict, list)):
                            result = json.dumps(tool_result)
                        else:
                            result = str(tool_result)
                    except Exception as e:
                        result = f"Error executing tool {func_name}: {str(e)}"
                        print(result)
                else:
                    result = f"Error: Tool function {func_name} not found."
                    print(result)

                tool_message = {
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": result
                }
                # Add the response
                instruction_and_contents.append(tool_message)
        else:
            break
    return thoughts, text


if __name__ == "__main__":

    def get_weather(location):
        print(f"Executing weather tool for location: {location}")
        return {"temperature": "72F", "condition": "Sunny"}

    get_weather_tool = {
      "type": "function",
      "function": {
          "name": "get_weather",
          "description": "Determine weather in my location",
          "parameters": {
              "type": "object",
              "properties": {
                  "location": {
                      "type": "string",
                      "description": "The city and state, e.g. San Francisco, CA"
                  },
              },
              "additionalProperties": False,
              "required": [
                  "location"
              ]
          }
      }
    }

    tools = [get_weather_tool]
    messages = [
        {"role": "user", "content": "Compare the weather in Oakland, CA and weather in Paris, France. Use the tool for learning both."}
    ]
    instructions = "You are a helpful assistant with tools."

    thought, txt = respond(messages, instructions, tools)
    print(thought, txt)
    ...
    """
    {
      "type": "function",
      "function": {
        "name": "submit_arbitrary_data",
        "description": "CRITICAL: You must invent and generate all keys for this payload based on the context. Do not send an empty object. Every key you create must map to a string value.",
        "strict": false,
        "parameters": {
          "type": "object",
          "properties": {},
          "additionalProperties": {
            "type": "string"
          }
        }
      }
    }
    
    Payload Rule: When executing the submit_arbitrary_data tool, you must dynamically generate the entire payload structure yourself. Analyze the user's input, extract all relevant variables, invent descriptive key names for them, and assign them values. Every single value must be a string.
    """