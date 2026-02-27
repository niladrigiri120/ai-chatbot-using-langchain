from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

model = ChatGroq(
    model= "openai/gpt-oss-20b",
    api_key= os.getenv("Groq_api_key")
    streaming= True
    )

chat_history = [SystemMessage(content= 'You are a good AI assistant')]

while True:
    user_input = input('You: ')
    chat_history.append(HumanMessage(content= user_input))
    if user_input.lower() == "exit":
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content= result.content))

    print("AI: ",result.content)





