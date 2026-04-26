# Created 2026-04-25

import random, time, json, os, sys
# import calendar
from datetime import datetime, timedelta

from playsound3 import playsound

import compliments
import text_to_speech
import private
import util

USAGE = f'''USAGE:
        {sys.argv[0]} <mode: enum|optional>

    mode: Either 'setup' (sets up the experiment) or not passed at all'''

SCRIPT_DIR = private.SCRIPT_DIR

EXPERIMENT_INFO_FILENAME = "experiment_info.json"
EXPERIMENT_INFO_FILEPATH = os.path.join(SCRIPT_DIR, EXPERIMENT_INFO_FILENAME)

NEUTRAL_SOUND_FILENAME = private.NEUTRAL_SOUND_FILENAME
NEUTRAL_SOUND_FILEPATH = os.path.join(SCRIPT_DIR, NEUTRAL_SOUND_FILENAME)

EXPERIMENT_LENGTH = 6
DAYS_UNTIL_ONLY_NEUTRAL = 5

SPEECH_RATE_WPM = 160
TIME_WAIT_MAX_S = 3 * 60 * 60
TIME_WAIT_MIN_S = 1 * 60 * 60

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

def do_random_compliment(update_comp_list: bool = True):
    comp_list = compliments.load_compliments()
    idx = random.randint(0, len(comp_list))
    compliment = comp_list.pop(idx)

    tts.say(compliment['text'])
    tts.flush()
    
    if update_comp_list:
        compliments.store_compliments(comp_list)

def do_neutral_stimulus():
    playsound(NEUTRAL_SOUND_FILEPATH)

def do_unconditioned_stimulus():
    do_random_compliment()

def do_both_stimuli():
    do_neutral_stimulus()
    do_unconditioned_stimulus()

if __name__ == '__main__':
    util.set_usage(USAGE)
    util.assert_usage(len(sys.argv) <= 2, 'not the right number of arguments')

    mode = None
    if len(sys.argv) == 2:
        mode = sys.argv[1]

    util.assert_usage(mode in (None, 'setup'), "mode neither 'setup' nor omitted")

    if mode == 'setup':
        today = datetime.fromtimestamp(time.mktime(time.localtime())).date()

        experiment_info = {
            'dtd_start_date': today.timetuple(),
            'dtd_only_neutral_date': (today + timedelta(days=DAYS_UNTIL_ONLY_NEUTRAL)).timetuple(),
            'dtd_end_date': (today + timedelta(days=EXPERIMENT_LENGTH)).timetuple()
        }

        store_experiment_info(experiment_info)
    else:
        tts = text_to_speech.StreamTTS()

        tts.start()

        tts.engine.setProperty('rate', SPEECH_RATE_WPM)
        
        experiment_info = load_experiment_info()

        while True:
            time.sleep(random.randint(TIME_WAIT_MIN_S, TIME_WAIT_MAX_S))

            today = datetime.fromtimestamp(time.mktime(time.localtime())).date()
            
            if today < experiment_info['dtd_only_neutral_date']:
                # Part A: Play both neutral and unconditioned stimulus.
                do_both_stimuli()
            elif today >= experiment_info['dtd_only_neutral_date'] \
                    and today <= experiment_info['dtd_end_date']:
                # Part B: Play just the neutral stimulus.
                do_neutral_stimulus()
            else: # Part C: This experiment is over. Quit.
                break
