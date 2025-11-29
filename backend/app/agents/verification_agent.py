from app.tools.google_factcheck import search_fact_check_api
from app.tools.google_search import search_google
from app.tools.web_scraper import scrape_news_search, scrape_news_api
from app.tools.indian_factcheckers import search_all_indian_factcheckers
from app.agents.research_agent import analyze_with_gemini
from app.utils.preprocess import clean_text
import asyncio

async def verify_claim(claim: str) -> dict:
    """
    Verifies a claim using multiple sources and AI analysis.
    
    Args:
        claim: The extracted factual claim to verify
    
    Returns:
        Dictionary containing verification results from all sources
    """
    try:
        # Clean the claim
        cleaned_claim = clean_text(claim)
        
        # Run verification tools in parallel (Google APIs + Indian Fact-Checkers + Web Scraper)
        fact_check_task = search_fact_check_api(cleaned_claim)
        google_search_task = search_google(cleaned_claim)
        indian_factcheckers_task = search_all_indian_factcheckers(cleaned_claim)
        web_scraper_task = scrape_news_search(cleaned_claim)
        news_api_task = scrape_news_api(cleaned_claim)
        
        # Wait for all results
        fact_check_results, google_results, indian_results, scraper_results, news_results = await asyncio.gather(
            fact_check_task,
            google_search_task,
            indian_factcheckers_task,
            web_scraper_task,
            news_api_task,
            return_exceptions=True
        )
        
        # Handle exceptions
        if isinstance(fact_check_results, Exception):
            print(f"Fact Check API error: {fact_check_results}")
            fact_check_results = {"claims": [], "error": str(fact_check_results)}
            
        if isinstance(google_results, Exception):
            print(f"Google Search error: {google_results}")
            google_results = {"results": [], "error": str(google_results)}
        
        if isinstance(indian_results, Exception):
            print(f"Indian fact-checkers error: {indian_results}")
            indian_results = {"results": [], "error": str(indian_results)}
        
        if isinstance(scraper_results, Exception):
            print(f"Web scraper error: {scraper_results}")
            scraper_results = {"results": [], "error": str(scraper_results)}
            
        if isinstance(news_results, Exception):
            print(f"NewsAPI error: {news_results}")
            news_results = {"results": [], "error": str(news_results)}
        
        # Combine all search results (Indian Fact-Checkers + Google + Scraper + NewsAPI)
        all_search_results = []
        all_search_results.extend(indian_results.get("results", []))  # Prioritize Indian sources
        all_search_results.extend(google_results.get("results", []))
        all_search_results.extend(scraper_results.get("results", []))
        all_search_results.extend(news_results.get("results", []))
        
        print(f"🇮🇳 Total search results: {len(all_search_results)} (Indian: {len(indian_results.get('results', []))}, Google: {len(google_results.get('results', []))}, Scraper: {len(scraper_results.get('results', []))}, NewsAPI: {len(news_results.get('results', []))})")
        
        # Use Gemini AI to analyze all search results
        ai_analysis = await analyze_with_gemini(cleaned_claim, all_search_results)
        
        # Compile verification results
        verification_results = {
            "claim": claim,
            "cleaned_claim": cleaned_claim,
            "fact_check_api": fact_check_results,
            "indian_factcheckers": indian_results,
            "google_search": google_results,
            "web_scraper": scraper_results,
            "news_api": news_results,
            "ai_analysis": ai_analysis,
            "verification_summary": {
                "fact_check_found": len(fact_check_results.get("claims", [])) > 0,
                "indian_results_count": len(indian_results.get("results", [])),
                "google_results_count": len(google_results.get("results", [])),
                "scraper_results_count": len(scraper_results.get("results", [])),
                "news_results_count": len(news_results.get("results", [])),
                "ai_confidence": ai_analysis.get("confidence", 0.0),
                "total_sources": len(all_search_results) + len(fact_check_results.get("claims", []))
            }
        }
        
        return verification_results
        
    except Exception as e:
        print(f"Error in verification agent: {str(e)}")
        return {
            "claim": claim,
            "error": str(e),
            "fact_check_api": {"claims": []},
            "google_search": {"results": []},
            "ai_analysis": {
                "verdict_suggestion": "UNVERIFIED",
                "confidence": 0.0,
                "reasoning": [f"Error: {str(e)}"]
            },
            "verification_summary": {
                "fact_check_found": False,
                "google_results_count": 0,
                "ai_confidence": 0.0,
                "total_sources": 0
            }
        }
