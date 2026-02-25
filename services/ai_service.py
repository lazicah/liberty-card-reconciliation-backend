"""
AI service for generating summaries using OpenAI.
"""
import json
import openai
from typing import Dict
from config import settings


class AIService:
    """Service for generating AI summaries."""
    
    def __init__(self):
        """Initialize AI service."""
        openai.api_key = settings.openai_api_key
        self.model = settings.ai_model
    
    def generate_summary(self, metrics: Dict) -> str:
        """
        Generate AI summary from metrics.
        
        Args:
            metrics: Dictionary containing reconciliation metrics
            
        Returns:
            AI-generated summary string
        """
        if not settings.openai_api_key:
            return "OpenAI API key not configured. AI summary skipped."
        
        metrics_json = json.dumps(metrics, indent=2)
        
        prompt = f"""
You are a financial operations analyst.
Analyze the metrics below and summarize performance, risks, and concerns.

Metrics:
{metrics_json}
"""
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI summary could not be generated: {str(e)}"
