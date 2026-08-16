from services.agent_service import AgentService


agent = AgentService()


response = agent.ask(
    "How many weeks of maternity leave are provided?"
)


print("\nAGENT RESPONSE:")
print(response)