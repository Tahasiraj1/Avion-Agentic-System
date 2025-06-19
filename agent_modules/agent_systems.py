from tools import update_customer_details, fetch_customer_details, get_products, fetch_orders, cancel_order, update_order
from .instructions import TRIAGE_AGENT, CUSTOMER_SUPPORT_AGENT, ORDER_AGENT_INSTRUCTIONS, PRODUCT_AGENT_INSTRUCTIONS
from helper import get_gemini_model
from agents import Agent

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
    tools=[fetch_orders, cancel_order, update_order],
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