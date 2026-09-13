from langchain_openai import ChatOpenAI
from app.core.config import setting

llm = ChatOpenAI(
    model=setting.OPENROUTER_MODEL,
    api_key=setting.OPENROUTER_API_KEY,
    base_url='https://openrouter.ai/api/v1',
    stream_usage=True
)

# user_msg = input("Enter your message:")
# messages = [
#     (
#         "system",
#         "You are a helpful assistant that gives me detail info about something that i ask of you?",
#     ),
#     ("human", f"{user_msg}"),
# ]
# ai_msg = llm.invoke(messages)
# print(ai_msg.text)