from llama_index.llms.groq import Groq
from llama_index.llms.gemini import Gemini
from config.settings import get_settings

settings = get_settings
_llm_cache = {}

def get_groq_llm(model_name: str):
    """Initialize and cache Groq LLM"""
    key = f"groq:{model_name}"
    if key in _llm_cache:
        return _llm_cache[key]

    if not settings.GROQ_API_KEY:
        raise ValueError("❌ GROQ_API_KEY not set in .env or Streamlit Secrets")
    
    if not settings.GROQ_API_KEY.startswith("gsk_"):
        raise ValueError("❌ GROQ_API_KEY format invalid (should start with 'gsk_')")

    try:
        llm = Groq(api_key=settings.GROQ_API_KEY, model=model_name, temperature=0.7)
        _llm_cache[key] = llm
        return llm
    except Exception as e:
        raise Exception(f"Failed to initialize Groq: {str(e)}")

def get_gemini_llm(model_name: str):
    """Initialize and cache Gemini LLM"""
    key = f"gemini:{model_name}"
    if key in _llm_cache:
        return _llm_cache[key]

    if not settings.GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY not set in .env or Streamlit Secrets")
    
    if not settings.GEMINI_API_KEY.startswith("AIza"):
        raise ValueError("❌ GEMINI_API_KEY format invalid (should start with 'AIza')")

    try:
        llm = Gemini(api_key=settings.GEMINI_API_KEY, model=model_name)
        _llm_cache[key] = llm
        return llm
    except Exception as e:
        raise Exception(f"Failed to initialize Gemini: {str(e)}")

def get_llm(provider: str, model_name: str):
    """Get LLM instance by provider and model"""
    provider = provider.lower()
    
    if provider == "groq":
        if not settings.GROQ_API_KEY:
            raise ValueError("⚙️ Groq API Key not configured")
        if model_name not in settings.groq_model_list:
            raise ValueError(f"Model '{model_name}' not in allowed list")
        return get_groq_llm(model_name)
    
    elif provider == "gemini":
        if not settings.GEMINI_API_KEY:
            raise ValueError("⚙️ Gemini API Key not configured")
        if model_name not in settings.gemini_model_list:
            raise ValueError(f"Model '{model_name}' not in allowed list")
        return get_gemini_llm(model_name)
    
    else:
        raise ValueError(f"Unknown provider: {provider}")

def clear_cache():
    """Clear LLM cache"""
    global _llm_cache
    _llm_cache.clear()