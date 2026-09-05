import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re

# 1. Base Class for Scraper Adapters
class BaseJobScraper:
    async def fetch_page(self, session, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                return None
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            return None

# 2. Generic HTML Job Scraper Adapter
class GenericWebJobScraper(BaseJobScraper):
    def clean_html(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
        text = soup.get_text(separator=' ')
        # Clean extra spaces
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text

    async def scrape_job_url(self, url):
        async with aiohttp.ClientSession() as session:
            print(f"⏳ Fetching job details from URL: {url}")
            html_content = await self.fetch_page(session, url)
            
            if not html_content:
                return {"error": "Failed to retrieve webpage content."}
            
            cleaned_text = self.clean_html(html_content)
            
            # Simple Title Extraction from HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.title.string.strip() if soup.title else "Unknown Job Title"
            
            return {
                "title": title,
                "description": cleaned_text[:2000], # First 2000 chars of extracted content
                "raw_text_length": len(cleaned_text),
                "source_url": url
            }

# 3. Direct Test Execution
async def main():
    scraper = GenericWebJobScraper()
    # Sample Test URL
    test_url = "https://httpbin.org/html" 
    result = await scraper.scrape_job_url(test_url)
    
    print("\n--- Scraper Result ---")
    print("Title:", result.get("title"))
    print("Text Length:", result.get("raw_text_length"))
    print("Sample Content:", result.get("description")[:200], "...")

if __name__ == "__main__":
    asyncio.run(main())