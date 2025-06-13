how to run the project

```
uv venv
```

```
fastapi dev main.py
```

open `http://127.0.0.1:8000/docs`

Try it out
- post a message
```
{
  "message": "tell me a joke",
  "sessionId": "mock_session_id"
}
```

- post another message
```
{
  "message": "tell me a story",
  "sessionId": "mock_session_id"
}
```
now the error occur:
```
Stack trace:
Traceback (most recent call last):
  File "/Users/user/Program/show-to_input_list-issue/main.py", line 60, in generate
    async for event in result.stream_events():
  File "/Users/user/Program/show-to_input_list-issue/.venv/lib/python3.12/site-packages/agents/result.py", line 215, in stream_events
    raise self._stored_exception
  File "/Users/user/Program/show-to_input_list-issue/.venv/lib/python3.12/site-packages/agents/run.py", line 574, in _run_streamed_impl
    turn_result = await cls._run_single_turn_streamed(
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/user/Program/show-to_input_list-issue/.venv/lib/python3.12/site-packages/agents/run.py", line 698, in _run_single_turn_streamed
    async for event in model.stream_response(
  File "/Users/user/Program/show-to_input_list-issue/.venv/lib/python3.12/site-packages/agents/models/openai_chatcompletions.py", line 150, in stream_response
    response, stream = await self._fetch_response(
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/user/Program/show-to_input_list-issue/.venv/lib/python3.12/site-packages/agents/models/openai_chatcompletions.py", line 218, in _fetch_response
    converted_messages = Converter.items_to_messages(input)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/user/Program/show-to_input_list-issue/.venv/lib/python3.12/site-packages/agents/models/chatcmpl_converter.py", line 435, in items_to_messages
    raise UserError(f"Unhandled item type or structure: {item}")
agents.exceptions.UserError: Unhandled item type or structure: [{'role': 'user', 'content': 'tell me a joke'}, {'id': '__fake_id__', 'content': [{'annotations': [], 'text': "Sure! Why don't skeletons fight each other?\n\nBecause they don't have the guts!", 'type': 'output_text'}], 'role': 'assistant', 'status': 'completed', 'type': 'message'}]

finally
```
