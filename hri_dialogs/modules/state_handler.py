####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
####################################################################################################
import random
from spy.modules.BaseModule   import BaseModule, main

import StringIO
import urllib2
import urllib

import pyaudio    
import time
import wave

import yarp
import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()


class StateHandler(BaseModule):
    """ The StateHandler class provides a yarp module to that handles the state of an HRI task.
    """

    def configure(self, rf):
        BaseModule.configure(self, rf)
    
        self.speechPort  = self.createOutputPort('speech')
        self.pointPort   = self.createOutputPort('point')
        self.textPort    = self.createInputPort('text')

        # mary settings
        self.speed       = 1.0
        self.locale      = 'en_GB'
        self.voice       = 'dfki-poppy'
        self.process_url = 'http://127.0.0.1:59125/process'

        # read database
        with open('Data_base_fruits.csv', 'r') as f:

            # remove header line
            # remove windows line ending character
            data         = [x.replace('\r', '')  for x in f.read().split('\n')[1:]]

            # split lines into entries and only keep entries that have 3 elements
            self.db      = [x.split(',') for x in data if len(x.split(',')) == 3]

            # get the set of available colors
            self.colors  = set([x[2] for x in self.db])

            # get the set of available objects
            self.objects = set([x[1] for x in self.db])

            # print the loaded database
            print '--- values ---'
            print 'colors: ',
            for x in self.colors:
                print x, 
            print ''

            print 'objects:',
            for x in self.objects:
                print x, 
            print ''

            print '--- database ---'
            for x in self.db:
                print '%s\t%s\t%s' % tuple(x)

        return True
    
    
    def updateModule(self):
        
        bottle = self.textPort.read()
        if bottle:
            print bottle.toString()
        
        return BaseModule.updateModule(self)


    def runModule(self, *args):
        self.configure(None)
        self.start()
        return True

#     def respond(self, command, reply):
#         """ This is the respond hook method which gets called upon receiving a bottle via RPC port.
# 
#         @param command - input bottle
#         @param reply - output bottle
#         @return boolean
#         """
#         success = False
# 
#         try:
#             if command.get(0).toString() == 'start':
#                 self.start()
#         except Exception as e:
#             print e
# 
#         # reply with success
#         reply.addString('ack' if success else 'nack')
#         return True


#     def say(self, text):
#         bottle  = yarp.Bottle()
#         bottle.clear()
# 
#         bottle.addString(text)
# 
#         self.speechPort.write(bottle)
    

    def point(self, location):
        bottle  = yarp.Bottle()
        bottle.clear()

        x = 0.1
        y = 0.1
        z = 0.1

        bottle.addDouble(x)
        bottle.addDouble(y)
        bottle.addDouble(z)

        self.pointPort.write(bottle)



    def recognizeSpeech(self):
        # Function which receive a sound and give back a sentence in the form of list of words.
        while True:
            print("I am listening")
            with m as source:
                audio = r.listen(source)
            print("Got it! Now to recognize it")
            try:
                    # recognize speech using Google Speech Recognition
                    a = r.recognize_google(audio)
                    print type(a)
                    a = a.encode('utf8')
                    print type(a)
                
                    # we need some special handling here to correctly print unicode characters to standard output
                    if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                        print("You said {}".format(a).encode("utf-8"))
                        break
                    else:  # this version of Python uses unicode for strings (Python 3+)
                        print("You said {}".format(a))
                        break
            except sr.UnknownValueError:
                        self.say("Oops! Did not catch that")
            except sr.RequestError as e:
                        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

                        # tts.say("Your text is : "+a)#verification 1
                        # tts.say("SLU will output a semantics for your text.")

        new_sentence = a.split()  # divide a big string in several little string divided by a space (=don't work for composed words). b is a list of little strings.
        print(new_sentence)  # verification 
        return new_sentence


    def findObjects(self):
        
        #
        # Gather Object Locations
        #
        
        # TODO: 

        # { <object id> : [<x-location>, <y-location>] }
        foundObjects = {}

        # { <object name>: [ <color>, [<x-location>, <y-location>] ] }
        self.objects = {}
        for oid, name, color in self.db:
            if oid in foundObjects:
                self.objects[name] = [color, foundObjects[oid]]
        

    def start(self):

        tries = 3
        self.findObjects()
        
        # MESSAGE DE DEPART
        self.say("I am listening!")
        
        #///////////////////////////////////////////////////////////////////////////////////////////
        #/                                         MAIN PROGRAM                                    /
        #///////////////////////////////////////////////////////////////////////////////////////////

        # Greeting*********************************************
        self.greetingResponse(self.recognizeSpeech(), tries)

        # program stop when stop == True
        stop = False   
        while not stop:

        # ACTIONS#############################################################################

            # Wait for a color in the sentence **************************************
            color = self.waitForColor()

            for _try in range(tries):
            
                # Question processing**************************
                obj   = self.searchColorInDB(color, _try)
                self.doYouMean(obj)
    
                answer = self.recognizeSpeech()
    
                if 'yes' in answer:
                    self.say('Yeah!')
                    break
                            
                elif 'no' in answer:
                    self.letMeTryAgain()


            # after n tries
            if 'no' in answer:
                self.say("Your are cheating!")
                time.sleep(0.5)
                self.say("Which one is it?")
                _ = self.recognizeSpeech()
                self.say('Ah, I see.')

            stop = self.repeat()
                
        # Leave********************************************
        self.goodbye()


    def greetingResponse(self, phrase, tries):

        # chose response phrase
        phrases = [ 'Hi!', 
                    'Hello!',
                    'Good morning!' ]
        phrase = phrases[ random.randint(0, len(phrases)-1) ]

        for g in ['hello' , 'morning' , 'hi']:
            if g in phrase:
                self.say(phrase)
                break 

        # Explain what is next
        self.say('Please play the I spy game with me.')
        self.say('I will guess %s times.' % tries)


    def waitForColor(self):
        color = None
        while not color:
        
            phrase = self.recognizeSpeech()
        
            # COLOR (NAME COMPLEMENT)
            for c in self.colors:
                if c in phrase:
                    color = c
                    break

            if not color:
                self.say("Sorry, but I'm only interested in playing the game.")
    
        print "The SLU found a color: %s " % (color)
        return color



    def doYouMean(self, obj):
        
        # chose response phrase
        phrases = [ 'Is it the %s?', 
                    'the %s?',
                    'mmmmm.    That %s?' ]
        phrase = phrases[ random.randint(0, len(phrases)-1) ]

        # response
        self.say(phrase % obj)
#        self.point(self.objects[obj])
        

    def letMeTryAgain(self):
        # chose response phrase
        phrases = [ 'Let me try again.', 
                    'Oh, but this time' ]
        phrase = phrases[ random.randint(0, len(phrases)-1) ]

        # response
        self.say(phrase)


    def repeat(self):
        self.say("Do you want to try again?")
        while True:
        
            phrase = self.recognizeSpeech()
            if 'yes' in phrase:
                return False
            
            elif 'no' in phrase:
                return True

            else:
                self.say("Sorry, but I did not understand you. Please say yes or no.")


    def goodbye(self):

        # chose response phrase
        phrases = [ 'Thank you for playing the game with me.', 
                    'Goodbye.',
                    'Bye bye.' ]
        phrase = phrases[ random.randint(0, len(phrases)-1) ]

        # response
        self.say(phrase)


    def searchColorInDB(self, color, _try):
        #Function which receive a color and an iteration and give back an object. E.g. "Which is the 
        # FIRST RED thing in the list?"
        #--> "it is the APPLE"
        
        # just get all colors in order
        colors  = [x[2] for x in self.db]

        assert color in colors, 'color unknown'
        
        # select the object based on the try
        indices = [i for i, x in enumerate(colors) if x == color]

        # select the name of the object
        return self.db[indices[_try]][1]


    def say(self, data):
        
        """based on http://stackoverflow.com/questions/17657103/how-to-play-wav-file-in-python"""
        
        # define stream chunk   
        chunk = 1024  
        
        # open a wav format music  
        f = wave.open(self.getWaveFile(data))  
    
        # instantiate PyAudio  
        p = pyaudio.PyAudio()  
        
        # open stream  
        stream = p.open(format   = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate     = int(f.getframerate() * self.speed),  
                        output   = True)  
        
        # read data  
        data = f.readframes(chunk)  
        
        # play stream  
        while data != '':  
            stream.write(data)  
            data = f.readframes(chunk)  
        
        # stop stream  
        stream.stop_stream()  
        stream.close()  
        
        # close PyAudio  
        p.terminate()      
    

    def getWaveFile(self, text):
        values = { 'INPUT_TYPE' :    'TEXT',
                   'AUDIO':          'WAVE_FILE',
                   'OUTPUT_TYPE':    'AUDIO',
                   'LOCALE':         self.locale,
                   'INPUT_TEXT':     text,
                   'VOICE':          self.voice }
    
        data        = urllib.urlencode(values)  
        req         = urllib2.Request(self.process_url, data)
        response    = urllib2.urlopen(req)
        return StringIO.StringIO(response.read())


if __name__ == '__main__':
    main(StateHandler)
