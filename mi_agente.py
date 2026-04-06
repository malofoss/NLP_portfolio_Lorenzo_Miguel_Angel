import gradio as gr

def simple_agent(message, history):
    # This is a simple logic to simulate an AI agent
    if "hello" in message.lower() or "hi" in message.lower():
        return "Hello there! I am your new AI agent for 2026. How can I help you?"
    elif "agent" in message.lower():
        return "Yes! 2026 is the year of the agents, and Gradio helps manage their UI."
    else:
        return f"I received your message: '{message}'. As an AI, I am still learning!"

# We create a Chat Interface, perfect for AI agents
demo = gr.ChatInterface(
    fn=simple_agent, 
    title="My First AI Agent Interface",
    description="A simple agent interface built with Gradio."
)

demo.launch()
