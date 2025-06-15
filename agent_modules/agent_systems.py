from .instructions import TRIAGE_AGENT, CUSTOMER_SUPPORT_AGENT, ORDER_AGENT_INSTRUCTIONS, PRODUCT_AGENT_INSTRUCTIONS
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
from tools.update_customer_details import update_customer_details
from tools.fetch_customer_details import fetch_customer_details
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
    model='gemini-2.5-flash-preview-05-20'
)

customer_agent = Agent(
    name="Customer Service Agent",
    instructions=CUSTOMER_SUPPORT_AGENT,
    model=model,
    tools=[update_customer_details, fetch_customer_details],
)

order_agent = Agent(
    name="Order Service Agent",
    instructions=ORDER_AGENT_INSTRUCTIONS,
    model=model,
    tools=[fetch_orders, cancel_order],
)

product_agent = Agent(
    name="Product Service Agent",
    instructions=PRODUCT_AGENT_INSTRUCTIONS,
    model=model,
    tools=[get_products],
)

triage_agent = Agent(
    name="Orchestrator Agent",
    instructions=TRIAGE_AGENT,
    model=model,
    handoffs=[customer_agent, order_agent, product_agent],
)