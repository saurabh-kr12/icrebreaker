
"""Configuration settings for the Icebreaker Bot."""
import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API settings (Free Tier)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL_ID = "gemini-3.5-flash-lite"
EMBEDDING_MODEL_ID = "gemini-embedding-001"

# EnrichLayer API settings
# ENRICHLAYER_API_KEY is the primary name. PROXYCURL_API_KEY is retained
# for backward compatibility with existing .env files.
ENRICHLAYER_API_KEY = os.getenv(
    "ENRICHLAYER_API_KEY",
    os.getenv("PROXYCURL_API_KEY", ""),
)

# Mock data URL
MOCK_DATA_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/ZRe59Y_NJyn3hZgnF1iFYA/linkedin-profile-data.json"

# Query settings
SIMILARITY_TOP_K = 5
TEMPERATURE = 0.0
MAX_NEW_TOKENS = 500
MIN_NEW_TOKENS = 1
TOP_K = 50
TOP_P = 1

# Node settings
CHUNK_SIZE = 500

# LLM prompt templates
INITIAL_FACTS_TEMPLATE = """
You are an AI assistant that provides detailed answers based on the provided context.

Context information is below:

{context_str}

Based on the context provided, list 3 interesting facts about this person's career or education.

Answer in detail, using only the information provided in the context.
"""

USER_QUESTION_TEMPLATE = """
You are an AI assistant that provides detailed answers to questions based on the provided context.

Context information is below:
{context_str}

Question: {query_str}

Conversation context:
{conversation_history}

Question mode: {question_mode}
Answer in detail using only the supplied profile context. Be explicit about comparisons,
confidence, career gaps, leadership signals, and evidence. Do not infer facts that are
not supported by the context.

End with "Evidence:" followed by short source labels corresponding to the retrieved chunks.
If the answer is unavailable, say "I don't know. The information is not available on the LinkedIn profile."
"""
