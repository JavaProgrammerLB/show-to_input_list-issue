import os
from agents import Agent, RunConfig,Runner, OpenAIChatCompletionsModel, TResponseInputItem, set_tracing_disabled
from openai import AsyncOpenAI, BaseModel
from openai.types.responses import ResponseTextDeltaEvent
from fastapi.responses import StreamingResponse
import json
from dotenv import load_dotenv
import traceback
from fastapi import FastAPI

from session_service import SessionService

app = FastAPI()


set_tracing_disabled(disabled=True)


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL")

MODEL_NAME = "openai/gpt-4o-mini"

openai_client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=openai_client
)


class ChatRequest(BaseModel):
    message: str;
    sessionId: str;


@app.post("/chat")
async def root(request: ChatRequest):
    chat_agent = Agent(
        name="Chat Agent",
        instructions="[chat for fun]",
        model=model
    )
    
    session_service = SessionService()
    input_items: list[TResponseInputItem] = []
    input_items = session_service.get_session(request.sessionId)
    input_items.append({"role": "user", "content": request.message})
    
    result = Runner.run_streamed(starting_agent=chat_agent, input=input_items, run_config=RunConfig(group_id=request.sessionId))
    endFlag = '\n\n'
    
    async def generate():
        try:
            
            async for event in result.stream_events():
                if (event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent)):
                    yield f"data: {json.dumps(event.data.delta, ensure_ascii=False)}{endFlag}"
                elif event.type == "agent_updated_stream_event":
                    pass
                elif event.type == "run_item_stream_event":
                    if event.item.type == "tool_call_item":
                        yield f"tool: {json.dumps(event.item.raw_item.model_dump(), ensure_ascii=False)}{endFlag}"
                    elif event.item.type == "tool_call_output_item":
                        yield f"result: {json.dumps(event.item.output, ensure_ascii=False)}{endFlag}"
                    elif event.item.type == "message_output_item":
                        pass
                    else:
                        pass
            input_items = result.to_input_list()
            session_service.set_session(request.sessionId, input_items)
                    
        except Exception as e:             
            error_info = traceback.format_exc()
            print(f"Stack trace:\n{error_info}")
        finally:
            print('finally')

    return StreamingResponse(generate(), media_type="text/event-stream")