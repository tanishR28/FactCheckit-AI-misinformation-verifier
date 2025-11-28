import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime

async def scrape_news_search(claim: str) -> dict:
    """
    Scrapes DuckDuckGo for news results (no API key needed).
    
    Args:
        claim: The claim to search for
    
    Returns:
        Dictionary with search results
    """
    try:
        # Use DuckDuckGo HTML (no API key needed)
        search_query = f"{claim} news fact check"
        url = f"https://html.duckduckgo.com/html/?q={search_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    result_divs = soup.find_all('div', class_='result', limit=5)
                    
                    for div in result_divs:
                        title_tag = div.find('a', class_='result__a')
                        snippet_tag = div.find('a', class_='result__snippet')
                        
                        if title_tag:
                            title = title_tag.get_text(strip=True)
                            url_link = title_tag.get('href', '')
                            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
                            
                            # Extract domain
                            domain = ""
                            url_tag = div.find('a', class_='result__url')
                            if url_tag:
                                domain = url_tag.get_text(strip=True)
                            
                            results.append({
                                "title": title,
                                "snippet": snippet,
                                "url": url_link,
                                "displayLink": domain,
                                "source": "DuckDuckGo"
                            })
                    
                    print(f"DuckDuckGo scraper found {len(results)} results")
                    return {
                        "results": results,
                        "total": len(results),
                        "query": search_query,
                        "source": "web_scraper"
                    }
                else:
                    print(f"DuckDuckGo scraper status: {response.status}")
                    return {"results": [], "error": f"Status {response.status}"}
                    
    except asyncio.TimeoutError:
        print("Web scraper timeout")
        return {"results": [], "error": "Timeout"}
    except Exception as e:
        print(f"Web scraper error: {str(e)}")
        return {"results": [], "error": str(e)}


async def scrape_news_api(claim: str) -> dict:
    """
    Uses NewsAPI.org free tier (100 requests/day, no credit card).
    You can get free key from: https://newsapi.org/register
    
    Args:
        claim: The claim to search for
    
    Returns:
        Dictionary with news results
    """
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    news_api_key = os.getenv("NEWS_API_KEY", "")
    
    if not news_api_key:
        print("No NEWS_API_KEY found, skipping NewsAPI")
        return {"results": [], "error": "No API key"}
    
    try:
        # Search news from last 7 days
        search_query = claim.replace(" ", " AND ")
        url = f"https://newsapi.org/v2/everything"
        
        params = {
            "q": search_query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5,
            "apiKey": news_api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get("articles", [])
                    
                    results = []
                    for article in articles[:5]:
                        results.append({
                            "title": article.get("title", ""),
                            "snippet": article.get("description", ""),
                            "url": article.get("url", ""),
                            "displayLink": article.get("source", {}).get("name", ""),
                            "publishedAt": article.get("publishedAt", ""),
                            "source": "NewsAPI"
                        })
                    
                    print(f"NewsAPI found {len(results)} results")
                    return {
                        "results": results,
                        "total": len(results),
                        "query": search_query
                    }
                else:
                    error_data = await response.text()
                    print(f"NewsAPI error: {response.status} - {error_data}")
                    return {"results": [], "error": f"Status {response.status}"}
                    
    except Exception as e:
        print(f"NewsAPI error: {str(e)}")
        return {"results": [], "error": str(e)}
