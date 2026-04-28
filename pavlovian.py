# Created 2026-04-25

import random, time, json, os, sys
from datetime import datetime, timedelta

from playsound3 import playsound

import compliments
import text_to_speech
import private
import util

USAGE = f'''USAGE:
        {sys.argv[0]} <mode: enum|optional> <options for mode>

    mode: Either 'setup' (sets up the experiment) or not passed at all
        'setup':
                {sys.argv[0]} setup <length: int> <days_until_neutral: int>
            length: Length of experiment in days
            days_until_neutral: Number of days until the unconditioned stimulus is taken away'''

SCRIPT_DIR = private.SCRIPT_DIR

EXPERIMENT_INFO_FILENAME = "experiment_info.json"
EXPERIMENT_INFO_FILEPATH = os.path.join(SCRIPT_DIR, EXPERIMENT_INFO_FILENAME)

NEUTRAL_SOUND_FILENAME = private.NEUTRAL_SOUND_FILENAME
NEUTRAL_SOUND_FILEPATH = os.path.join(SCRIPT_DIR, NEUTRAL_SOUND_FILENAME)

SPEECH_RATE_WPM = 160
TIME_WAIT_MAX_S = 2 * 60 * 60
TIME_WAIT_MIN_S = 0.75 * 60 * 60

def load_experiment_info() -> list[dict]:
    experiment_info = None
    with open(EXPERIMENT_INFO_FILEPATH, encoding="ascii") as file:
        experiment_info = json.load(file)

    for k, v in experiment_info.items():
        if k.startswith('ts_'):
            experiment_info[k] = time.struct_time(v)
        elif k.startswith('dtd_'):
            experiment_info[k] = datetime.fromtimestamp(time.mktime(time.struct_time(v))).date()
        elif k.startswith('dt_'):
            experiment_info[k] = datetime.fromtimestamp(time.mktime(time.struct_time(v)))

    return experiment_info

def store_experiment_info(data: list[dict]) -> None:
    with open(EXPERIMENT_INFO_FILEPATH, mode="w", encoding="ascii") as file:
        json.dump(data, file, ensure_ascii=True, indent=2)

def do_random_compliment(update_comp_list: bool = True) -> str:
    comp_list = compliments.load_compliments()
    idx = random.randint(0, len(comp_list) - 1)
    compliment = comp_list.pop(idx)

    tts.say(compliment['text'])
    tts.flush()
    
    if update_comp_list:
        compliments.store_compliments(comp_list)
    
    return compliment['text']

def do_neutral_stimulus():
    playsound(NEUTRAL_SOUND_FILEPATH)

def do_unconditioned_stimulus() -> str:
    return do_random_compliment()

def do_both_stimuli() -> str:
    do_neutral_stimulus()
    return do_unconditioned_stimulus()

if __name__ == '__main__':
    util.set_usage(USAGE)

    mode = None
    if len(sys.argv) >= 2:
        mode = sys.argv[1]

    private.setup(mode)

    if mode == 'setup':
        util.assert_usage(len(sys.argv) == 4, 'too many or too few arguments for mode setup')
        
        _, _, experiment_length, days_until_only_neutral = util.unpack_typed(
            sys.argv,
            None,
            str,
            int,
            int
        )

        today = datetime.fromtimestamp(time.mktime(time.localtime())).date()

        experiment_info = {
            'dtd_start_date': today.timetuple(),
            'dtd_only_neutral_date': (today + timedelta(days=days_until_only_neutral)).timetuple(),
            'dtd_end_date': (today + timedelta(days=experiment_length)).timetuple()
        }

        store_experiment_info(experiment_info)
    elif mode == None:
        tts = text_to_speech.StreamTTS()

        tts.start()

        tts.engine.setProperty('rate', SPEECH_RATE_WPM)

        voices = tts.engine.getProperty('voices')
        tts.engine.setProperty('voice', voices[1].id)
        
        experiment_info = load_experiment_info()

        while True:
            time.sleep(random.uniform(TIME_WAIT_MIN_S, TIME_WAIT_MAX_S))

            dt_right_now = datetime.fromtimestamp(time.mktime(time.localtime()))
            today = dt_right_now.date()
            dt_time_of_day = dt_right_now.time()

            if private.is_do_not_disturb_time(dt_right_now):
                # No stimuli from the experiment should be played during this
                # time.
                continue
        
            neutral_only = False
            compliment = None
            
            if today < experiment_info['dtd_only_neutral_date']:
                neutral_only = False
            elif today >= experiment_info['dtd_only_neutral_date'] \
                    and today <= experiment_info['dtd_end_date']:
                neutral_only = True
            else: # Part C: This experiment is over. Quit.
                break
        
            private.on_stimulus(neutral_only)
            
            if not neutral_only:
                # Part A: Play both neutral and unconditioned stimulus.
                compliment = do_both_stimuli()
            else:
                # Part B: Play just the neutral stimulus.
                do_neutral_stimulus()
            
            private.on_stimulus_end(neutral_only, compliment)
    else:
        util.assert_usage(False, f'unknown mode {repr(mode)}')
