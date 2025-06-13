from .instructions import CUSTOMER_AGENT_INSTRUCTIONS, CUSTOMER_SUPPORT_AGENT, ORDER_AGENT_INSTRUCTIONS
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
from tools.update_customer_details import update_customer_details
from tools.fetch_products import get_products
from tools.fetch_orders import fetch_orders
from tools.cancel_order import cancel_order
from dotenv import load_dotenv
import os

load_dotenv()

set_tracing_disabled(disabled=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

provider = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key,
)

model = OpenAIChatCompletionsModel(
    openai_client=provider,
    model='gemini-2.0-flash'
)

customer_agent = Agent(
    name="Customer Service Agent",
    instructions=CUSTOMER_AGENT_INSTRUCTIONS,
    model=model,
    tools=[update_customer_details],
)

order_agent = Agent(
    name="Order Service Agent",
    instructions=ORDER_AGENT_INSTRUCTIONS,
    model=model,
    tools=[fetch_orders, cancel_order],
)

agent = Agent(
    name="Customer Support Agent",
    instructions=CUSTOMER_SUPPORT_AGENT,
    model=model,
    tools=[fetch_orders, get_products, cancel_order],
    handoffs=[customer_agent]
)