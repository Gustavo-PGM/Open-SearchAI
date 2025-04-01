from agents_llm import news_agent, editor_agent
from agents import Runner
from htmlText import save_news_to_html
from llm import model
from scrapy import get_news_articles

async def run_news_workflow(topic):
    print(f"\n🚀 Iniciando busca por: {topic}")
    
    if model.supports_tools:
       
        raw_response = await Runner.run(
            news_agent,
            f"Busque notícias recentes sobre {topic}"
        )
        raw_content = raw_response.final_output
    else:
        
        raw_content = await get_news_articles(topic)
    
    edited_response = await Runner.run(
        editor_agent,
        f"Formate seguindo o template padrão:\n\n{raw_content}"
    )
    
    save_news_to_html(topic, edited_response.final_output)
    return edited_response.final_output
