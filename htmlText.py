import markdown
import re

def save_news_to_html(topic, edited_news):
    basic_css = """
    <style>
        body { 
            font-family: system-ui, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
            color: #333;
        }
        h1 {
            color: #2B6CB0;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 0.5rem;
        }
        h3 {
            color: #2D3748;
            margin: 1.5rem 0 0.5rem;
        }
        a {
            color: #2B6CB0;
            text-decoration: none;
            font-size: 0.9em;
        }
        a:hover {
            text-decoration: underline;
        }
        .url {
            display: block;
            margin: 0.5rem 0;
            color: #4A5568;
        }
        hr {
            border: 0;
            height: 1px;
            background: #E2E8F0;
            margin: 2rem 0;
        }
    </style>
    """
    


    safe_topic = re.sub(r'[<>:"/\\|?*]', '_', topic)
    safe_topic = safe_topic.strip()[:50]

  
    edited_news_html = markdown.markdown(edited_news)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Notícias sobre {topic}</title>
        {basic_css}
    </head>
    <body>
        <h1>Notícias sobre {topic}</h1>
        {edited_news_html}
    </body>
    </html>
    """
    
    with open(f"{safe_topic}.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("\n✅ Arquivo HTML gerado com sucesso!")