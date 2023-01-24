import threading
import RPi.GPIO as GPIO
import time

class Led(object):

    LED_OFF = 0
    LED_ON = 1
    LED_FLASHING = 2

    # the short time sleep to use when the led is on or off to ensure the led responds quickly to changes to blinking
    FAST_CYCLE = 0.05

    def __init__(self, led_pin, name):
        self.__name = name
        # create the semaphore used to make thread exit
        self.pin_stop = threading.Event()
        # the pin for the LED
        self.__led_pin = led_pin
        # initialise the pin and turn the led off
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__led_pin, GPIO.OUT)
        # the mode for the led - off/on/flashing
        self.__ledmode = self.LED_OFF
        GPIO.output(self.__led_pin, self.__ledmode)
        # make sure the LED is off (this also initialises the times for the thread)
        self.off()

    def __blink_pin(self, time_on, time_off, pin_stop):
        try:
            while not pin_stop.is_set():
                GPIO.output(self.__led_pin, GPIO.HIGH)
                time.sleep(time_on)
                GPIO.output(self.__led_pin, GPIO.LOW)
                time.sleep(time_off)
        except KeyboardInterrupt as e:
            self.off()
            GPIO.cleanup()
            return


    def blink(self, time_on=0.050, time_off=1):
        # blinking will start at the next first period
        # because turning the led on now might look funny because we don't know
        # when the next first period will start - the blink routine does all the
        # timing so that will 'just work'
        self.pin_stop.clear()
        if self.__ledmode == self.LED_FLASHING:
            return
        self.__ledmode = self.LED_FLASHING
        self.__time_on = time_on
        self.__time_off = time_off
        # create the thread, keep a reference to it for when we need to exit
        self.__thread = threading.Thread(name=self.__name,target=self.__blink_pin, args=(self.__time_on, self.__time_off, self.pin_stop))
        # start the thread
        self.__thread.start()

    def off(self):
        self.__ledmode = self.LED_OFF
        GPIO.output(self.__led_pin, self.__ledmode)

    def on(self):
        self.__ledmode = self.LED_ON
        GPIO.output(self.__led_pin, self.__ledmode)
    def stopBlink(self):
        # set the semaphore so the thread will exit after sleep has completed
        self.pin_stop.set()
        if hasattr(self, 'attr_name'):
            # wait for the thread to exit
            self.__thread.join()
    def reset(self):
        # set the semaphore so the thread will exit after sleep has completed
        self.pin_stop.set()
        # wait for the thread to exit
        self.__thread.join()
        # now clean up the GPIO
        GPIO.cleanup()
