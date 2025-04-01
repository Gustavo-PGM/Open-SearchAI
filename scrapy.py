from duckduckgo_search import DDGS
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
from llm import current_date


CONFIG = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'timeout': 20,
    'retries': 2,
    'max_text_length': 800
}

def sanitize_text(text):
    cleaned = re.sub(r'\s+', ' ', text).strip()
    return re.sub(r'[\x00-\x1F\x7F-\x9F]', '', cleaned)

async def extract_article_content(url):
    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True) 
        page = await browser.new_page()
        
        try:
           
            await page.goto(url, timeout=30000)
            
         
            await page.wait_for_selector("body", timeout=15000)
            
           
            html = await page.content()
            
           
            soup = BeautifulSoup(html, 'html.parser')
            
            
            for tag in soup.find_all(['nav', 'footer', 'script', 'style', 'iframe', 'noscript']):
                tag.decompose()
            
           
            article = soup.find('article') or soup.find('main') or soup.find('div', class_=re.compile(r'content|post'))
            
            if article:
                text = article.get_text(separator='\n', strip=True)
            else:
              
                elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])
                text = '\n'.join([e.get_text(strip=True) for e in elements if 50 < len(e.get_text(strip=True)) < 2000])
            
  
            cleaned = re.sub(r'\n{3,}', '\n\n', text)
            return cleaned[:1500] + " [...]" if len(cleaned) > 1500 else cleaned
            
        except Exception as e:
            print(f"🚨 Erro crítico em {url}: {str(e)}")
            return "Conteúdo não pôde ser extraído"
        finally:
            await browser.close()

async def get_news_articles(topic):
    print(f"\n🔍 Buscando notícias sobre: {topic}")
    ddg = DDGS()
    
    results = ddg.text(
        keywords=f"{topic} {current_date}",
        region='br-pt',
        max_results=6
    )
    
    if not results:
        return "Nenhum resultado encontrado"
    
    news_entries = []
    for result in results:
        if not result['href'].startswith(('http://', 'https://')):
            continue
            
        print(f"📡 Conectando em: {result['href']}")
        content = await extract_article_content(result['href'])
        
        entry = (
            f"### {result['title']}\n"
            f"**URL:** {result['href']}\n"
            f"**Conteúdo:**\n{content}\n"
            f"{'-'*40}"
        )
        news_entries.append(entry)
    
    return "\n\n".join(news_entries)