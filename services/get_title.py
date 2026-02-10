from llama_index.core import PromptTemplate
from llm_factory.get_llm import get_llm

def get_chat_title(provider: str, model_name: str, user_query: str) -> str:
    """Generate a concise title for the chat based on user query"""
    try:
        llm = get_llm(provider, model_name)
        
        title_prompt_template = (
            "Generate a short, clear chat title based on this query.\n"
            "Rules:\n"
            "- Maximum 5 words\n"
            "- No punctuation\n"
            "- Summarize the main topic\n"
            "- Be concise and clear\n\n"
            "Query: {user_query}\n\n"
            "Title:"
        )
        
        title_prompt = PromptTemplate(title_prompt_template).format(user_query=user_query)
        title = llm.complete(prompt=title_prompt).text.strip()
        title = title.replace("Title:", "").strip()
        
        if len(title) > 50:
            title = title[:50] + "..."
        
        return title or "New Chat"
    except Exception as e:
        return "New Chat"