import keyboard

class Keyboard:
    def __init__(self, keyboard_q):
        self.keyboard_q = keyboard_q

    def keyboard_log(self):
        """

        :return: Put all pressed keys in queue
        """
        # log all pressed keys
        keyboard.on_release(lambda letter: self.keyboard_q.put(letter.name))

    def keyboard_par(self):
        letter = self.keyboard_q.get()
        return letter


def keyboard_press(event):
    """

    :param event:
    :return:
    """
    keyboard.send(event)