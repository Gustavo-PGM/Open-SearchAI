import asyncio
from workflow import run_news_workflow

async def main():
    result = await run_news_workflow("Quem é o atual técnico da seleção brasileira")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())