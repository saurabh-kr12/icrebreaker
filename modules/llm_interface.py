"""Module for interfacing with IBM watsonx.ai LLMs."""

import logging
from typing import Dict, Any, Optional

from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import config

logger = logging.getLogger(__name__)

def create_watsonx_llm(
    temperature: float = 0.7,
    max_new_tokens: int = 512,
    **kwargs,
):
    """Initialize and return the Google Gemini LLM instance."""
    try:
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set.")
        llm = GoogleGenAI(
            model=config.LLM_MODEL_ID,
            api_key=config.GEMINI_API_KEY,
            temperature=temperature,
            max_tokens=max_new_tokens,
        )
        logger.info(f"Initialized Gemini LLM: {config.LLM_MODEL_ID}")
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize Gemini LLM: {e}")
        raise


def create_watsonx_embedding():
    """Initialize and return the Google Gemini Embedding model."""
    try:
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set.")
        embed_model = GoogleGenAIEmbedding(
            model_name=config.EMBEDDING_MODEL_ID,
            api_key=config.GEMINI_API_KEY,
        )
        logger.info(f"Initialized Gemini Embedding model: {config.EMBEDDING_MODEL_ID}")
        return embed_model
    except Exception as e:
        logger.error(f"Failed to initialize Gemini Embedding model: {e}")
        raise

def change_llm_model(new_model_id: str) -> None:
    """Change the LLM model to use.
    
    Args:
        new_model_id: New LLM model ID to use.
    """
    global config
    config.LLM_MODEL_ID = new_model_id
    logger.info(f"Changed LLM model to: {new_model_id}")
