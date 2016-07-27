####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
####################################################################################################
import random

DSimple = {
        'start':      ['Nock Nock' ],
        'greeting':   ['Hi!' ],
        'explain':    ['I spy? you!' ],
        'refere_to':  ['%(obj)s?'],
        'success':    ['Yey Yey!', 
                       'Yeah!' ],
        'failed':     ['Oh!' ],
        'asr_failed': ['What?'],
        'try_again':  ['again!?'],
        'goodbye':    [ 'Bye bye.',
                      ],
        'cheat':      ['cheat!'],
        'clarification':    ['What one?'],
        'clarification2':    ['What?'],
        'other':      ['other thing!'],
        'pick':       ['Go!'],
        'Ah,!':       ['Ah,!'],
        'shuffle':    ['Resort please'],
        'ready':      ['Finished?'],
      }


DComplex = {
        'start':      ['Nock Nock' ],
        'greeting':   ['Hi!', 
                       'Hello!' ],
        'explain':    ['Let us play the I spy game, you start! Go!' ],
        'refere_to':  ['Is it the %(obj)s?', 
                       'the %(obj)s?',
                       'That %(obj)s?'],
        'success':    ['Yeah^^!', 
                       'Yes^^!' ],
        'failed':     ['Let me try again.', 
                       'Oh, but this time' ],
        'asr_failed': ['Sorry, but I did not understand you.'],
        'try_again':  ['Do you want to try again?'],
        'goodbye':    [ 'Thank you for playing the game with me.', 
                       'Goodbye.',
                       'Bye bye.',
                      ],
        'cheat':      ['You are cheating!'],
        'clarification':    ['Which one is it?'],
        'clarification2':    ['What did you say?'],
        'other':      ['Use other objects!'],
        'pick':       ['Go for it!'],
        'Ah,!':       ['Ah,!'],
        'shuffle':    ['Resort please'],
        'ready':      ['Finished?'],
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
        
    