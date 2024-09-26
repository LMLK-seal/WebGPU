# Private LLM chatbot using WebGPU

This project implements a chatbot application that leverages the power of large language models (LLMs) to interact with users and analyze PDF documents. Users can upload a PDF, and then engage in a conversational interface to ask questions about the document's content. The chatbot provides answers formatted with Markdown for improved readability.

## Background:

The application utilizes the unsloth/Phi-3-mini-4k-instruct model, a powerful causal language model, for natural language understanding and generation. It integrates PDF processing capabilities using PyPDF2 to extract text from uploaded PDF files. The Flask framework provides the web application infrastructure, creating a user-friendly interface for interacting with the chatbot.

## Features:

1. **PDF Upload and Analysis:** Users can upload PDF documents for analysis. The application extracts text from the PDF and makes it available to the chatbot.
2. **Conversational Interface:** A user-friendly chat interface allows for natural language interaction with the AI.
3. **Markdown Formatting:** The chatbot responses are formatted using Markdown, enhancing readability and providing structure to the information.
4. **Clear Conversation Button:** Allows users to easily clear the chat history.

## Installation:

1. Clone the repository:

git clone https://github.com/LMLK-seal/WebGPU.git

2. Create a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt
or
You can install these libraries using pip: 
```
   pip install torch transformers flask PyPDF2 markdown
   ```

4. Run the application:

python app.py

The application will start on http://127.0.0.1:5000/.

## Usage:

Navigate to the application URL in your web browser.

Upload a PDF document (Optional).

Type your questions in the chat interface and click "Send".

The chatbot will respond with answers based on the provided PDF and the overall instructions.

## Note:

You'll need a working internet connection to download the LLM and its associated files. The initial load time might be significant depending on your internet speed and hardware.

The unsloth/Phi-3-mini-4k-instruct model is relatively small, offering a balance between performance and resource requirements. Larger models could be substituted, but would require more computational resources. Adjust the max_new_tokens parameter in app.py to control the length of the chatbot's responses.

Contributions and improvements are welcome!
