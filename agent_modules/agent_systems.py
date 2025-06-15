from .instructions import TRIAGE_AGENT, CUSTOMER_SUPPORT_AGENT, ORDER_AGENT_INSTRUCTIONS, PRODUCT_AGENT_INSTRUCTIONS
from tools.update_customer_details import update_customer_details
from tools.fetch_customer_details import fetch_customer_details
from helper.gemini_model import get_gemini_model
from agents import Agent
from tools.fetch_products import get_products
from tools.fetch_orders import fetch_orders
from tools.cancel_order import cancel_order

model = get_gemini_model()

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