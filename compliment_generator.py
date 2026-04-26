# Created 2026-04-05

import sys
import ollama

import compliments
from util import *
import private

USAGE = f'''USAGE:
        {sys.argv[0]} <name: str> <age: int> <gender: str> <n_compliments: int> <model: str>

    name: Name of complementee
    age: Age of complementee
    gender: Gender of complementee
    n_compliments: Number of compliments to generate
    model: Name of LLM to use availabe on Ollama'''

COMPLIMENT_MAX_LEN_CHARS = 350

if __name__ == '__main__':
    set_usage(USAGE)

    assert_usage(len(sys.argv) == 6)
    
    _, name, age, gender, n_compliments, model = unpack_typed(
        sys.argv,
        None,
        str,
        int,
        str,
        int,
        str
    )

    comp_list = []

    extra_info_msg = f'''Here's some extra info about them:
---
{private.COMPLINMENTEE_EXTRA_INFO}
---''' if private.COMPLINMENTEE_EXTRA_INFO else ''
    
    for i in range(n_compliments):
        print('Generating compliment', i+1, end='...', flush=True)

        prompt = f'Generate ONLY ONE SUPER WARM AND KIND-HEARTED AND CARING one-to-two-sentence\
compliment which incorporates ALL INFORMATION AVAILABLE to a {age}-year-old {gender} named {name}.\n{extra_info_msg}'
        
        # print('prompt:', prompt)

        try_again = True

        while try_again:
            response = ollama.generate(
                model,
                prompt,
                options={
                    'temperature': 5.0
                }
            )

            if len(response.response) <= COMPLIMENT_MAX_LEN_CHARS:
                try_again = False
        
        comp_list.append({
            'text': response.response
        })

        print(f'Done! ({len(response.response)}) chars')
    
    compliments.store_compliments(comp_list)

    print('Compliments stored!')
