####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
####################################################################################################
import StringIO
import urllib2
import urllib

import pyaudio    
import wave


class MaryTTS(object):
    
    
    def __init__(self):
        self.speed       = 1.0
        self.locale      = 'en_GB'
        self.voice       = 'dfki-poppy'
        self.process_url = 'http://127.0.0.1:59125/process'


    def say(self, text):
        
        """based on http://stackoverflow.com/questions/17657103/how-to-play-wav-file-in-python"""
        
        # define stream chunk   
        chunk = 1024  
        
        # open a wav format music  
        f = wave.open(self.getWaveFile(text))  
    
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
    
    
    def storeSpeech(self, text, filename):
        with open(filename, 'w') as f:
            f.write(self.getWaveFile(text))
