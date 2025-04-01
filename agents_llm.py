from agents import Agent
from llm import model
from scrapy import get_news_articles


def create_agent(name, instructions, tools=None):
    return Agent(
        name=name,
        instructions=instructions,
        tools=tools if model.supports_tools else [],
        model=model
    )

news_agent = create_agent(
    name="Assistente de Notícias",
    instructions="""Analise DETALHADAMENTE o conteúdo das URLs...""",
    tools=[get_news_articles]
)

editor_agent = create_agent(
    name="Assistente de Editor",
    instructions="""Sintetize as informações em tópicos claros..."""
)