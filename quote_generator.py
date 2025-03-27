import openai
import random
import logging
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class QuoteGenerator:
    def __init__(self):
        self.quotes_cache = []
    
    def generate_quotes_from_articles(self, articles, num_quotes=10):
        """Generate quotes from a list of articles"""
        if not articles:
            raise ValueError("No articles provided to generate quotes from")
        
        all_quotes = []
        
        # Process each article to generate quotes
        for article in articles[:min(10, len(articles))]:  # Limit to 10 articles for processing
            title = article['title']
            source = article['source']
            
            # Generate quotes based on article title (faster than processing full content)
            prompt = f"""
            As a financial expert, create 2 insightful and quotable statements based on this financial news headline:
            "{title}" (from {source})
            
            Make the quotes sound like they're from a market sage or financial thought leader.
            Each quote should be concise (under 150 characters), impactful, and include a key insight relevant to traders or investors.
            Don't use quotation marks in your response.
            """
            
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a financial expert who creates powerful, quotable insights."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                
                generated_text = response.choices[0].message.content.strip()
                
                # Split the text into individual quotes
                quote_lines = [q.strip() for q in generated_text.split('\n') if q.strip()]
                
                for quote in quote_lines:
                    if quote and len(quote) > 20:  # Skip too short quotes
                        all_quotes.append({
                            'text': quote,
                            'source': f"Based on {source} headline",
                            'article_title': title
                        })
                
            except Exception as e:
                logging.error(f"Error generating quotes for article '{title}': {str(e)}")
        
        # Shuffle and select the best quotes
        random.shuffle(all_quotes)
        selected_quotes = all_quotes[:num_quotes]
        
        self.quotes_cache = selected_quotes
        return selected_quotes 