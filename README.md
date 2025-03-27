# Financial Quote Generator

A Python-based tool that generates insightful financial quotes using OpenAI's GPT model. This tool processes financial news articles and creates quotable statements that sound like they're from market experts and financial thought leaders.

## Features

- Generates concise, impactful financial quotes from news articles
- Uses OpenAI's GPT-3.5-turbo model for natural language generation
- Processes up to 10 articles at a time
- Caches generated quotes for reuse
- Includes source attribution for each quote

## Prerequisites

- Python 3.x
- OpenAI API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd quoteMaker
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `config.py` file in the project root and add your OpenAI API key:
```python
OPENAI_API_KEY = "your-api-key-here"
```

## Usage

```python
from quote_generator import QuoteGenerator

# Initialize the quote generator
generator = QuoteGenerator()

# Example articles list
articles = [
    {
        'title': 'Market Analysis: Tech Stocks Surge Amid AI Boom',
        'source': 'Financial Times'
    },
    # ... more articles
]

# Generate quotes
quotes = generator.generate_quotes_from_articles(articles, num_quotes=10)

# Access the generated quotes
for quote in quotes:
    print(f"Quote: {quote['text']}")
    print(f"Source: {quote['source']}")
    print(f"Based on: {quote['article_title']}")
    print("---")
```

## Configuration

The quote generator can be configured with the following parameters:

- `num_quotes`: Number of quotes to generate (default: 10)
- `max_articles`: Maximum number of articles to process (default: 10)

## Error Handling

The generator includes error handling for:
- Empty article lists
- API request failures
- Invalid responses

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your chosen license]

## Acknowledgments

- OpenAI for providing the GPT model
- Financial news sources for the input articles 