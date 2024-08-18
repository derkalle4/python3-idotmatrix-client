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
    # Turn on the screen
    Screen on 
    
    # Set color
    set screen color to red

    # start timer
    timer for 10 minutes

    # pause timer
    pause timer

```


# Checklist
- [x] Implement basic functionality
- [] Implement image and gif functionality to allow assitant to create and send pictures to the screen
- [] Fix buggy text
- [] Put together a simple web GUI to interact with the agent
- [] Add support for multiple agent backends