from buzzer import SuperArduino
from pyfirmata import Arduino, util
import time

from playsound import playsound

super_arduino = SuperArduino('/dev/ttyACM1')

super_arduino.turn_on_light()


super_arduino.turn_on_buzzer([False, False, True, False])

super_arduino.turn_on_light([False, False, True, False])


while True:
    res = super_arduino.get_winner()
    print(res)
    if res is not None:
        liste = [False for i in range(4)]
        liste[res] = True
        print(res, liste)
        super_arduino.turn_on_buzzer(liste)
        time.sleep(2)




while True:
    liste = super_arduino.get_value()
    print(liste)
    if max(liste) > 0.4:
        input()




super_arduino.list_buzzer[0].turn_on_light()

super_arduino.board.digital[4].write(1)



super_arduino.board.digital[7].write(1)









while False:
    super_arduino.get_value()
    time.sleep(1)



board = Arduino('/dev/ttyACM0')



board.digital[4].write(1)
board.digital[5].write(1)
board.digital[6].write(1)
board.digital[7].write(1)

board.digital[4].write(0)
board.digital[5].write(0)
board.digital[6].write(0)
board.digital[7].write(0)


board.digital[8].write(1)
board.digital[9].write(1)
board.digital[10].write(1)
board.digital[11].write(1)

board.digital[8].write(0)
board.digital[9].write(0)
board.digital[10].write(0)
board.digital[11].write(0)

it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()
board.analog[0].read()
board.analog[1].enable_reporting()
board.analog[1].read()
board.analog[2].enable_reporting()
board.analog[2].read()
board.analog[3].enable_reporting()
board.analog[3].read()

board.get_pin('a:0:i').read()

board_mega = Arduino('/dev/ttyACM0')
board_mega.digital[13].write(1)