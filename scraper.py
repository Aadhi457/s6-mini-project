import requests
import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentScraper:
    def __init__(self, download_dir: str = "samples/scraped"):
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download_file(self, url: str) -> Optional[str]:
        """Downloads a single file from a URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Extract filename from URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = "downloaded_file.bin"
            
            filepath = os.path.join(self.download_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Successfully downloaded {url} to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            return None

    def scrape_links(self, url: str) -> List[str]:
        """Scrapes all links from a webpage."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for a_tag in soup.find_all('a', href=True):
                full_url = urljoin(url, a_tag['href'])
                links.append(full_url)
            
            logger.info(f"Found {len(links)} links on {url}")
            return links
        except Exception as e:
            logger.error(f"Failed to scrape links from {url}: {e}")
            return []

if __name__ == "__main__":
    # Example usage
    scraper = ContentScraper()
    # Let's test with a benign URL
    links = scraper.scrape_links("http://example.com")
    print(f"Links found: {links}")
