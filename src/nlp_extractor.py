import re
import spacy
from typing import Dict, List, Any
import logging
from transformers import pipeline
import torch

class NLPExtractor:
    """Extract key information from unstructured documents using NLP techniques"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize spaCy model (download with: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Initialize sentiment analysis pipeline
        try:
            self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                             model="distilbert-base-uncased-finetuned-sst-2-english")
        except Exception as e:
            self.logger.warning(f"Could not initialize sentiment analyzer: {e}")
            self.sentiment_analyzer = None
    
    def extract_key_information(self, text: str) -> Dict[str, Any]:
        """Extract key information from unstructured text"""
        if not text.strip():
            return {"error": "Empty text provided"}
        
        results = {
            "financial_metrics": self._extract_financial_metrics(text),
            "entities": self._extract_entities(text),
            "sentiment": self._analyze_sentiment(text),
            "key_phrases": self._extract_key_phrases(text),
            "risks": self._identify_risks(text),
            "opportunities": self._identify_opportunities(text),
            "management_insights": self._extract_management_insights(text)
        }
        
        return results
    
    def _extract_financial_metrics(self, text: str) -> Dict[str, List[str]]:
        """Extract financial metrics and numbers from text"""
        financial_metrics = {
            "revenue": [],
            "profit": [],
            "growth": [],
            "margins": [],
            "debt": [],
            "cash": []
        }
        
        # Patterns for different financial metrics
        patterns = {
            "revenue": [
                r"revenue[s]?\s*(?:of\s*)?(?:is\s*)?(?:was\s*)?(?:\$?[\d,]+(?:\.\d+)?[kmb]?)",
                r"sales[s]?\s*(?:of\s*)?(?:is\s*)?(?:was\s*)?(?:\$?[\d,]+(?:\.\d+)?[kmb]?)",
                r"turnover[s]?\s*(?:of\s*)?(?:is\s*)?(?:was\s*)?(?:\$?[\d,]+(?:\.\d+)?[kmb]?)"
            ],
            "profit": [
                r"profit[s]?\s*(?:of\s*)?(?:is\s*)?(?:was\s*)?(?:\$?[\d,]+(?:\.\d+)?[kmb]?)",
                r"net\s*income\s*(?:of\s*)?(?:is\s*)?(?:was\s*)?(?:\$?[\d,]+(?:\.\d+)?[kmb]?)",
                r"ebitda\s*(?:of\s*)?(?:is\s*)?(?:was\s*)?(?:\$?[\d,]+(?:\.\d+)?[kmb]?)"
            ],
            "growth": [
                r"growth\s*(?:rate\s*)?(?:of\s*)?(?:is\s*)?(?:was\s*)?(?:[\d,]+(?:\.\d+)?%)",
                r"increased?\s*(?:by\s*)?(?:[\d,]+(?:\.\d+)?%)",
                r"decreased?\s*(?:by\s*)?(?:[\d,]+(?:\.\d+)?%)"
            ]
        }
        
        for metric_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.findall(pattern, text.lower())
                financial_metrics[metric_type].extend(matches)
        
        # Remove duplicates and clean up
        for key in financial_metrics:
            financial_metrics[key] = list(set(financial_metrics[key]))
        
        return financial_metrics
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using spaCy"""
        if not self.nlp:
            return {"error": "spaCy model not available"}
        
        doc = self.nlp(text)
        entities = {
            "organizations": [],
            "persons": [],
            "locations": [],
            "dates": [],
            "money": [],
            "percent": []
        }
        
        for ent in doc.ents:
            if ent.label_ == "ORG":
                entities["organizations"].append(ent.text)
            elif ent.label_ == "PERSON":
                entities["persons"].append(ent.text)
            elif ent.label_ == "GPE" or ent.label_ == "LOC":
                entities["locations"].append(ent.text)
            elif ent.label_ == "DATE":
                entities["dates"].append(ent.text)
            elif ent.label_ == "MONEY":
                entities["money"].append(ent.text)
            elif ent.label_ == "PERCENT":
                entities["percent"].append(ent.text)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of the text"""
        if not self.sentiment_analyzer:
            return {"error": "Sentiment analyzer not available"}
        
        # Split text into chunks if too long
        max_length = 512
        chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        
        sentiments = []
        for chunk in chunks:
            if chunk.strip():
                try:
                    result = self.sentiment_analyzer(chunk[:512])  # Truncate to max length
                    sentiments.append(result[0])
                except Exception as e:
                    self.logger.warning(f"Sentiment analysis failed for chunk: {e}")
        
        if not sentiments:
            return {"error": "Could not analyze sentiment"}
        
        # Aggregate sentiment results
        positive_score = sum(1 for s in sentiments if s['label'] == 'POSITIVE')
        total_score = len(sentiments)
        
        return {
            "overall_sentiment": "positive" if positive_score > total_score / 2 else "negative",
            "confidence": max(s['score'] for s in sentiments),
            "detailed_sentiments": sentiments
        }
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from the text"""
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        key_phrases = []
        
        # Extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) >= 2 and len(chunk.text.split()) <= 5:
                key_phrases.append(chunk.text)
        
        # Extract important phrases based on POS tags
        important_phrases = []
        for token in doc:
            if token.pos_ in ['NOUN', 'ADJ'] and not token.is_stop:
                # Get surrounding context
                start = max(0, token.i - 1)
                end = min(len(doc), token.i + 3)
                phrase = doc[start:end].text
                if len(phrase.split()) >= 2:
                    important_phrases.append(phrase)
        
        key_phrases.extend(important_phrases)
        
        # Remove duplicates and return top phrases
        unique_phrases = list(set(key_phrases))
        return unique_phrases[:20]  # Return top 20 phrases
    
    def _identify_risks(self, text: str) -> List[str]:
        """Identify potential risks mentioned in the text"""
        risk_keywords = [
            "risk", "risky", "concern", "issue", "problem", "challenge", "difficulty",
            "uncertainty", "volatility", "decline", "decrease", "loss", "debt",
            "competition", "market risk", "operational risk", "financial risk",
            "regulatory", "compliance", "legal", "litigation", "lawsuit"
        ]
        
        risks = []
        text_lower = text.lower()
        
        for keyword in risk_keywords:
            if keyword in text_lower:
                # Find sentences containing the risk keyword
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        risks.append(sentence.strip())
        
        return list(set(risks))[:10]  # Return top 10 risk mentions
    
    def _identify_opportunities(self, text: str) -> List[str]:
        """Identify potential opportunities mentioned in the text"""
        opportunity_keywords = [
            "opportunity", "potential", "growth", "expansion", "increase",
            "improvement", "advantage", "benefit", "upside", "positive",
            "strong", "robust", "healthy", "profitable", "successful"
        ]
        
        opportunities = []
        text_lower = text.lower()
        
        for keyword in opportunity_keywords:
            if keyword in text_lower:
                # Find sentences containing the opportunity keyword
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        opportunities.append(sentence.strip())
        
        return list(set(opportunities))[:10]  # Return top 10 opportunity mentions
    
    def _extract_management_insights(self, text: str) -> Dict[str, List[str]]:
        """Extract management-related insights"""
        insights = {
            "leadership": [],
            "strategy": [],
            "operations": [],
            "financial_performance": []
        }
        
        # Leadership keywords
        leadership_patterns = [
            r"ceo|chief executive|cfo|chief financial|cto|chief technology",
            r"management team|leadership|executive|director|president"
        ]
        
        # Strategy keywords
        strategy_patterns = [
            r"strategy|strategic|plan|roadmap|vision|mission",
            r"acquisition|merger|partnership|alliance"
        ]
        
        # Operations keywords
        operations_patterns = [
            r"operational|operations|process|efficiency|productivity",
            r"supply chain|manufacturing|distribution|logistics"
        ]
        
        text_lower = text.lower()
        
        # Extract insights based on patterns
        for pattern in leadership_patterns:
            matches = re.findall(pattern, text_lower)
            insights["leadership"].extend(matches)
        
        for pattern in strategy_patterns:
            matches = re.findall(pattern, text_lower)
            insights["strategy"].extend(matches)
        
        for pattern in operations_patterns:
            matches = re.findall(pattern, text_lower)
            insights["operations"].extend(matches)
        
        # Remove duplicates
        for key in insights:
            insights[key] = list(set(insights[key]))
        
        return insights
