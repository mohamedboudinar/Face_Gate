import RPi.GPIO as GPIO
import time
import threading

class StepperMotor:
    def __init__(self, pins, delay=0.002, steps_per_rev=4096):
        """
        Initialize the stepper motor with the given GPIO pins and settings.

        :param pins: List of GPIO pins connected to the stepper motor driver.
        :param delay: Delay between steps to control the speed of the motor.
        :param steps_per_rev: Number of steps for a full revolution.
        """
        self.pins = pins
        self.delay = delay
        self.steps_per_rev = steps_per_rev
        self.current_step = 0
        self.ONE_STEP = 1
        self.MAX_NUM_STEPS = 8
        self.setup_gpio()

    def setup_gpio(self):
        """Set up the GPIO pins."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def cleanup_gpio(self):
        """Clean up the GPIO pins."""
        for pin in self.pins:
            GPIO.output(pin, False)
        GPIO.cleanup()

    def step_forward(self, steps=1):
        """Move the motor forward by the specified number of steps."""
        for _ in range(steps):
            self.current_step += self.ONE_STEP
            self._move(self.current_step % self.MAX_NUM_STEPS)

    def step_backward(self, steps=1):
        """Move the motor backward by the specified number of steps."""
        for _ in range(steps):
            self.current_step -= self.ONE_STEP
            self._move(self.current_step % self.MAX_NUM_STEPS)

    def rotate(self, revolutions=1):
        """Rotate the motor by the specified number of revolutions."""
        steps = int(revolutions * self.steps_per_rev)
        if steps > 0:
            self.step_forward(steps)
        else:
            self.step_backward(abs(steps))

    def _move(self, step):
        """Private method to energize the motor coils for the specified step."""
        seq = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]
        
        for pin in range(4):
            GPIO.output(self.pins[pin], seq[step][pin])
        time.sleep(self.delay)

    def __del__(self):
        """Clean up the GPIO pins when the object is deleted."""
        self.cleanup_gpio()

def usage_stepper_1():
    motor_pins = [17, 18, 27, 22]
    motor = StepperMotor(motor_pins)
    while True:
        motor.rotate(1)
        time.sleep(1)
        motor.rotate(-1)

def usage_stepper_2():
    motor_pins = [23, 24, 25, 4]
    motor = StepperMotor(motor_pins)
    while True:
        motor.rotate(1)
        time.sleep(1)
        motor.rotate(-1)

def thread_function1():
    usage_stepper_1()

def thread_function2():
    usage_stepper_2()

def main():
    thread1 = threading.Thread(target=thread_function1)
    thread2 = threading.Thread(target=thread_function2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
