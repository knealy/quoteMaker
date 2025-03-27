import streamlit as st
import logging
from datetime import datetime
import os
import json

# Import our modules
from news_scraper import NewsScraper
from quote_generator import QuoteGenerator
from social_media_manager import SocialMediaManager
from config import BACKGROUND_COLORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Initialize our components
scraper = NewsScraper()
quote_gen = QuoteGenerator()
social_media = SocialMediaManager()

# Setup cache directory
os.makedirs('cache', exist_ok=True)
CACHE_FILE = 'cache/quotes_cache.json'

def save_quotes_to_cache(quotes):
    """Save generated quotes to a cache file"""
    with open(CACHE_FILE, 'w') as f:
        json.dump({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'quotes': quotes
        }, f)

def load_quotes_from_cache():
    """Load quotes from cache if available and recent"""
    if not os.path.exists(CACHE_FILE):
        return None
    
    try:
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
            
        # Check if quotes are from today
        if data['date'] == datetime.now().strftime('%Y-%m-%d'):
            return data['quotes']
    except Exception as e:
        logging.error(f"Error loading quotes from cache: {str(e)}")
    
    return None

def main():
    st.set_page_config(
        page_title="Finance Quote Generator",
        page_icon="💰",
        layout="wide"
    )
    
    st.title("Finance Quote Generator & Social Media Automation")
    st.markdown("Generate impactful quotes from the latest financial news and post them to social media.")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        if st.button("Refresh Financial News & Generate Quotes"):
            with st.spinner("Fetching latest financial news..."):
                articles = scraper.fetch_news(max_articles=15)
                st.session_state.articles = articles
                
            with st.spinner("Generating quotes from news..."):
                quotes = quote_gen.generate_quotes_from_articles(articles, num_quotes=10)
                st.session_state.quotes = quotes
                save_quotes_to_cache(quotes)
                st.success(f"Generated {len(quotes)} quotes from {len(articles)} articles!")
        
        st.markdown("---")
        
        # Background color picker
        st.subheader("Image Background")
        selected_color = st.color_picker("Pick a color for quote background", BACKGROUND_COLORS[0])
        st.session_state.selected_color = selected_color
    
    # Main content area
    if 'quotes' not in st.session_state:
        # Try to load from cache first
        cached_quotes = load_quotes_from_cache()
        if cached_quotes:
            st.session_state.quotes = cached_quotes
            st.info("Loaded today's quotes from cache. Click 'Refresh' to get new quotes.")
        else:
            st.session_state.quotes = []
            st.info("Click 'Refresh Financial News & Generate Quotes' to get started.")
    
    if 'articles' not in st.session_state:
        st.session_state.articles = []
    
    if 'selected_color' not in st.session_state:
        st.session_state.selected_color = BACKGROUND_COLORS[0]
    
    # Display quotes if available
    if st.session_state.quotes:
        st.header("Select a Quote to Post")
        
        for i, quote in enumerate(st.session_state.quotes):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### Quote {i+1}")
                st.markdown(f"> {quote['text']}")
                st.caption(f"Source: {quote['source']}")
            
            with col2:
                # Preview and post buttons
                if st.button(f"Preview Quote {i+1}", key=f"preview_{i}"):
                    image_path = social_media.create_quote_image(
                        quote, background_color=st.session_state.selected_color)
                    st.session_state.preview_image = image_path
                    st.session_state.preview_quote = quote
                
                st.markdown("---")
                
                # Social media posting buttons
                if st.button(f"Post to Twitter", key=f"twitter_{i}"):
                    image_path = social_media.create_quote_image(
                        quote, background_color=st.session_state.selected_color)
                    success = social_media.post_to_twitter(quote, image_path)
                    if success:
                        st.success("Posted to Twitter!")
                    else:
                        st.error("Failed to post to Twitter. Check logs.")
                
                if st.button(f"Post to Instagram", key=f"insta_{i}"):
                    image_path = social_media.create_quote_image(
                        quote, background_color=st.session_state.selected_color)
                    success = social_media.post_to_instagram(quote, image_path)
                    if success:
                        st.success("Posted to Instagram!")
                    else:
                        st.error("Failed to post to Instagram. Check logs.")
            
            st.markdown("---")
        
        # Display preview if available
        if 'preview_image' in st.session_state:
            st.header("Quote Preview")
            st.image(st.session_state.preview_image)
            
            # Add "Post This" buttons for the preview
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Post Preview to Twitter"):
                    success = social_media.post_to_twitter(
                        st.session_state.preview_quote, st.session_state.preview_image)
                    if success:
                        st.success("Posted to Twitter!")
                    else:
                        st.error("Failed to post to Twitter. Check logs.")
            
            with col2:
                if st.button("Post Preview to Instagram"):
                    success = social_media.post_to_instagram(
                        st.session_state.preview_quote, st.session_state.preview_image)
                    if success:
                        st.success("Posted to Instagram!")
                    else:
                        st.error("Failed to post to Instagram. Check logs.")
    
    # Display fetched articles at the bottom
    if st.session_state.articles:
        with st.expander("View Fetched Articles"):
            for i, article in enumerate(st.session_state.articles):
                st.markdown(f"#### {i+1}. {article['title']}")
                st.markdown(f"Source: {article['source']} - [Read Article]({article['url']})")
                st.markdown("---")

if __name__ == "__main__":
    main() 