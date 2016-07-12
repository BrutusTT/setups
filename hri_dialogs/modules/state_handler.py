####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
####################################################################################################
from pyNAO.BaseModule   import BaseModule, main


class StateHandler(BaseModule):
    """ The NaoController class provides a yarp module to control the Nao robot.
    """

    def respond(self, command, reply):
        """ This is the respond hook method which gets called upon receiving a bottle via RPC port.

        @param command - input bottle
        @param reply - output bottle
        @return boolean
        """
        reply = 'nack'

        if command.get(0).toString() == 'point':

            arm   = command.get(1).toString()

            if arm not in ['left', 'right']:
                reply += ' message format for point: point <"left"|"right"> (x y z)'

            else:
                _list = command.get(2).asList()
                xyz   = [ _list.get(0).asDouble(), 
                          _list.get(1).asDouble(),
                          _list.get(2).asDouble() ] 
                self.nao.point('LArm' if arm == 'left' else 'RArm', xyz)
                reply = 'ack'

        elif command.get(0).toString() == 'look':
                _list = command.get(1).asList()
                xyz = [ _list.get(0).asDouble(), 
                        _list.get(1).asDouble(),
                        _list.get(2).asDouble(),
                        ] 
                
                self.nao.look(xyz)
                reply = 'ack'



        # reply with success
        reply.addString(reply)
        return True


if __name__ == '__main__':
    main(StateHandler)
