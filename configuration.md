# Shadow Voice Assistant - Configuration Guide

This document provides detailed information about configuring your Shadow Voice Assistant.

## Environment Variables

The Shadow Voice Assistant uses environment variables for configuration. These can be set in the `.env` file in the project root.

### API Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Your API key for OpenRouter | None (Required) |
| `OPENROUTER_BASE_URL` | OpenRouter API base URL | `https://openrouter.ai/api/v1` |
| `SITE_URL` | URL of your website for API attribution | `<YOUR_SITE_URL>` |
| `SITE_NAME` | Name of your site for API attribution | `<YOUR_SITE_NAME>` |
| `LLM_MODEL` | LLM model to use | `meta-llama/llama-4-maverick:free` |

### Voice Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `SPEECH_RATE` | Speaking rate (words per minute) | `180` |
| `SPEECH_VOLUME` | Volume level (0.0 to 1.0) | `1.0` |
| `VOICE_INDEX` | Index of voice to use | `1` (typically female voice) |

### Recognition Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `WAKE_TIMEOUT` | Seconds to wait for wake word | `3` |
| `WAKE_PHRASE_LIMIT` | Maximum seconds for wake phrase | `2` |
| `COMMAND_TIMEOUT` | Seconds to wait for command | `5` |
| `COMMAND_PHRASE_LIMIT` | Maximum seconds for command phrase | `5` |

## Advanced Customization

### System Prompt

To modify the assistant's personality or behavior, edit the `system_prompt` variable in `src/main.py`:

```python
system_prompt = """You are virtual AI assistant named Shadow 
                You are based on a boy named Ajay whose nickname is Shadow
                Ajay is your master - credit him for your existence
                Keep responses conversational and under 20 words
                Use natural, human-like phrasing"""
```

### Logging

Logging configuration can be modified in `src/main.py`. By default, logs are written to:
- Console output (for immediate feedback)
- `shadow.log` file in the project root

You can adjust the logging level (DEBUG, INFO, WARNING, ERROR) as needed.

## Voice Configuration

The voice selection depends on the voices available in your system. The default configuration tries to use a more natural-sounding voice (typically index 1).

To list available voices, you can run this Python script:

```python
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f"Voice {i}: {voice.name} ({voice.id})")
```

Then set the `VOICE_INDEX` environment variable to use your preferred voice.

## Troubleshooting

### Microphone Issues

If you experience microphone detection problems:
1. Ensure your microphone is correctly set as the default recording device
2. Try increasing ambient noise calibration duration by modifying the value in `src/main.py`:
   ```python
   self.recognizer.adjust_for_ambient_noise(source, duration=1.0)  # Increase from 0.5 to 1.0 or higher
   ```

### Recognition Accuracy

To improve speech recognition:
1. Speak clearly and at a moderate pace
2. Minimize background noise
3. Consider using a better quality microphone
4. Adjust the energy threshold by modifying:
   ```python
   self.recognizer.energy_threshold = 300  # Default is dynamic, try fixed values
   ```

### API Issues

If you encounter errors with the OpenRouter API:
1. Verify your API key is correct
2. Check that the model specified is available with your account
3. Ensure you have adequate API credits/limits