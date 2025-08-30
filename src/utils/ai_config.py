"""
AI Configuration and utilities for the enhanced crawler
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class AIConfig:
    """Configuration for AI-enhanced crawling"""
    openai_api_key: str
    model: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-ada-002"
    max_tokens: int = 400
    temperature: float = 0.2
    
    # Quality thresholds
    relevance_threshold: float = 0.6
    quality_threshold: float = 0.7
    similarity_threshold: float = 0.9
    
    # Rate limiting
    requests_per_minute: int = 60
    max_concurrent_requests: int = 5


class AIPromptTemplates:
    """Templates for AI prompts used in crawling"""
    
    CONTENT_ANALYSIS = """
    Analyze the following web content for a web crawler with this objective: "{objective}"
    Target topics: {topics}
    
    URL: {url}
    Title: {title}
    Content: {content}
    
    Provide analysis in JSON format:
    {{
        "relevance_score": 0.0-1.0 (how relevant to crawl objective),
        "quality_score": 0.0-1.0 (content quality and usefulness),
        "category": "category name",
        "summary": "brief summary (max 200 chars)",
        "key_topics": ["topic1", "topic2", "topic3"],
        "sentiment": "positive/negative/neutral",
        "language": "language code",
        "content_type": "article/product/news/blog/technical/other"
    }}
    """
    
    URL_PRIORITIZATION = """
    Rate the likelihood (0.0-1.0) that this URL leads to valuable content for: "{objective}"
    
    URL: {url}
    Link text: {link_text}
    Context: {context}
    
    Consider: relevance to objective, content quality indicators, URL structure.
    Respond with only a number between 0.0 and 1.0.
    """
    
    KEYWORD_EXTRACTION = """
    Generate 10-15 relevant keywords and phrases for the topic: "{topic}"
    Return only the keywords, separated by commas, no explanations.
    Focus on terms that would appear in web content about this topic.
    """
    
    CONTENT_SUMMARIZATION = """
    Summarize the following content in exactly one sentence (max 200 characters):
    
    Title: {title}
    Content: {content}
    
    Focus on the main point and key information.
    """


def load_ai_config() -> AIConfig:
    """Load AI configuration from environment variables or defaults"""
    return AIConfig(
        openai_api_key=os.getenv('OPENAI_API_KEY', ''),
        model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        embedding_model=os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-ada-002'),
        max_tokens=int(os.getenv('OPENAI_MAX_TOKENS', '400')),
        temperature=float(os.getenv('OPENAI_TEMPERATURE', '0.2')),
        relevance_threshold=float(os.getenv('AI_RELEVANCE_THRESHOLD', '0.6')),
        quality_threshold=float(os.getenv('AI_QUALITY_THRESHOLD', '0.7')),
        similarity_threshold=float(os.getenv('AI_SIMILARITY_THRESHOLD', '0.9')),
        requests_per_minute=int(os.getenv('OPENAI_RPM_LIMIT', '60')),
        max_concurrent_requests=int(os.getenv('OPENAI_CONCURRENT_LIMIT', '5'))
    )


def validate_ai_config(config: AIConfig) -> List[str]:
    """Validate AI configuration and return list of issues"""
    issues = []
    
    if not config.openai_api_key:
        issues.append("OpenAI API key is required")
    
    if config.relevance_threshold < 0 or config.relevance_threshold > 1:
        issues.append("Relevance threshold must be between 0 and 1")
    
    if config.quality_threshold < 0 or config.quality_threshold > 1:
        issues.append("Quality threshold must be between 0 and 1")
    
    if config.max_tokens < 50 or config.max_tokens > 4000:
        issues.append("Max tokens should be between 50 and 4000")
    
    return issues


def get_ai_cost_estimate(tokens_used: int, model: str = "gpt-3.5-turbo") -> float:
    """Estimate cost of AI API usage (approximate)"""
    # Rough cost estimates per 1K tokens (as of 2024)
    costs = {
        "gpt-3.5-turbo": 0.002,  # $0.002 per 1K tokens
        "gpt-4": 0.03,           # $0.03 per 1K tokens
        "text-embedding-ada-002": 0.0001  # $0.0001 per 1K tokens
    }
    
    cost_per_1k = costs.get(model, 0.002)
    return (tokens_used / 1000) * cost_per_1k


def create_ai_prompt(template: str, **kwargs) -> str:
    """Create AI prompt from template with variables"""
    return template.format(**kwargs)
