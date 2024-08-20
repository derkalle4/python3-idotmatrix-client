# Run Assistant

This script uses OpenAI's function calling functionality to perform tasks with your screen. You can ask the assistant to perform tasks like turning on the screen, setting the screen color, starting a timer, etc.

# Pre-requisites
- You need to have an OpenAI account and an API key. You can get one [here](https://platform.openai.com/).
- Store your key as an environment variable `OPENAI_API_KEY`.

1. Install OpenAI's library,

```
    pip install openai
```

2. Run the script,

```
    python assistant/assistant.py
```
3. Ask the assistant to perform a task.


# Example
```
    python assistant/assistant.py
```

```
    Screen on 
    
    set screen color to red

    timer for 10 minutes

    pause timer

    set demo.gif and process it to 32 pixels

```


# Checklist
- [x] Implement basic functionality
- [x] Implement image and gif functionality to allow assitant to create and send pictures to the screen
- [] Allow assistant to find relevant image and gifs from local
- [] Allow assistant to find relevant image and gifs from internet
- [] Allow assistant to create images and gifs
- [] Fix buggy text
- [] Put together a simple web GUI to interact with the agent
- [] Add support for multiple agent backends
- [] Add voice support