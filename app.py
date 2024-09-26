import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from flask import Flask, render_template, request, jsonify, current_app
import PyPDF2
import logging

# Global variables for model, tokenizer, and pipeline
model = None
tokenizer = None
pipe = None

def create_app():
    app = Flask(__name__, static_url_path='/static', template_folder='templates')

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = app.logger

    def load_model():
        global model, tokenizer, pipe
        try:
            torch.random.manual_seed(0)
            model = AutoModelForCausalLM.from_pretrained(
                "unsloth/Phi-3-mini-4k-instruct",
                device_map="auto",
                torch_dtype="auto",
                trust_remote_code=True,
            )
            tokenizer = AutoTokenizer.from_pretrained("unsloth/Phi-3-mini-4k-instruct")
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
            )
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model: {e}")

    # Load the model when the app is created
    with app.app_context():
        load_model()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload_pdf', methods=['POST'])
    def upload_pdf():
        try:
            pdf_file = request.files.get('pdf')
            if not pdf_file:
                return jsonify({'status': 'error', 'message': 'No PDF file provided.'})

            pdf_reader = PyPDF2.PdfReader(pdf_file)
            extracted_text = ""
            for page in pdf_reader.pages:
                extracted_text += page.extract_text()

            current_app.config['extracted_text'] = extracted_text
            logger.info("PDF processed successfully")
            return jsonify({'status': 'success', 'message': 'PDF uploaded and processed.'})

        except PyPDF2.errors.PdfReadError:
            logger.error("Error reading PDF file")
            return jsonify({'status': 'error', 'message': 'Error reading PDF file. Is it a valid PDF?'})
        except Exception as e:
            logger.error(f"Unexpected error during PDF processing: {e}")
            return jsonify({'status': 'error', 'message': f'An unexpected error occurred during PDF processing: {str(e)}'})

    @app.route('/chat', methods=['POST'])
    def chat():
        global model, tokenizer, pipe
        
        if not all([model, tokenizer, pipe]):
            logger.error("Model not initialized")
            return jsonify({'status': 'error', 'message': 'Model not initialized. Please try again later.'})

        try:
            data = request.get_json()
            messages = data.get('messages', [])

            if not messages:
                return jsonify({'status': 'error', 'message': 'No messages provided.'})

            # Updated system message with Markdown formatting instructions
            system_message = {
                "role": "system", 
                "content": "You are a helpful AI assistant. Format your responses using Markdown syntax:\n"
                           "- Use **bold** for headlines and important terms\n"
                           "- Use *italics* for emphasis\n"
                           "- Use --- for horizontal rules\n"
                           "- Use bullet points (-, *, +) for lists\n"
                           "- Use numbers (1., 2., 3.) for ordered lists\n"
                           "- Use > for blockquotes\n"
                           "- Use `backticks` for inline code\n"
                           "- Use ```language\ncode\n``` for code blocks\n"
                           "- Use __underline__ before colons in key terms\n"
                           "Ensure your responses are well-structured and easy to read."
            }
            messages.insert(0, system_message)

            # Access the extracted text
            extracted_text = current_app.config.get('extracted_text', "")
            if extracted_text:
                pdf_content_message = {"role": "system", "content": f"PDF Content:\n\n{extracted_text}"}
                messages.insert(1, pdf_content_message)

            generation_args = {
                "max_new_tokens": 500,
                "return_full_text": False,
                "temperature": 0.7,
                "do_sample": True,
            }

            logger.info(f"Sending messages to model: {messages}")

            output = pipe(messages, **generation_args)
            
            if isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict) and 'generated_text' in output[0]:
                response = output[0]['generated_text']
            else:
                raise ValueError("Unexpected model output structure")

            logger.info("Chat response generated successfully")
            return jsonify({'status': 'success', 'messages': [response]})

        except ValueError as ve:
            logger.error(f"Value error in chat processing: {ve}")
            return jsonify({'status': 'error', 'message': 'Invalid input or unexpected model output.'})
        except Exception as e:
            logger.error(f"Unexpected error in chat processing: {e}")
            return jsonify({'status': 'error', 'message': 'An unexpected error occurred. Please try again.'})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=True, reloader_type="stat", extra_files=None)
