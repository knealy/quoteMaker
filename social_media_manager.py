import os
import logging
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tweepy
from instagrapi import Client
from config import (
    TWITTER_API_KEY, TWITTER_API_SECRET, 
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET,
    INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD,
    BACKGROUND_COLORS
)

class SocialMediaManager:
    def __init__(self):
        self.setup_twitter()
        self.setup_instagram()
        
        # Create directory for images if it doesn't exist
        os.makedirs('generated_images', exist_ok=True)
    
    def setup_twitter(self):
        """Set up Twitter API client"""
        self.twitter_client = None
        if all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
            try:
                auth = tweepy.OAuth1UserHandler(
                    TWITTER_API_KEY, TWITTER_API_SECRET,
                    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
                )
                self.twitter_client = tweepy.API(auth)
                logging.info("Twitter client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Twitter client: {str(e)}")
    
    def setup_instagram(self):
        """Set up Instagram API client"""
        self.instagram_client = None
        if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
            try:
                self.instagram_client = Client()
                self.instagram_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                logging.info("Instagram client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Instagram client: {str(e)}")
    
    def create_quote_image(self, quote, background_color=None, width=1080, height=1080):
        """Create an image with the quote text"""
        if not background_color:
            background_color = BACKGROUND_COLORS[0]
        
        # Create image with background color
        img = Image.new('RGB', (width, height), background_color)
        draw = ImageDraw.Draw(img)
        
        # Load font (using default system font, you can specify a path to a custom font)
        try:
            font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Bold.ttf')
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 55)
                small_font = ImageFont.truetype(font_path, 35)
            else:
                # Use default font if custom font not available
                font = ImageFont.load_default()
                font_size = 55
                small_font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Wrap text to fit image width
        quote_text = quote['text']
        wrapped_text = textwrap.fill(quote_text, width=30)
        
        # Calculate text position (centered)
        text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Draw white text with slight shadow for better readability
        shadow_offset = 3
        draw.text((position[0] + shadow_offset, position[1] + shadow_offset), wrapped_text, 
                  font=font, fill=(0, 0, 0, 128))
        draw.text(position, wrapped_text, font=font, fill=(255, 255, 255))
        
        # Draw small source text at the bottom
        source_text = f"Source: {quote['source']}"
        source_bbox = draw.textbbox((0, 0), source_text, font=small_font)
        source_width = source_bbox[2] - source_bbox[0]
        draw.text(((width - source_width) // 2, height - 80), source_text, 
                  font=small_font, fill=(255, 255, 255, 200))
        
        # Save the image
        file_path = os.path.join('generated_images', f"quote_{hash(quote_text)}.jpg")
        img.save(file_path)
        
        return file_path
    
    def post_to_twitter(self, quote, image_path=None):
        """Post a quote to Twitter, with or without an image"""
        if not self.twitter_client:
            raise ValueError("Twitter client not initialized. Check your API credentials.")
        
        try:
            if image_path:
                # Post with image
                media = self.twitter_client.media_upload(image_path)
                self.twitter_client.update_status(status=quote['text'], media_ids=[media.media_id])
            else:
                # Post text only
                self.twitter_client.update_status(quote['text'])
            
            logging.info(f"Successfully posted to Twitter: {quote['text'][:30]}...")
            return True
        except Exception as e:
            logging.error(f"Failed to post to Twitter: {str(e)}")
            return False
    
    def post_to_instagram(self, quote, image_path):
        """Post a quote image to Instagram"""
        if not self.instagram_client:
            raise ValueError("Instagram client not initialized. Check your credentials.")
        
        try:
            caption = f"{quote['text']}\n\n#finance #trading #investing #marketwisdom #stockmarket"
            self.instagram_client.photo_upload(image_path, caption)
            
            logging.info(f"Successfully posted to Instagram: {quote['text'][:30]}...")
            return True
        except Exception as e:
            logging.error(f"Failed to post to Instagram: {str(e)}")
            return False 