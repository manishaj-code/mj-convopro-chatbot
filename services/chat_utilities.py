from llama_index.core.llms import ChatMessage, MessageRole
from llm_factory.get_llm import get_llm

def get_answer(provider: str, model_name: str, chat_history: list) -> str:
    """Get answer from LLM based on chat history"""
    try:
        llm = get_llm(provider, model_name)
        
        messages = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content="""You are ConvoPro, a helpful and friendly AI assistant.
Provide clear, accurate, and concise answers to user questions.
- Be conversational and engaging
- Ask clarifying questions if needed
- Provide detailed explanations when appropriate
- Use markdown formatting for better readability
- Keep responses well-organized and easy to understand"""
            )
        ]
        
        for msg in chat_history:
            messages.append(
                ChatMessage(
                    role=MessageRole[msg["role"].upper()],
                    content=msg["content"]
                )
            )
        
        response = llm.chat(messages=messages)
        return response.message.content
    except Exception as e:
        raise Exception(f"Error getting response: {str(e)}")