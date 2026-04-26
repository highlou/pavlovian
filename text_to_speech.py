# Created 2024-11-05

import pyttsx3
import threading, time, re

# Credit: https://gist.github.com/n1n9-jp/5857d7725f3b14cbc8ec3e878e4307ce
def remove_emojis(text):
    regex = re.compile(
        '['
        u'\U00002700-\U000027BF'  # Dingbats
        u'\U0001F600-\U0001F64F'  # Emoticons
        u'\U00002600-\U000026FF'  # Miscellaneous Symbols
        u'\U0001F300-\U0001F5FF'  # Miscellaneous Symbols And Pictographs
        u'\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
        u'\U0001FA70-\U0001FAFF'  # Symbols and Pictographs Extended-A
        u'\U0001F680-\U0001F6FF'  # Transport and Map Symbols
        ']+',
        re.UNICODE
    )
    return re.sub(regex, '', text)

class StreamTTS:
    _stream: str
    _queue: list
    
    engine: None
    remove_emojis: bool
    min_sentence_limit: int
    pause_every_line: bool
    min_sentence_limit: int
    flush_limit: int

    def __init__(self,
                 engine=None,
                 remove_emojis=True,
                 remove_asterisks=True,
                 pause_every_line=True,
                 min_sentence_limit=20,
                 flush_limit=200):
        self._stream = ''
        self._queue = []
        if engine == None: self.engine = pyttsx3.init()
        else: self.engine = engine
        self.remove_asterisks = remove_asterisks
        self.remove_emojis = remove_emojis
        self.pause_every_line = pause_every_line
        self.min_sentence_limit = min_sentence_limit
        self.flush_limit = flush_limit

    def start(self):
        self.engine.startLoop(False)

    def stop(self):
        self.engine.endLoop()

    def say(self, text):
        text_to_say = text

        # Remove special characters if desired
        if self.remove_emojis:
            text_to_say = remove_emojis(text_to_say)
        if self.remove_asterisks:
            text_to_say = text_to_say.replace('*', '')

        # Add the chunk of text (with special characters possibly removed) to
        # the queue and process it
        self._queue.append(text_to_say)
        self._process_queue()

    def flush(self):
        self._process_queue(True)
        while self.engine.isBusy():
            self.engine.iterate()
            time.sleep(0.025)

    def empty_stream(self):
        self._stream.clear()

    def is_queue_empty(self):
        return len(self._queue) == 0 and len(self._stream) == 0

    def _process_queue(self, flush=False):
        while len(self._queue) > 0:
            self._stream += self._queue.pop(0)

        regex = r'[^.,!?]+[.,!?]+'
        matches = re.findall(regex, self._stream)

        if flush or len(self._stream) >= self.flush_limit:
            self._say(self._stream)
            self._stream = ''
        elif len(matches) > 0:
            text = ' '.join(matches).strip()
            if len(text) >= self.min_sentence_limit:
                self._say(text)
                for m in matches:
                    self._stream = self._stream.replace(m, '')

    def _say(self, text):
        self.engine.say(text)
        self.engine.iterate()
        
        if self.pause_every_line:
            while self.engine.isBusy():
                self.engine.iterate()
                time.sleep(0.025)
