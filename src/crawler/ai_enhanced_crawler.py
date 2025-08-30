#!/usr/bin/env python3
"""
AI-Enhanced Alopecosa Fabrilis Web Crawler
Extends the original crawler with GPT integration for intelligent content analysis,
smart URL prioritization, and adaptive crawling strategies.
"""

import os
import json
import time
import hashlib
import re
from typing import Set, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, deque

# Import the original crawler
from .alopecosa_crawler import AlopecosaCrawler, CrawlResult

# For embeddings and similarity (optional - can work without)
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# OpenAI integration
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


@dataclass
class AIAnalysis:
    """AI analysis results for crawled content"""
    relevance_score: float
    quality_score: float
    category: str
    summary: str
    key_topics: List[str]
    sentiment: str
    language: str
    content_type: str
    embedding: Optional[List[float]] = None


@dataclass
class SmartCrawlResult(CrawlResult):
    """Enhanced crawl result with AI analysis"""
    ai_analysis: Optional[AIAnalysis] = None
    priority_score: float = 0.0
    content_hash: str = ""
    is_duplicate: bool = False


class AIEnhancedCrawler(AlopecosaCrawler):
    """
    AI-Enhanced Web Crawler with GPT integration for:
    - Intelligent content analysis and quality assessment
    - Smart URL prioritization based on content relevance
    - Adaptive crawling strategies using machine learning
    - Content summarization and categorization
    - Duplicate detection and content deduplication
    - Semantic search capabilities
    """
    
    def __init__(self, 
                 base_url: str,
                 openai_api_key: str = None,
                 crawl_objective: str = None,
                 target_topics: List[str] = None,
                 use_ai: bool = True,
                 **kwargs):
        
        super().__init__(base_url, **kwargs)
        
        # AI Configuration
        self.use_ai = use_ai and OPENAI_AVAILABLE
        if self.use_ai:
            self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
            if not self.openai_api_key:
                self.logger.warning("OpenAI API key not found. AI features will be disabled.")
                self.use_ai = False
            else:
                self.client = OpenAI(api_key=self.openai_api_key)
        
        # Crawling objectives and targets
        self.crawl_objective = crawl_objective or "General web crawling for information discovery"
        self.target_topics = target_topics or []
        
        # AI-enhanced attributes
        self.content_embeddings = {}
        self.content_hashes = set()
        self.topic_model = None
        self.relevance_threshold = 0.6
        self.quality_threshold = 0.7
        
        # Smart prioritization
        self.url_priorities = defaultdict(float)
        self.topic_keywords = self._extract_topic_keywords() if self.use_ai else {}
        
        # Learning and adaptation
        self.crawl_history = []
        self.success_patterns = defaultdict(list)
        self.failure_patterns = defaultdict(list)
        
        # Performance tracking
        self.ai_analysis_time = 0.0
        self.total_ai_calls = 0
        
        # Text processing for non-AI mode
        self.vectorizer = None
        if not self.use_ai and SKLEARN_AVAILABLE:
            self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        self.logger.info(f"AI-Enhanced Crawler initialized with objective: {self.crawl_objective}")
        if self.target_topics:
            self.logger.info(f"Target topics: {', '.join(self.target_topics)}")
        self.logger.info(f"AI features: {'Enabled' if self.use_ai else 'Disabled (using fallback methods)'}")

    def _extract_topic_keywords(self) -> Dict[str, List[str]]:
        """Extract keywords for each target topic using GPT or fallback methods"""
        if not self.target_topics:
            return {}
        
        keywords = {}
        
        if self.use_ai:
            try:
                for topic in self.target_topics:
                    prompt = f"""
                    Generate 10-15 relevant keywords and phrases for the topic: "{topic}"
                    Return only the keywords, separated by commas, no explanations.
                    Focus on terms that would appear in web content about this topic.
                    """
                    
                    response = self.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=150,
                        temperature=0.3
                    )
                    
                    keyword_text = response.choices[0].message.content.strip()
                    keywords[topic] = [kw.strip() for kw in keyword_text.split(',')]
                    
                    self.logger.info(f"Extracted {len(keywords[topic])} keywords for topic: {topic}")
                    
            except Exception as e:
                self.logger.error(f"Error extracting topic keywords with AI: {e}")
                # Fallback to basic keyword extraction
                keywords = self._extract_keywords_fallback()
        else:
            keywords = self._extract_keywords_fallback()
            
        return keywords

    def _extract_keywords_fallback(self) -> Dict[str, List[str]]:
        """Fallback keyword extraction without AI"""
        keywords = {}
        for topic in self.target_topics:
            # Simple keyword expansion
            base_keywords = topic.lower().split()
            expanded = base_keywords.copy()
            
            # Add common variations
            if 'ai' in topic.lower() or 'artificial intelligence' in topic.lower():
                expanded.extend(['machine learning', 'deep learning', 'neural networks', 'automation'])
            elif 'machine learning' in topic.lower():
                expanded.extend(['ai', 'artificial intelligence', 'data science', 'algorithms'])
            elif 'web' in topic.lower():
                expanded.extend(['internet', 'online', 'digital', 'website', 'webpage'])
            
            keywords[topic] = list(set(expanded))
        
        return keywords

    def _analyze_content_with_ai(self, content: str, title: str, url: str) -> AIAnalysis:
        """Analyze content using GPT for relevance, quality, and categorization"""
        if not self.use_ai:
            return self._analyze_content_fallback(content, title, url)
        
        try:
            # Create analysis prompt
            prompt = f"""
            Analyze the following web content for a web crawler with this objective: "{self.crawl_objective}"
            Target topics: {', '.join(self.target_topics) if self.target_topics else 'General'}
            
            URL: {url}
            Title: {title}
            Content: {content[:2000]}...
            
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
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.2
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                analysis_data = json.loads(analysis_text)
            except json.JSONDecodeError:
                # Fallback parsing if JSON is malformed
                analysis_data = self._parse_analysis_fallback(analysis_text)
            
            # Create embedding for semantic search
            embedding = self._create_content_embedding(content[:1000])
            
            return AIAnalysis(
                relevance_score=float(analysis_data.get('relevance_score', 0.5)),
                quality_score=float(analysis_data.get('quality_score', 0.5)),
                category=analysis_data.get('category', 'unknown'),
                summary=analysis_data.get('summary', '')[:200],
                key_topics=analysis_data.get('key_topics', []),
                sentiment=analysis_data.get('sentiment', 'neutral'),
                language=analysis_data.get('language', 'unknown'),
                content_type=analysis_data.get('content_type', 'other'),
                embedding=embedding
            )
            
        except Exception as e:
            self.logger.error(f"Error in AI content analysis: {e}")
            return self._analyze_content_fallback(content, title, url)

    def _analyze_content_fallback(self, content: str, title: str, url: str) -> AIAnalysis:
        """Fallback content analysis without AI"""
        # Simple heuristics-based analysis
        text = f"{title} {content}".lower()
        
        # Calculate relevance based on target topics
        relevance_score = 0.5
        if self.target_topics:
            topic_matches = sum(1 for topic in self.target_topics if topic.lower() in text)
            relevance_score = min(1.0, 0.5 + (topic_matches * 0.1))
        
        # Calculate quality based on content length and structure
        quality_score = 0.5
        if len(content) > 500:
            quality_score += 0.2
        if len(content) > 1000:
            quality_score += 0.1
        if title and len(title) > 10:
            quality_score += 0.1
        
        # Simple categorization
        category = 'unknown'
        if any(word in text for word in ['article', 'blog', 'post']):
            category = 'blog'
        elif any(word in text for word in ['product', 'buy', 'price']):
            category = 'product'
        elif any(word in text for word in ['news', 'update', 'announcement']):
            category = 'news'
        
        # Simple summary (first 100 chars)
        summary = content[:100] + "..." if len(content) > 100 else content
        
        # Detect language (simple English detection)
        language = 'en' if all(ord(c) < 128 for c in content[:100]) else 'unknown'
        
        return AIAnalysis(
            relevance_score=relevance_score,
            quality_score=quality_score,
            category=category,
            summary=summary,
            key_topics=self.target_topics[:3] if self.target_topics else [],
            sentiment='neutral',
            language=language,
            content_type='other'
        )

    def _parse_analysis_fallback(self, text: str) -> Dict:
        """Fallback parser for malformed JSON responses"""
        analysis = {}
        
        # Extract scores using regex
        relevance_match = re.search(r'"relevance_score":\s*([0-9.]+)', text)
        quality_match = re.search(r'"quality_score":\s*([0-9.]+)', text)
        
        analysis['relevance_score'] = float(relevance_match.group(1)) if relevance_match else 0.5
        analysis['quality_score'] = float(quality_match.group(1)) if quality_match else 0.5
        
        # Extract other fields
        category_match = re.search(r'"category":\s*"([^"]+)"', text)
        analysis['category'] = category_match.group(1) if category_match else 'unknown'
        
        summary_match = re.search(r'"summary":\s*"([^"]+)"', text)
        analysis['summary'] = summary_match.group(1) if summary_match else ''
        
        return analysis

    def _create_content_embedding(self, content: str) -> List[float]:
        """Create embedding for content using OpenAI's embedding API or fallback"""
        if not self.use_ai:
            return []
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=content
            )
            return response.data[0].embedding
        except Exception as e:
            self.logger.error(f"Error creating embedding: {e}")
            return []

    def _calculate_url_priority(self, url: str, link_text: str, context: str) -> float:
        """Calculate priority score for a URL using AI analysis or heuristics"""
        try:
            # Base priority on URL structure and link text
            base_score = 0.5
            
            # Boost for target topic keywords
            for topic, keywords in self.topic_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in link_text.lower() or keyword.lower() in url.lower():
                        base_score += 0.1
            
            # Boost for promising URL patterns
            if any(pattern in url.lower() for pattern in ['article', 'blog', 'news', 'post', 'content']):
                base_score += 0.2
            
            # Penalize for less useful patterns
            if any(pattern in url.lower() for pattern in ['login', 'register', 'cart', 'checkout', 'admin']):
                base_score -= 0.3
            
            # Use GPT for intelligent URL assessment if available
            if self.use_ai and len(link_text) > 10:
                try:
                    prompt = f"""
                    Rate the likelihood (0.0-1.0) that this URL leads to valuable content for: "{self.crawl_objective}"
                    
                    URL: {url}
                    Link text: {link_text}
                    Context: {context[:200]}
                    
                    Consider: relevance to objective, content quality indicators, URL structure.
                    Respond with only a number between 0.0 and 1.0.
                    """
                    
                    response = self.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=10,
                        temperature=0.1
                    )
                    
                    try:
                        ai_score = float(response.choices[0].message.content.strip())
                        base_score = (base_score + ai_score) / 2
                    except (ValueError, AttributeError):
                        pass
                except Exception as e:
                    self.logger.debug(f"AI URL prioritization failed: {e}")
            
            return max(0.0, min(1.0, base_score))
            
        except Exception as e:
            self.logger.error(f"Error calculating URL priority: {e}")
            return 0.5

    def _is_duplicate_content(self, content: str) -> Tuple[bool, str]:
        """Check if content is duplicate using hashing and similarity"""
        # Create content hash
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        if content_hash in self.content_hashes:
            return True, content_hash
        
        # Check semantic similarity if we have embeddings
        if self.content_embeddings and self.use_ai:
            current_embedding = self._create_content_embedding(content[:1000])
            if current_embedding:
                similarities = []
                for url, embedding in self.content_embeddings.items():
                    if embedding:
                        try:
                            similarity = cosine_similarity([current_embedding], [embedding])[0][0]
                            similarities.append((url, similarity))
                        except:
                            continue
                
                # If very similar content exists, mark as duplicate
                max_similarity = max(similarities, key=lambda x: x[1])[1] if similarities else 0
                if max_similarity > 0.9:  # 90% similarity threshold
                    return True, content_hash
        
        # Fallback: simple text similarity using TF-IDF
        if not self.use_ai and SKLEARN_AVAILABLE and self.vectorizer:
            try:
                # This is a simplified approach - in practice you'd want to build the vectorizer properly
                pass
            except:
                pass
        
        self.content_hashes.add(content_hash)
        return False, content_hash

    def _smart_hunt_for_prey(self, soup, current_url: str) -> List[Tuple[str, float]]:
        """Enhanced link discovery with AI-powered prioritization"""
        links_with_priority = []
        link_elements = soup.find_all('a', href=True)
        
        for link in link_elements:
            href = link.get('href')
            absolute_url = urljoin(current_url, href)
            
            if not self._is_allowed_url(absolute_url):
                continue
            
            # Get link context
            link_text = link.get_text(strip=True)
            parent = link.parent
            context = parent.get_text(strip=True) if parent else ""
            
            # Calculate AI-powered priority
            priority = self._calculate_url_priority(absolute_url, link_text, context)
            links_with_priority.append((absolute_url, priority))
            
            # Update URL priorities
            self.url_priorities[absolute_url] = max(self.url_priorities[absolute_url], priority)
        
        # Sort by priority (highest first)
        links_with_priority.sort(key=lambda x: x[1], reverse=True)
        
        return links_with_priority

    def _crawl_page_with_ai(self, url: str, depth: int) -> Optional[SmartCrawlResult]:
        """Enhanced page crawling with AI analysis"""
        if url in self.visited_urls:
            return None
        
        # Get basic crawl result from parent class
        basic_result = super()._crawl_page(url, depth)
        if not basic_result:
            return None
        
        # Perform AI analysis
        start_ai_time = time.time()
        
        ai_analysis = self._analyze_content_with_ai(
            basic_result.content, 
            basic_result.title, 
            url
        )
        
        # Check for duplicates
        is_duplicate, content_hash = self._is_duplicate_content(basic_result.content)
        
        # Store embedding for future similarity checks
        if ai_analysis.embedding:
            self.content_embeddings[url] = ai_analysis.embedding
        
        # Calculate priority score
        priority_score = (ai_analysis.relevance_score + ai_analysis.quality_score) / 2
        
        # Track AI processing time
        self.ai_analysis_time += time.time() - start_ai_time
        self.total_ai_calls += 1
        
        # Create enhanced result
        smart_result = SmartCrawlResult(
            url=basic_result.url,
            title=basic_result.title,
            content=basic_result.content,
            links=basic_result.links,
            status_code=basic_result.status_code,
            crawl_time=basic_result.crawl_time,
            timestamp=basic_result.timestamp,
            metadata=basic_result.metadata,
            ai_analysis=ai_analysis,
            priority_score=priority_score,
            content_hash=content_hash,
            is_duplicate=is_duplicate
        )
        
        # Log AI insights
        self.logger.info(f"AI Analysis for {url}: "
                        f"Relevance={ai_analysis.relevance_score:.2f}, "
                        f"Quality={ai_analysis.quality_score:.2f}, "
                        f"Category={ai_analysis.category}")
        
        if is_duplicate:
            self.logger.info(f"Duplicate content detected: {url}")
        
        return smart_result

    def smart_crawl(self) -> List[SmartCrawlResult]:
        """Main AI-enhanced crawling method"""
        self.logger.info(f"Starting AI-Enhanced Crawler on {self.base_url}")
        self.logger.info(f"Crawl Objective: {self.crawl_objective}")
        
        pages_crawled = 0
        high_quality_pages = 0
        
        while self.url_queue and pages_crawled < self.max_pages:
            current_url, depth = self.url_queue.popleft()
            
            if depth > self.max_depth:
                continue
            
            result = self._crawl_page_with_ai(current_url, depth)
            if result:
                pages_crawled += 1
                
                # Track high-quality pages
                if result.ai_analysis and result.ai_analysis.quality_score > self.quality_threshold:
                    high_quality_pages += 1
                
                # Smart link discovery and prioritization
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(result.content, 'html.parser')  # Re-parse for link analysis
                prioritized_links = self._smart_hunt_for_prey(soup, current_url)
                
                # Add high-priority URLs to front of queue
                for link_url, priority in prioritized_links[:5]:  # Top 5 priority links
                    if link_url not in self.visited_urls:
                        if priority > 0.7:  # High priority
                            self.url_queue.appendleft((link_url, depth + 1))
                        elif priority > 0.5:  # Medium priority
                            self.url_queue.append((link_url, depth + 1))
                        # Low priority links are ignored
                
                # Adaptive behavior based on AI analysis
                if pages_crawled % 10 == 0:
                    self._adapt_ai_strategy()
                
                # Filter out low-quality results if needed
                if (result.ai_analysis and 
                    result.ai_analysis.relevance_score > self.relevance_threshold and
                    not result.is_duplicate):
                    self.results.append(result)
        
        self.logger.info(f"AI-Enhanced crawling completed!")
        self.logger.info(f"Pages crawled: {pages_crawled}")
        self.logger.info(f"High-quality pages: {high_quality_pages}")
        if self.use_ai:
            self.logger.info(f"Total AI analysis time: {self.ai_analysis_time:.2f}s")
            self.logger.info(f"Average AI time per page: {self.ai_analysis_time/max(1, self.total_ai_calls):.2f}s")
        
        return self.results

    def _adapt_ai_strategy(self):
        """Adapt crawling strategy based on AI analysis results"""
        if not self.results:
            return
        
        # Calculate average quality and relevance
        recent_results = self.results[-10:]  # Last 10 results
        avg_quality = sum(r.ai_analysis.quality_score for r in recent_results if r.ai_analysis) / len(recent_results)
        avg_relevance = sum(r.ai_analysis.relevance_score for r in recent_results if r.ai_analysis) / len(recent_results)
        
        # Adjust thresholds based on performance
        if avg_quality < 0.5:
            self.quality_threshold = max(0.5, self.quality_threshold - 0.1)
            self.logger.info(f"Lowering quality threshold to {self.quality_threshold}")
        elif avg_quality > 0.8:
            self.quality_threshold = min(0.9, self.quality_threshold + 0.05)
            self.logger.info(f"Raising quality threshold to {self.quality_threshold}")
        
        if avg_relevance < 0.5:
            self.relevance_threshold = max(0.4, self.relevance_threshold - 0.1)
            self.logger.info(f"Lowering relevance threshold to {self.relevance_threshold}")

    def semantic_search(self, query: str, top_k: int = 10) -> List[Tuple[SmartCrawlResult, float]]:
        """Perform semantic search on crawled content"""
        if not self.results or not query:
            return []
        
        try:
            if self.use_ai:
                # Use OpenAI embeddings for semantic search
                query_embedding = self._create_content_embedding(query)
                if not query_embedding:
                    return []
                
                # Calculate similarities
                similarities = []
                for result in self.results:
                    if (result.ai_analysis and result.ai_analysis.embedding and 
                        not result.is_duplicate):
                        
                        try:
                            similarity = cosine_similarity(
                                [query_embedding], 
                                [result.ai_analysis.embedding]
                            )[0][0]
                            similarities.append((result, similarity))
                        except:
                            continue
                
                # Sort by similarity and return top results
                similarities.sort(key=lambda x: x[1], reverse=True)
                return similarities[:top_k]
            else:
                # Fallback to keyword-based search
                return self._keyword_search_fallback(query, top_k)
            
        except Exception as e:
            self.logger.error(f"Error in semantic search: {e}")
            return []

    def _keyword_search_fallback(self, query: str, top_k: int) -> List[Tuple[SmartCrawlResult, float]]:
        """Fallback keyword-based search without AI"""
        query_words = query.lower().split()
        results = []
        
        for result in self.results:
            if result.is_duplicate:
                continue
                
            text = f"{result.title} {result.content}".lower()
            matches = sum(1 for word in query_words if word in text)
            relevance = matches / len(query_words) if query_words else 0
            
            if relevance > 0:
                results.append((result, relevance))
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def get_content_categories(self) -> Dict[str, int]:
        """Get distribution of content categories"""
        categories = defaultdict(int)
        for result in self.results:
            if result.ai_analysis and not result.is_duplicate:
                categories[result.ai_analysis.category] += 1
        return dict(categories)

    def get_ai_insights(self) -> Dict:
        """Get comprehensive AI insights about the crawl"""
        if not self.results:
            return {}
        
        valid_results = [r for r in self.results if r.ai_analysis and not r.is_duplicate]
        
        if not valid_results:
            return {}
        
        insights = {
            'total_pages_analyzed': len(valid_results),
            'average_relevance_score': sum(r.ai_analysis.relevance_score for r in valid_results) / len(valid_results),
            'average_quality_score': sum(r.ai_analysis.quality_score for r in valid_results) / len(valid_results),
            'content_categories': self.get_content_categories(),
            'language_distribution': defaultdict(int),
            'sentiment_distribution': defaultdict(int),
            'content_type_distribution': defaultdict(int),
            'high_quality_pages': len([r for r in valid_results if r.ai_analysis.quality_score > 0.8]),
            'highly_relevant_pages': len([r for r in valid_results if r.ai_analysis.relevance_score > 0.8]),
            'duplicates_detected': len([r for r in self.results if r.is_duplicate]),
            'ai_processing_time': self.ai_analysis_time,
            'ai_calls_made': self.total_ai_calls
        }
        
        # Calculate distributions
        for result in valid_results:
            insights['language_distribution'][result.ai_analysis.language] += 1
            insights['sentiment_distribution'][result.ai_analysis.sentiment] += 1
            insights['content_type_distribution'][result.ai_analysis.content_type] += 1
        
        return insights

    def export_enhanced_results(self, filename: str = None):
        """Export results with AI analysis"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_enhanced_crawl_results_{timestamp}.json"
        
        # Prepare data for export
        export_data = {
            'crawl_info': {
                'base_url': self.base_url,
                'crawl_objective': self.crawl_objective,
                'target_topics': self.target_topics,
                'crawl_timestamp': datetime.now().isoformat(),
                'total_pages': len(self.results),
                'ai_insights': self.get_ai_insights()
            },
            'results': []
        }
        
        for result in self.results:
            result_data = {
                'url': result.url,
                'title': result.title,
                'content': result.content,
                'status_code': result.status_code,
                'timestamp': result.timestamp.isoformat(),
                'priority_score': result.priority_score,
                'is_duplicate': result.is_duplicate,
                'content_hash': result.content_hash
            }
            
            if result.ai_analysis:
                result_data['ai_analysis'] = {
                    'relevance_score': result.ai_analysis.relevance_score,
                    'quality_score': result.ai_analysis.quality_score,
                    'category': result.ai_analysis.category,
                    'summary': result.ai_analysis.summary,
                    'key_topics': result.ai_analysis.key_topics,
                    'sentiment': result.ai_analysis.sentiment,
                    'language': result.ai_analysis.language,
                    'content_type': result.ai_analysis.content_type
                }
            
            export_data['results'].append(result_data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Enhanced results exported to {filename}")


def main():
    """Demo function for AI-Enhanced Crawler"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI-Enhanced Alopecosa Fabrilis Web Crawler')
    parser.add_argument('url', help='Starting URL to crawl')
    parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
    parser.add_argument('--objective', help='Crawling objective')
    parser.add_argument('--topics', nargs='+', help='Target topics')
    parser.add_argument('--depth', type=int, default=2, help='Maximum crawl depth')
    parser.add_argument('--pages', type=int, default=25, help='Maximum pages to crawl')
    parser.add_argument('--output', help='Output filename')
    parser.add_argument('--search', help='Perform semantic search after crawling')
    parser.add_argument('--no-ai', action='store_true', help='Disable AI features')
    
    args = parser.parse_args()
    
    try:
        crawler = AIEnhancedCrawler(
            base_url=args.url,
            openai_api_key=args.api_key,
            crawl_objective=args.objective or "General web content discovery",
            target_topics=args.topics,
            use_ai=not args.no_ai,
            max_depth=args.depth,
            max_pages=args.pages
        )
        
        print("🕷️ Starting AI-Enhanced Web Crawling...")
        results = crawler.smart_crawl()
        
        print(f"\n✅ Crawling completed! Analyzed {len(results)} pages.")
        
        # Show AI insights
        insights = crawler.get_ai_insights()
        print("\n🧠 AI Insights:")
        for key, value in insights.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {key}: {value}")
        
        # Export results
        crawler.export_enhanced_results(args.output)
        
        # Semantic search demo
        if args.search:
            print(f"\n🔍 Semantic search for: '{args.search}'")
            search_results = crawler.semantic_search(args.search, top_k=5)
            for i, (result, similarity) in enumerate(search_results, 1):
                print(f"{i}. [{similarity:.3f}] {result.title}")
                print(f"   {result.url}")
                if result.ai_analysis:
                    print(f"   Summary: {result.ai_analysis.summary}")
                print()
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
