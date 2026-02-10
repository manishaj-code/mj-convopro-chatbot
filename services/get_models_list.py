from config.settings import get_settings

settings = get_settings

def get_models_list() -> dict:
    """Returns available models for each provider"""
    models = {
        "groq": settings.groq_model_list if settings.GROQ_API_KEY else [],
        "gemini": settings.gemini_model_list if settings.GEMINI_API_KEY else [],
    }
    return {k: v for k, v in models.items() if v}

def get_provider_info() -> dict:
    """Get provider information and branding"""
    return {
        "groq": {
            "name": "Groq",
            "icon": "⚡",
            "description": "Ultra-fast inference",
            "color": "#FF6B6B"
        },
        "gemini": {
            "name": "Google Gemini",
            "icon": "🔮",
            "description": "Advanced reasoning",
            "color": "#4285F4"
        }
    }

if __name__ == "__main__":
    import pprint
    pprint.pprint(get_models_list())