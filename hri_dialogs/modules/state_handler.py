####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
####################################################################################################
from thread import start_new_thread
from spy.modules.BaseModule   import BaseModule, main
import time

import yarp
import speech_recognition as sr

from dialog   import Dialog
from database import Database
from mary_tts import MaryTTS

r = sr.Recognizer()
m = sr.Microphone()


class StateHandler(BaseModule):
    """ The StateHandler class provides a yarp module to that handles the state of an HRI task.
    """

    def startLog(self):
        with open('state_handler_%s.log' % time.time(), 'w') as f:
            self.log = f
    

    def __del__(self):
        if hasattr(self, 'log') and self.log:
            self.log.close()
    

    def writeAudio(self, data):
        filename = 'speech_input_%s.data' % time.time()
        self.log.write('%s\tspeech_input\t%s' % (time.time(), filename) )
        with open(filename, 'w') as f:
            f.write(data)


    def configure(self, rf):
        BaseModule.configure(self, rf)
        self.startLog()
    
        self.speechPort  = self.createOutputPort('speech')
        self.pointPort   = self.createOutputPort('point')
#        self.textPort    = self.createInputPort('text')
        self.markerPort  = self.createInputPort('marker', 'buffered')

        self.connect(self.pointPort.getName(), '/NaoController/rpc')

        # Load the TTS engine
        self.tts         = MaryTTS()

        # Load the object database
        self.db = Database('Data_base_fruits.csv')

        # Load the dialog
        self.dialog = Dialog('complex')

        return True
    
    
#     def updateModule(self):
#         
#         bottle = self.textPort.read()
#         if bottle:
#             print bottle.toString()
#         
#         return BaseModule.updateModule(self)

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
    

    def point(self, args):
        bottle  = yarp.Bottle()
        bottle.clear()

        mx, my = args[1]

        y = ((mx / 240.0) - 1.0) * 0.2
        z = (my / 640.0) * -0.4

        bottle.addString('point')
        bottle.addString('left')
        bottle.addDouble(0.2)
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
                        self.log.write('%s\t%s' % (time.time(), "You said {}".format(a).encode("utf-8")))
                        break
                    else:  # this version of Python uses unicode for strings (Python 3+)
                        print("You said {}".format(a))
                        self.log.write('%s\t%s' % (time.time(), "You said {}".format(a)))
                        break
            except sr.UnknownValueError:
                        self.tts.say("Oops! Did not catch that")
            except sr.RequestError as e:
                        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

                        # self.tts.say("Your text is : "+a)#verification 1
                        # self.tts.say("SLU will output a semantics for your text.")

        new_sentence = a.split()  # divide a big string in several little string divided by a space (=don't work for composed words). b is a list of little strings.
        print(new_sentence)  # verification 
        return new_sentence


    def findObjects(self):
        
        self.connect('/HCMarker/markers:o', self.markerPort.getName())
        
        #
        # Gather Object Locations
        #
        start   = time.time()
        markers = {}
        while time.time() - start < 0.5:
            
            bottle = self.markerPort.read()
            if bottle:
                count = bottle.get(0).asInt()
                if count > 0:
                    # get the lists of markers from the bottle
                    data_list = bottle.get(1).asList()             
                    # iterate over all elements in data and retrieve the information
                    for idx in range(count):
                        # get the information for one marker
                        marker_info = data_list.get(idx).asList()          
                        # information is put into a dictionary
                        markers[marker_info.get(0).asInt()] = (marker_info.get(1).asInt(), marker_info.get(2).asInt())                
                
        yarp.Network.disconnect('/HCMarker/markers:o', self.markerPort.getName())
            
        # { <object id> : [<x-location>, <y-location>] }
        foundObjects = markers

        # { <object name>: [ <color>, [<x-location>, <y-location>] ] }
        self.objects = {}
        for oid, name, color in self.db.db:
            if oid in foundObjects:
                self.objects[name] = [color, foundObjects[oid]]
                print name

        self.db.setVisibleObjects(self.objects.keys())  

    def start(self):

        # MESSAGE DE DEPART
        self.say('start')
        
        #///////////////////////////////////////////////////////////////////////////////////////////
        #/                                         MAIN PROGRAM                                    /
        #///////////////////////////////////////////////////////////////////////////////////////////

        # Greeting*********************************************
        self.listenFor(['hello' , 'morning' , 'hi'], success = 'greeting')

        # Explain what is next
        self.say('explain')

        # program stop when stop == True
        stop = False   
        while not stop:

        # ACTIONS#############################################################################

            self.findObjects()

            # Wait for a color in the sentence **************************************
            color = None
            while not color:
                color = self.listenFor(self.db.colors, fail = 'asr_failed')
        
            print "The SLU found a color: %s " % (color)
            tries  = self.db.getObjectCountByColor(color)
            answer = ''

            for _try in range(tries):
            
                # Question processing**************************
                obj   = self.db.searchObjectByColor(color, _try)
                start_new_thread(self.point, (self.objects[obj], ))
                self.say('refere_to', obj = obj)
                time.sleep(2)
    
                answer = self.recognizeSpeech()
    
                if 'yes' in answer:
                    self.say('success')
                    break
                            
                elif 'no' in answer:
                    self.say('failed') 


            # after n tries
            if 'no' in answer:
                self.tts.say("Your are cheating!")
                time.sleep(0.5)
                self.tts.say("Which one is it?")
                _ = self.recognizeSpeech()
                self.tts.say('Ah, I see.')

            stop = self.repeat()
                
        # Leave********************************************
        self.say('goodbye')


    def repeat(self):
        self.say('try_again')
        while True:
        
            phrase = self.recognizeSpeech()
            if 'yes' in phrase:
                return False
            
            elif 'no' in phrase:
                return True

            else:
                self.say('asr_failed')


    

    def listenFor(self, trigger, success = None, fail = None):

        phrase = self.recognizeSpeech()
        for x in trigger:
            if x in phrase:
                if success:
                    self.say(success)
                return x

        if fail:
            self.say(fail)



    def say(self, phrase, **kwargs):
        """ This method fetches a phrase from the dialog and if one was found it will be handed over
            to the TTS. 
            
            Additional named arguments are can be used to fill slots.
            
        @param string - phrase as defined by the dialog
        """
        speech = self.dialog.response(phrase)
        if speech:
            if '%' in speech:
                speech = speech % (kwargs)
            self.log.writeln('%s\t%s' % (time.time(), speech))
            self.tts.say(speech)



if __name__ == '__main__':
    main(StateHandler)
