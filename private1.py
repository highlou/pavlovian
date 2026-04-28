# Rename this to private.py and set the values of some of the constants for the
# code to work!

from datetime import datetime

# The absolute path of directory to this script.
SCRIPT_DIR = ''

# The filename of neutral sound in this directory.
NEUTRAL_SOUND_FILENAME = ''

# Extra information about complementee (optional).
COMPLEMENTEE_EXTRA_INFO: None | str = None

# Determines whether t is during DO NUT DISTURB time (optional).
def is_do_not_disturb_time(t: datetime) -> bool:
    return False

# Extra code that runs when the script is running in order to perform the
# experiment, instead of just setting up the experiment.
def setup(mode: None | str) -> None:
    pass

# This function is run when the code starts to play the stimulus to the user.
def on_stimulus(neutral_only: bool) -> None:
    pass

# This function is run after the code finishes playing the stimulus to the user
# (optional).
def on_stimulus_end(neutral_only: bool, compliment: str=None) -> None:
    pass
