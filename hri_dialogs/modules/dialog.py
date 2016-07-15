####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
####################################################################################################
import random

DSimple = {
        'start':      ['I am here' ],
        'greeting':   ['Hi' ],
        'explain':    ['Please play the I spy game with me.' ],
        'refere_to':  ['%(obj)s?'],
        'success':    ['Yeah!', 
                       'Yuchu!' ],
        'failed':     ['Let me try again.', 
                       'Oh, but this time' ],
        'asr_failed': ['Sorry, but I did not understand you.'],
        'try_again':  ['again?'],
        'goodbye':    [ 'Bye bye.',
                      ], 

      }


DComplex = {
        'start':      ['I am here' ],
        'greeting':   ['Hi!', 
                       'Hello!',
                       'Good morning!' ],
        'explain':    ['Please play the I spy game with me.' ],
        'refere_to':  ['Is it the %(obj)s?', 
                       'the %(obj)s?',
                       'That %(obj)s?'],
        'success':    ['Yeah!', 
                       'Yuchu!' ],
        'failed':     ['Let me try again.', 
                       'Oh, but this time' ],
        'asr_failed': ['Sorry, but I did not understand you.'],
        'try_again':  ['Do you want to try again?'],
        'goodbye':    [ 'Thank you for playing the game with me.', 
                       'Goodbye.',
                       'Bye bye.',
                      ], 
      }



class Dialog(object):


    def __init__(self, dialog_type):
        
        if dialog_type == 'simple':
            self._db = DSimple
        else:
            self._db = DComplex


    def response(self, phrase):
        if phrase in self._db:
            responses = self._db[phrase]
            return responses[ random.randint(0, len(responses)-1) ]
        
    