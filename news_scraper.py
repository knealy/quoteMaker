import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from config import NEWS_SOURCES

class NewsScraperError(Exception):
    pass

class NewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.articles = []
    
    def fetch_news(self, max_articles=20):
        """Fetch financial news from configured sources"""
        self.articles = []
        
        for source in NEWS_SOURCES:
            try:
                response = requests.get(source['url'], headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract headlines and links - this is a generic approach
                # You may need to customize this for each source
                headlines = soup.find_all(['h1', 'h2', 'h3', 'h4'], limit=10)
                
                for headline in headlines:
                    if headline.find('a'):
                        link = headline.find('a').get('href', '')
                        title = headline.text.strip()
                        
                        # Make relative URLs absolute
                        if link and not link.startswith(('http://', 'https://')):
                            if link.startswith('/'):
                                base_url = '/'.join(source['url'].split('/')[:3])
                                link = base_url + link
                            else:
                                link = source['url'] + link
                        
                        if link and title and len(title) > 15:  # Filter out very short titles
                            self.articles.append({
                                'source': source['name'],
                                'title': title,
                                'url': link,
                                'date': datetime.now().strftime('%Y-%m-%d')
                            })
                
            except Exception as e:
                logging.error(f"Error fetching news from {source['name']}: {str(e)}")
        
        # Return the most recent articles, limiting to max_articles
        return self.articles[:max_articles]
    
    def fetch_article_content(self, article_url):
        """Fetch and extract the main content of an article"""
        try:
            response = requests.get(article_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract article paragraphs - this is a generic approach
            paragraphs = soup.find_all('p')
            content = ' '.join([p.text for p in paragraphs if len(p.text) > 50])
            
            return content[:5000]  # Limit to first 5000 chars to avoid processing too much text
            
        except Exception as e:
            logging.error(f"Error fetching article content from {article_url}: {str(e)}")
            return "" 