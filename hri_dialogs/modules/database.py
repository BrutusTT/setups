####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
####################################################################################################


class Database(object):
    """ The Database class provides a container for the relation between marker IDs, object names 
        and colors.
    """
    
    
    def __init__(self, filename):
        
        
        # read database
        with open(filename, 'r') as f:

            # remove header line
            # remove windows line ending character
            data         = [x.replace('\r', '')  for x in f.read().split('\n')[1:]]

            # split lines into entries and only keep entries that have 3 elements
            self.db      = [x.split(',') for x in data if len(x.split(',')) == 3]
            self.db      = [(int(oid), name, color) for oid, name, color in self.db]

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


    def getObjectCountByColor(self, color):
        counter = 0
        for _, _, obj_color in self.db:
            if obj_color == color:
                counter += 1
        return counter


    def searchObjectByColor(self, color, _try):
        """  The function receives a color and an iteration and gives corresponding object name 
             back, e.g.:
             - "Which is the FIRST RED thing in the list?"
             --> "apple"

        @param color - string
        @param _try  - integer
        @return string - object name
        """
        assert isinstance(color, type('')), 'The color attribute needs to be a string.'
        assert isinstance(_try,  int),      '_try needs to be an integer'
        
        # just get all colors in order
        colors  = [x[2] for x in self.db]
        assert color in colors, 'The word %s was not found in the available colors' % color
        
        # select the object based on the try
        indices = [i for i, x in enumerate(colors) if x == color]
        assert _try < len(indices), 'You only got %s objects but its already your %s try.' % (_try, len(indices)) 

        # select the name of the object
        return self.db[indices[_try]][1]
