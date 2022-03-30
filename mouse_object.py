import mouse

class Mouse:
    def __init__(self, mouse_q):
        """

        :param mouse_q:
        """
        self.mouse_q = mouse_q


    def listener_button_click(self):
        """

        :return:
        """
        # make a listener when left button is clicked and put the value in the queue and the position of the mouse
        mouse.on_click(lambda: self.mouse_q.put(['left', mouse.get_position()]))
        # make a listener when right button is clicked and put the value in the queue and the position of the mouse
        mouse.on_right_click(lambda: self.mouse_q.put(['right', mouse.get_position()]))
        # make a listener when middle button is clicked and put the value in the queue and the position of the mouse
        mouse.on_middle_click(lambda: self.mouse_q.put(['middle', mouse.get_position()]))

    def mouse_click_par(self):
        """

        :return:
        """
        parameters_list = self.mouse_q.get()
        click = parameters_list[0]
        x = parameters_list[1][0]
        y = parameters_list[1][1]
        return [x, y, click]



def mouse_click(x, y, click):
    """

    :param x:
    :param y:
    :param click:
    :return:
    """
    mouse.move(x, y)
    mouse.click(click)