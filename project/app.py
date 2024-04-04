import utils
import streamlit as st
from dotenv import load_dotenv
import os
import asyncio
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.prompt_template.input_variable import InputVariable
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Load environment variables from .env file
load_dotenv()

pdf_path = "../data/raw/human-nutrition-text.pdf"
selected_page_numbers = [378, 379, 380, 381]

kernel = sk.Kernel()
service_id = None

async def chat_to_summarize(text_combined):
    deployment = os.getenv("AZURE_DEPLOYMENT")
    api_key = os.getenv("AZURE_API_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")

    service_id = "aoai_chat_completion"
    kernel.add_service(
        AzureChatCompletion(service_id=service_id, deployment_name=deployment, endpoint=endpoint, api_key=api_key),
    )

    prompt = """
    1. You are a writer that will create a summary based on the data that is being provided
    2. You have to return a summary that is easy to understand and that is not too long
    3. Put a general Title to know the topic of the summary
    4. Put subtitles to separate the different sections of the summary, leave lines between the subtitles and the text

    {{$history}}
    Data Provided to realize the summary: {{$user_input}}
     """

    execution_settings = sk_oai.OpenAIChatPromptExecutionSettings(
        service_id=service_id,
        ai_model_id=deployment,
        max_tokens=4000,
        temperature=0.3,
    )

    prompt_template_config = sk.PromptTemplateConfig(
    template=prompt,
    name="chat",
    template_format="semantic-kernel",
    input_variables=[
        InputVariable(name="input", description="The user input", is_required=True),
        InputVariable(name="history", description="The conversation history", is_required=True),
    ],
    execution_settings=execution_settings,
    )

    chat_function = kernel.create_function_from_prompt(
        function_name="chat",
        plugin_name="chatPlugin",
        prompt_template_config=prompt_template_config,
    )

    chat_history = ChatHistory()
    chat_history.add_system_message("Remember to be aware of a correct grammar")

    arguments = KernelArguments(user_input=text_combined, history=chat_history)

    print("Starting summarization...")
    response = await kernel.invoke(chat_function, arguments)
    return response

def main():
    # Call the function to download the pdf_file
    utils.download_pdf_file()
    pages_and_texts = utils.open_and_read_pdf(pdf_path=pdf_path)

    st.sidebar.title("Select Mode")
    st.sidebar.markdown("Test pages: [378, 379, 380, 381]")
    st.sidebar.markdown("Custom pages: You can choose (separated by commas)")
    mode = st.sidebar.radio("Mode", ("Test", "Custom"))
    
    if mode == "Test":
        selected_page_numbers = '378, 379, 380, 381'
        text_combined = "This is a test using predefined pages: [378, 379, 380, 381]"
    else:
        selected_page_numbers = st.sidebar.text_input("Enter page numbers separated by commas:")

    summarize_button = st.sidebar.button("Summarize")

    if summarize_button:
        if selected_page_numbers:
            selected_page_numbers = [int(page_num.strip()) for page_num in selected_page_numbers.split(',')]
            # Select the pages we want to summarize
            selected_pages = utils.select_example_pages(pages_and_texts, selected_page_numbers)

            # Extract 'text' values from selected_pages and join them into a single string
            text_combined = ' '.join(page['text'] for page in selected_pages)

            # Summarize
            response = asyncio.run(chat_to_summarize(text_combined))
            st.subheader("Summary:")
            st.write(response)
        else:
            st.warning("Please enter page numbers before summarizing.")

if __name__ == "__main__":
    main()