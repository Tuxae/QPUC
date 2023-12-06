from buzzer import SuperArduino
import time

from playsound import playsound

super_arduino = SuperArduino('/dev/ttyACM0')


while True:
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
while True:
    time.sleep(1)
    board_mega.digital[13].write(0)
    time.sleep(1)
    board_mega.digital[13].write(1)