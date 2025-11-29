"""
Indian Fact-Checkers Integration
Scrapes verified fact-check sources from India:
- PIB Fact Check (Government of India)
- Alt News (Independent)
- BOOM Live (Independent)
- Factly (Independent)
- Vishvas News (PIB Initiative)
"""

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
import re

async def scrape_pib_factcheck(claim: str) -> dict:
    """
    Scrapes PIB Fact Check (Press Information Bureau - Government of India)
    Official government fact-checking portal
    """
    try:
        search_query = claim.replace(" ", "+")
        url = f"https://factcheck.pib.gov.in/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    articles = soup.find_all('article', class_='post', limit=3)
                    
                    for article in articles:
                        title_tag = article.find('h2', class_='entry-title')
                        link_tag = title_tag.find('a') if title_tag else None
                        content_tag = article.find('div', class_='entry-content')
                        
                        if title_tag and link_tag:
                            title = title_tag.get_text(strip=True)
                            url_link = link_tag.get('href', '')
                            snippet = content_tag.get_text(strip=True)[:200] if content_tag else ""
                            
                            # Determine verdict from title
                            title_lower = title.lower()
                            verdict = "UNVERIFIED"
                            if any(word in title_lower for word in ['fake', 'false', 'misleading', 'morphed']):
                                verdict = "FALSE"
                            elif any(word in title_lower for word in ['true', 'genuine', 'verified']):
                                verdict = "TRUE"
                            
                            results.append({
                                "title": title,
                                "snippet": snippet,
                                "url": url_link,
                                "source": "PIB Fact Check (Govt. of India)",
                                "verdict": verdict,
                                "credibility": "high"
                            })
                    
                    print(f"PIB Fact Check found {len(results)} results")
                    return {"results": results, "source": "pib_factcheck"}
                else:
                    return {"results": [], "error": f"Status {response.status}"}
                    
    except Exception as e:
        print(f"PIB Fact Check error: {str(e)}")
        return {"results": [], "error": str(e)}


async def scrape_altnews(claim: str) -> dict:
    """
    Scrapes Alt News - Award-winning independent fact-checking website
    """
    try:
        search_query = claim.replace(" ", "+")
        url = f"https://www.altnews.in/?s={search_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    articles = soup.find_all('article', limit=3)
                    
                    for article in articles:
                        title_tag = article.find('h3', class_='entry-title')
                        link_tag = title_tag.find('a') if title_tag else None
                        excerpt_tag = article.find('div', class_='entry-content')
                        
                        if title_tag and link_tag:
                            title = title_tag.get_text(strip=True)
                            url_link = link_tag.get('href', '')
                            snippet = excerpt_tag.get_text(strip=True)[:200] if excerpt_tag else ""
                            
                            # Determine verdict
                            title_lower = title.lower()
                            verdict = "UNVERIFIED"
                            if any(word in title_lower for word in ['fake', 'false', 'misleading', 'doctored', 'morphed']):
                                verdict = "FALSE"
                            elif any(word in title_lower for word in ['fact check:', 'debunked']):
                                verdict = "MISLEADING"
                            
                            results.append({
                                "title": title,
                                "snippet": snippet,
                                "url": url_link,
                                "source": "Alt News",
                                "verdict": verdict,
                                "credibility": "high"
                            })
                    
                    print(f"Alt News found {len(results)} results")
                    return {"results": results, "source": "altnews"}
                else:
                    return {"results": [], "error": f"Status {response.status}"}
                    
    except Exception as e:
        print(f"Alt News error: {str(e)}")
        return {"results": [], "error": str(e)}


async def scrape_boom_live(claim: str) -> dict:
    """
    Scrapes BOOM Live - Leading Indian fact-checking organization
    """
    try:
        search_query = claim.replace(" ", "%20")
        url = f"https://www.boomlive.in/?s={search_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    articles = soup.find_all('div', class_='story-card', limit=3)
                    
                    for article in articles:
                        title_tag = article.find('h2', class_='story-card__title')
                        link_tag = article.find('a', class_='story-card__url')
                        desc_tag = article.find('p', class_='story-card__description')
                        
                        if title_tag and link_tag:
                            title = title_tag.get_text(strip=True)
                            url_link = link_tag.get('href', '')
                            if not url_link.startswith('http'):
                                url_link = f"https://www.boomlive.in{url_link}"
                            snippet = desc_tag.get_text(strip=True) if desc_tag else ""
                            
                            # Determine verdict
                            title_lower = title.lower()
                            verdict = "UNVERIFIED"
                            if any(word in title_lower for word in ['fake', 'false', 'misleading', 'viral lie']):
                                verdict = "FALSE"
                            elif 'fact check' in title_lower:
                                verdict = "MISLEADING"
                            
                            results.append({
                                "title": title,
                                "snippet": snippet,
                                "url": url_link,
                                "source": "BOOM Live",
                                "verdict": verdict,
                                "credibility": "high"
                            })
                    
                    print(f"BOOM Live found {len(results)} results")
                    return {"results": results, "source": "boom"}
                else:
                    return {"results": [], "error": f"Status {response.status}"}
                    
    except Exception as e:
        print(f"BOOM Live error: {str(e)}")
        return {"results": [], "error": str(e)}


async def scrape_factly(claim: str) -> dict:
    """
    Scrapes Factly - South Indian fact-checking organization
    """
    try:
        search_query = claim.replace(" ", "+")
        url = f"https://factly.in/?s={search_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    articles = soup.find_all('article', limit=3)
                    
                    for article in articles:
                        title_tag = article.find('h2', class_='entry-title')
                        link_tag = title_tag.find('a') if title_tag else None
                        excerpt_tag = article.find('div', class_='entry-summary')
                        
                        if title_tag and link_tag:
                            title = title_tag.get_text(strip=True)
                            url_link = link_tag.get('href', '')
                            snippet = excerpt_tag.get_text(strip=True)[:200] if excerpt_tag else ""
                            
                            # Determine verdict
                            title_lower = title.lower()
                            verdict = "UNVERIFIED"
                            if any(word in title_lower for word in ['fake', 'false', 'misleading']):
                                verdict = "FALSE"
                            elif 'fact check' in title_lower:
                                verdict = "MISLEADING"
                            
                            results.append({
                                "title": title,
                                "snippet": snippet,
                                "url": url_link,
                                "source": "Factly",
                                "verdict": verdict,
                                "credibility": "medium"
                            })
                    
                    print(f"Factly found {len(results)} results")
                    return {"results": results, "source": "factly"}
                else:
                    return {"results": [], "error": f"Status {response.status}"}
                    
    except Exception as e:
        print(f"Factly error: {str(e)}")
        return {"results": [], "error": str(e)}


async def scrape_vishvas_news(claim: str) -> dict:
    """
    Scrapes Vishvas News - PIB's multilingual fact-checking initiative
    """
    try:
        search_query = claim.replace(" ", "+")
        url = f"https://www.vishvasnews.com/?s={search_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    articles = soup.find_all('article', limit=3)
                    
                    for article in articles:
                        title_tag = article.find('h2')
                        link_tag = title_tag.find('a') if title_tag else None
                        content_tag = article.find('div', class_='entry-content')
                        
                        if title_tag and link_tag:
                            title = title_tag.get_text(strip=True)
                            url_link = link_tag.get('href', '')
                            snippet = content_tag.get_text(strip=True)[:200] if content_tag else ""
                            
                            # Determine verdict
                            title_lower = title.lower()
                            verdict = "UNVERIFIED"
                            if any(word in title_lower for word in ['fake', 'false', 'misleading', 'गलत', 'भ्रामक']):
                                verdict = "FALSE"
                            elif any(word in title_lower for word in ['true', 'सही', 'सत्य']):
                                verdict = "TRUE"
                            
                            results.append({
                                "title": title,
                                "snippet": snippet,
                                "url": url_link,
                                "source": "Vishvas News (PIB)",
                                "verdict": verdict,
                                "credibility": "high"
                            })
                    
                    print(f"Vishvas News found {len(results)} results")
                    return {"results": results, "source": "vishvas"}
                else:
                    return {"results": [], "error": f"Status {response.status}"}
                    
    except Exception as e:
        print(f"Vishvas News error: {str(e)}")
        return {"results": [], "error": str(e)}


async def search_all_indian_factcheckers(claim: str) -> dict:
    """
    Search all Indian fact-checkers in parallel
    Returns combined results from all sources
    """
    try:
        # Run all scrapers in parallel
        results = await asyncio.gather(
            scrape_pib_factcheck(claim),
            scrape_altnews(claim),
            scrape_boom_live(claim),
            scrape_factly(claim),
            scrape_vishvas_news(claim),
            return_exceptions=True
        )
        
        # Combine all results
        all_results = []
        for result in results:
            if isinstance(result, dict) and not isinstance(result, Exception):
                all_results.extend(result.get("results", []))
        
        print(f"🇮🇳 Total Indian fact-checker results: {len(all_results)}")
        
        return {
            "results": all_results,
            "total": len(all_results),
            "sources": ["PIB", "Alt News", "BOOM", "Factly", "Vishvas News"]
        }
        
    except Exception as e:
        print(f"Indian fact-checkers error: {str(e)}")
        return {"results": [], "error": str(e)}
