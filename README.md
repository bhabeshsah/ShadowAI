# Shadow Voice Assistant

A voice-controlled AI assistant that responds to the wake word "Shadow" and processes commands using LLM technology.

![Shadow Voice Assistant](docs/shadow_logo.png)

## Features

- 🎤 Voice activation with the wake word "Shadow"
- 🔊 Natural-sounding text-to-speech responses
- 🧠 AI-powered responses using LLMs through OpenRouter API
- 🌐 Customizable personality and voice settings
- 📝 Detailed logging for debugging and performance monitoring

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/shadow.git
   cd shadow
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment template and add your API key:
   ```bash
   cp .env.template .env
   ```
   Then edit the `.env` file to add your OpenRouter API key and customize settings.

## Usage

Run the assistant:

```bash
python src/main.py
```

Once running:
1. Wait for the "Shadow initialized and ready!" message
2. Say "Shadow" to activate the assistant
3. When you hear "Yes? How can I help you today?", ask your question
4. Listen for the response

To exit, press Ctrl+C.

## Configuration

Edit the `.env` file to customize:

- API keys and endpoints
- Voice parameters (rate, volume, voice selection)
- Listening timeouts and sensitivity
- LLM model selection

See `docs/configuration.md` for detailed configuration options.

## Credits

- Created by: [Your Name]
- Based on Ajay's "Shadow" concept
- Uses OpenRouter API for LLM access

## License

This project is licensed under the MIT License - see the LICENSE file for details.