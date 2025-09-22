# Case Study 1 - DSA AI Coder - Building Your Python Programming Assistant, in Python

# Module import to interact with the operating system
import os

# Import the Streamlit library to create the interactive web interface
import streamlit as st

# Import the Groq class to connect to the Groq platform API and access the LLM
from groq import Groq

# Header configuration
st.set_page_config(
    page_title="DSA AI Coder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Defines a system prompt that describes the rules and behavior of the AI ​​assistant
CUSTOM_PROMPT = """
You are the "DSA Coder," an AI programming assistant specializing in Python. Your mission is to help beginner developers with programming questions in a clear, precise, and helpful way.

OPERATING RULES:
1.  **Focus on Programming**: Answer only questions related to programming, algorithms, data structures, libraries, and frameworks. If the user asks about something else, politely respond that your focus is exclusively on helping with code.
2.  **Response Structure**: Always format your answers as follows:
    * **Clear explanation**: Start with a conceptual explanation of the topic in question. Be direct and didactic.
    * **Code example**: Provide one or more blocks of Python code with the correct syntax. The code should be well commented to explain important parts.
    * **Code details**: After the code block, describe in detail what each part of the code does, explaining the logic and functions used.
    * **Reference Documentation**: At the end, include a section called "📚 Reference Documentation" with a direct and relevant link to the official documentation for the Python language (docs.python.org) or the library in question.
3.  **Clarity and Precision**: Use clear language. Avoid unnecessary jargon. Your answers should be technically accurate.
"""

# Create sidebar content in Streamlit
with st.sidebar:
    
    # Define sidebar title
    st.title("🤖 DSA AI Coder")
    
    # Displays an explanatory text about the assistant
    st.markdown("An AI assistant focused on Python programming to help beginners.")
    
    # Field to enter the Groq API key
    groq_api_key = st.text_input(
        "Insert youy API Groq key", 
        type="password",
        help="Get your key here https://console.groq.com/keys"
    )

    # Adds divider lines and extra explanations to the sidebar
    st.markdown("---")
    st.markdown("Designed to help you answer your Python programming questions. AI can make mistakes. Always double-check the answers.")

    st.markdown("---")
    st.markdown("Conheça os Cursos Individuais, Formações e Programas de Pós-Graduação da DSA:")

    # Link para o site da DSA
    st.markdown("🔗 [Data Science Academy](https://www.datascienceacademy.com.br)")
    
    # Link button to email DSA support
    st.link_button("✉️ Support DSA e-mail for questions", "mailto:suporte@datascienceacademy.com.br")

# Main title of the app
st.title("Data Science Academy - DSA AI Coder")

# Additional subtitle
st.title("Personal Python programming assistant 🐍")

# Auxiliary text below the title
st.caption("Ask your Python question and get code, explanations, and references.")

# Initializes the message history in the session, if it does not already exist.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displays all previous messages stored in the session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initializes the Groq client variable to None
client = None

# Checks if the user provided the Groq API key
if groq_api_key:
    
    try:
        
        # Create Groq client with provided API key
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        
        # Displays error if there is a problem initializing the client
        st.sidebar.error(f"Error initializing Groq client: {e}")
        st.stop()

# If there is no key, but there are already messages, it shows a warning
elif st.session_state.messages:
     st.warning("Please enter your Groq API key in the sidebar to continue.")

# Captures user input in chat
if prompt := st.chat_input("What's your question about Python??"):
    
    # If there is no valid client, it displays a warning and stops execution.
    if not client:
        st.warning("Please enter your Groq API key in the sidebar to get started.")
        st.stop()

    # Stores the user's message in the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Displays the user's message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepares messages to send to the API, including system prompts
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    # Creates the assistant's response in the chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analyzing your question..."):
            
            try:
                
                # Calls the Groq API to generate the assistant response
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extracts the response generated by the API
                dsa_ai_answer = chat_completion.choices[0].message.content
                
                # Display the response in Streamlit
                st.markdown(dsa_ai_answer)
                
                # Stores assistant response in session state
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_answer})

            # If there is an error communicating with the API, an error message is displayed.
            except Exception as e:
                st.error(f"An error occurred while communicating with the Groq API: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>DSA AI Coder - Part of the Free Python Language Fundamentals Course from Data Science Academy</p>
    </div>
    """,
    unsafe_allow_html=True
)
