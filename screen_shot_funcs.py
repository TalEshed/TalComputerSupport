from PIL import ImageGrab, Image
import pygame

def image_screen_shot():
    # Takes  screen shot
    img = ImageGrab.grab()
    return img

def equal(image1, image2):
    """

    :param image1: The old image
    :param image2: The new image
    :return: Returns the bounding box of the difference between the two images
    """
    # Load the first image
    image1.load()
    # Load the second image
    image2.load()
    # The coordinates of the start and the end of the difference box
    coordinates = image1._new(image1.im.chop_difference(image2.im)).getbbox()
    # If the size is to close to the size of the screen send the whole screen
    if coordinates != None and coordinates[2] - coordinates[0] > 1200 and coordinates[3] - coordinates[1] > 700:
        coordinates = (0, 0, 1920, 1080)
    # Return the coordinates of the start and the end of the difference box

    return coordinates

def drew_image(image, width_image, height_image, coordinates, screen):
    """

    :param image:
    :param width_image:
    :param height_image:
    :param coordinates:
    :param screen:
    :return:
    """
    # Match the image by size and color
    img = pygame.image.frombuffer(image, (width_image, height_image), "RGB")
    # Put the image on the screen
    screen.blit(img, coordinates)
    # Update the screen
    pygame.display.update()

def paste_on_img(img2, img1, coordinates):
    """

    :param img2:
    :param img1:
    :param coordinates:
    :return:
    """
    # Paste image 2 on image 1
    Image.Image.paste(img2, img1, (coordinates[0], coordinates[1]))
