import serial
import time

PORTA_ARDUINO = "COM3"
arduino = None

try:
    arduino = serial.Serial(PORTA_ARDUINO, 9600)
    time.sleep(2)
    print("Arduino conectado")
except Exception as e:
    print(e)

def enviar_comando(cmd):
    global arduino
    if arduino:
        arduino.write(cmd.encode())
        arduino.flush()
        print("Comando enviado:", cmd)
