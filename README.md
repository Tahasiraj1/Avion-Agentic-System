# Avion-Agentic-System

## Project Description
This project is an implementation of an Avion agentic system using Python and MongoDB. The system is designed to manage customer orders and customer details, as well as provide support for customers. The system uses a combination of tools and agents to interact with the customer and provide assistance.

## System Architecture
The system is designed to be a modular and scalable solution, with each component being a separate module. The system consists of the following components:

1. MongoDB: A NoSQL database used to store customer orders, customer details, and order items.
2. Agents: A collection of agents that interact with the customer and provide assistance. Each agent has a set of tools that it can use to perform tasks.
3. Tools: A collection of tools that the agents can use to perform tasks. These tools interact with the MongoDB database to retrieve and update data.
4. API: A RESTful API that allows the customer to interact with the system using a chat interface. The API uses the agents to provide assistance and interact with the MongoDB database.