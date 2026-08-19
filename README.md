# DepSek
API calls to DepSek without dependencies.
<pre>
  pip install depsek
</pre>
Then:
```Python
# Python
from yaml import safe_load as yl
from depsek.chat import chat_complete as cc

kwargs = """  # this is a string in YAML format
  max_tokens:   32000
  stop_sequences:
    - STOP
    - "\nTitle"
  temperature:  1.0
  top_k:        10
  top_p:        0.5
  reasoning_effort: high
"""

instruction = 'You are a helpful assistant. Do not use markdown or lists in your responses.'

weather_tool = """ # YAML definition of a function (old format)
  type: function
  function:
    name: get_weather
    description: Determine weather in a location
    parameters:
      type: object
      properties:
        location:
          type: string
          description: The city and state, e.g. San Francisco, CA
      additionalProperties: false
      required:
        - location
"""

tools = [yl(weather_tool)]

msgs = [{'role': 'user', 'content': 'What is the weather in Chicago, IL and Paris, France?'}]

thoughts, text = cc(
    messages=msgs,
    instructions=instruction,
    tools=tools,
    **yl(kwargs)
)
```
or
```Python
from yaml import safe_load as yl
from depsek.messages import message


kwargs = """  # this is a string in YAML format
  max_tokens:   32000
  stop_sequences:
    - STOP
    - "\nTitle"
  temperature:  1.0
  top_k:        10
  top_p:        0.5
  thinking:     
    type: enabled
    budget_tokens: 24576
    display: summarized
  tool_choice:
    type: auto
    disable_parallel_tool_use: false
"""

instruction = 'You are a helpful assistant. Do not use markdown or lists in your responses.'

get_weather_tool_str = """ # YAML definition of a function
    name: get_weather
    description: Determine weather in a location
    input_schema:
      type: object
      properties:
        location:
          type: string
          description: The city and state, e.g. San Francisco, CA
      additionalProperties: true
      required:
        - location
    """

tools = [yl(get_weather_tool_str)]

msg = [{'role': 'user', 'content': 'What is the weather in Chicago, IL and Paris, France?'}]

thoughts, text = message(
    messages=msg,
    instructions=instruction,
    tools=tools,
    **yl(kwargs)
)
```
or

```Python
from yaml import safe_load as yl
from depsek.responses import respond


kwargs = """  # this is a string in YAML format
  model: accounts/fireworks/models/glm-5p2
  max_tokens:   64000
  temperature:  1.0
"""

msgs = [{'role': 'user', 'content': 'What is the weather in Chicago, IL and Paris, France?'}]

weather_tool = """ # YAML definition of a function (new format)
  type: function
  name: get_weather
  description: Determine weather in a location
  parameters:
    type: object
    properties:
      location:
        type: string
        description: The city and state, e.g. San Francisco, CA
    additionalProperties: false
    required:
      - location
"""

tools = [yl(weather_tool)]

instructions = """
You are a helpful assistant.
Rubric: respond in plain text without any markdown, emphasis or lists;
all paragraphs except the first one should begin with a newline and a tab.
"""

thougts, text = respond(
    messages=msgs,
    instructions=instructions,
    tools=tools,
    **yl(kwargs)
)
```
