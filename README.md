# Private LLM chatbot using WebGPU

This project implements a chatbot application that leverages the power of large language models (LLMs) to interact with users and analyze PDF documents. Users can upload a PDF, and then engage in a conversational interface to ask questions about the document's content. The chatbot provides answers formatted with Markdown for improved readability.

**Important Note:** WebGPU is designed to be 100% offline and private once set up. However, it requires an initial download of the model. After this initial download, the application operates entirely on your local machine, ensuring your prompts remain private and secure.

## Background:

The application utilizes the unsloth/Phi-3-mini-4k-instruct model (Phi-3 as default you can use whatever model you like), a powerful causal language model, for natural language understanding and generation. It integrates PDF processing capabilities using PyPDF2 to extract text from uploaded PDF files. The Flask framework provides the web application infrastructure, creating a user-friendly interface for interacting with the chatbot.

## Features:

1. **PDF Upload and Analysis:** Users can upload PDF documents for analysis. The application extracts text from the PDF and makes it available to the chatbot.
2. **Conversational Interface:** A user-friendly chat interface allows for natural language interaction with the AI.
3. **Markdown Formatting:** The chatbot responses are formatted using Markdown, enhancing readability and providing structure to the information.
4. **Clear Conversation Button:** Allows users to easily clear the chat history.

## Installation

You can set up this project either by cloning the repository or by downloading the files directly.

### Option 1: Cloning the Repository

1. Clone the repository:
   ```
   git clone https://github.com/LMLK-seal/WebGPU.git
   ```
2. Navigate to the project directory:
   ```
   cd WebGPU
   ```

### Option 2: Downloading Files Directly

If you prefer not to clone the repository, you can download the necessary files directly:

1. Download the following files:
   - `app.py`
   - `static/css/styles.css`
   - `static/js/main.js`
   - `static/images/main.png`
   - `templates/index.html`

2. Ensure you maintain the same directory structure when saving the files locally.

### Setting Up the Environment

Regardless of which option you choose, follow these steps to set up your environment:

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
or use:

```
   pip install torch transformers flask PyPDF2 markdown
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your web browser and navigate to `http://localhost:5000` to view the application.

## Note

Make sure you have Python 3.7+ installed on your system before proceeding with the installation.

## Usage:

Navigate to the application URL in your web browser.

Upload a PDF document (Optional).

Type your questions in the chat interface and click "Send".

The chatbot will respond with answers based on the provided PDF and the overall instructions.

## Note:

You'll need a working internet connection to download the LLM and its associated files. The initial load time might be significant depending on your internet speed and hardware.

The unsloth/Phi-3-mini-4k-instruct model is relatively small, offering a balance between performance and resource requirements. Larger models could be substituted, but would require more computational resources. Adjust the max_new_tokens parameter in app.py to control the length of the chatbot's responses.

Contributions and improvements are welcome!
