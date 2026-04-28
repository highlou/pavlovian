# pavlovian
Perform Pavlovian conditioning on yourself!

This is for an assignment of mine from my psychology class.

## How it works

In any Pavlovian conditioning experiment, there is the **unconditioned stimulus** (US), the **unconditioned response** (UR), the **neutral stimulus** (NS), the **conditioned stimulus** (CS), and the **conditioned response** (CR). The goal is that, after many times the unconditioned stimulus is paired with the neutral stimulus, the neutral stimulus will become a conditioned stimulus and create the same involuntary response (conditioned response) similar to the involuntary response from the uncnoditioned stimulus (unconditioned response).

Random times during the day, the program runs a neutral stimulus in the form of sound, and pairs it with the unconditioned stimulus, which is an AI-generated compliment toward the user.

Over time, the unconditioned response, which consist of the feelings generated from the AI-generate compliment, should (hopefully) become a conditioned response, such that when the the unconditioned stimulus is taken away near the end of the experiment, the neutral-stimulus-now-become-conditioned-stimulus would also generate a similar (conditioned) stimulus, even though at the start of the experiment the neutral stimulus did not previously triggered that kind of response.

## Running it on your computer

This project uses Python 3.

### Dependencies

This project needs the following libraries (you can also just check `requirements.txt`):
* ollama
* playsound
* pyttsx3

But they are automatically installed if you run `build.bat`.

### private1.py

Before the code is able to run you must first rename `private1.py` to `private.py` and set appropriate values to all the non-optional constants.

### The different scripts

#### pavlovian.py

This is the main script that does the Pavlovian conditioning. If you run it like so:
```cmd
python pavlovian.py setup <length of experiment> <days until only NS is played>
```

It sets up the Pavlovian experiment and save the information into `experiment_info.json`. It stores the date the experiment starts, which is the date on which you run the script, the last date of the experiment (end date), as well as the date starting on which the script will only play the neutral stimulus withou the unconditioned stimulus, depending on what you sent it.

If you run it without any arguments, it will play the neutral stimulus with or without the unconditioned stimulus, depending on the current day, at random times while your computer is running.

It gets its compliments come from `compliments.json`.

#### compliment_generator.py

Generates the compliments and saves them to `compliments.json`. Run the script itself or check the source code for proper usage.

## Build pavlovian.py

This project uses PyInstaller to build `pavlovian.py` into one executable file, `pavlovian.exe`, which will be placed in the project directory.

### On Windows

Just run:

```cmd
build.bat
```

And a console-less executable named `pavlovian.exe` will be created in the project directory.
