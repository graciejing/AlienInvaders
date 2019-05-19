"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special class
for it. Unless you need something special for your extra gameplay features, Ship
and Aliens could just be an instance of GImage that you move across the screen.
You only need a new class when you add extra features to an object. So
technically Bolt, which has a velocity, is really the only model that needs to
have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the objects,
and you might want to add a custom initializer.  With that said, feel free to
keep the pass underneath the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Authors: Zain Khoja (znk4), Gracie Jing (kgj7)
Date: May 7, 2019
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship
    just means changing the x attribute (which you can do directly), you want
    to prevent the player from moving the ship offscreen.  This is an ideal
    thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not
    require this. You could put this method in Wave if you wanted to.  But the
    advantage of putting it here is that Ships and Aliens collide with different
    bolts.  Ships collide with Alien bolts, not Ship bolts. And Aliens collide
    with Ship bolts, not Alien bolts. An easy way to keep this straight is for
    this class to have its own collision method.

    However, there is no need for any more attributes other than those inherited
    by GImage. You would only add attributes if you needed them for extra
    gameplay features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    INSTANCE ATTRIBUTES:
        x:         [int] contains horizontal location of the Ship
        y:         [int] contains vertical location of the Ship
        width:     [int] contains width of the Ship
        height:    [int] contains height of the Ship
        source:    [str] contains Ship image source
        _shipBolt:  sound of player ship shooting a bolt
        _shipDeath: sound of player ship blowing up
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShipX(self):
        """
        Returns x-coordinate of current Ship object.
        """
        return self.x

    def setShipX(self, ship_x):
        """
        Sets x-coordinate of current Ship object.

        Parameter ship_x: the Ship's x-coordinate to change to
        Precondition: ship_x is an integer
        """
        self.x = ship_x

    def getShipY(self):
        """
        Returns y-coordinate of the current Ship object.
        """
        return self.y

    def setShipY(self, ship_y):
        """
        Sets y-coordinate of current Ship object.

        Parameter ship_y: the Ship's y-coordinate to change to
        Precondition: ship_y is an integer
        """
        self.y = ship_y

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, ship_x, ship_y, ship_w, ship_h, ship_img):
        """
        Initializes an Ship object.

        The object inherits values from GImage unless otherwise specified.

        OBJECT ATTRIBUTES:
            ship_x:     horizontal location of the Ship
            ship_y:     vertical location of the Ship
            ship_w:     width of the image
            ship_h:     height of the image
            ship_img:   file of the Ship image
        """
        super().__init__(x = ship_x, y = ship_y, width = ship_w,
        height = ship_h, source = ship_img)
        self._shipBolt = Sound('pew1.wav')
        self._shipDeath = Sound('blast1.wav')

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def moveShip(self, input):
        """
        Animates ship moving with user input.

        The ship will move left and right according to user input until it hits
        the edge of the screen.

        Parameter input: an input passed down from invaders
        Precondition: a valid input
        """
        min = SHIP_WIDTH/2
        max = GAME_WIDTH - (SHIP_WIDTH/2)
        left_pressed = input.is_key_down('left') and self.x >= min
        if left_pressed:
            self.x -= SHIP_MOVEMENT

        right_pressed = input.is_key_down('right') and self.x <= max
        if right_pressed:
            self.x += SHIP_MOVEMENT

    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the alien and collides with this
        ship

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        return not bolt.isPlayerBolt() and \
        (self.contains((bolt.x-BOLT_WIDTH/2, bolt.y+BOLT_HEIGHT/2)) or \
        self.contains((bolt.x+BOLT_WIDTH/2, bolt.y+BOLT_HEIGHT/2)) or \
        self.contains((bolt.x-BOLT_WIDTH/2, bolt.y-BOLT_HEIGHT/2)) or \
        self.contains((bolt.x+BOLT_WIDTH/2, bolt.y-BOLT_HEIGHT/2)))

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def shipBoltPlay(self):
        """
        Plays the player bolt sound.
        """
        self._shipBolt.play()

    def shipDeathPlay(self):
        """
        Plays the player death sound.
        """
        self._shipDeath.play()


class Alien(GSprite):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not
    require this.  You could put this method in Wave if you wanted to.  But the
    advantage of putting it here is that Ships and Aliens collide with different
    bolts. Ships collide with Alien bolts, not Ship bolts.  And Aliens collide
    with Ship bolts, not Alien bolts. An easy way to keep this straight is for
    this class to have its own collision method.

    However, there is no need for any more attributes other than those inherited
    by GImage. You would only add attributes if you needed them for extra
    gameplay features (like giving each alien a score value). If you add
    attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    INSTANCE ATTRIBUTES:
        x:           [int] contains horizontal location of the Alien
        y:           [int] contains vertical location of the Alien
        width:       [int] contains width of the Alien
        height:      [int] contains height of the Alien
        source:      [str] contains Alien image source
        _type:       [int] contains type of Alien based on source image
        _alienBolt:  sound of alien shooting a bolt
        _alienDeath: sound of alien blowing up
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAlienX(self):
        """
        Returns x-coordinate of current Alien object.
        """
        return self.x

    def setAlienX(self, alien_x):
        """
        Sets x-coordinate of current Alien object.

        Parameter alien_x: the Alien's x-coordinate to change to
        Precondition: alien_x is an integer
        """
        self.x = alien_x

    def getAlienY(self):
        """
        Returns y-coordinate of the current Alien object.
        """
        return self.y

    def setAlienY(self, alien_y):
        """
        Sets y-coordinate of current Alien object.

        Parameter alien_y: the Alien's y-coordinate to change to
        Precondition: ship_y is an integer
        """
        self.y = alien_y

    def getType(self):
        """
        Returns type (int) of Alien based on source image.
        """
        return self._type

    def setType(self, alien_type):
        """
        Sets alien's type value based on source image.

        Parameter alien_type: the type of Alien based on the source image
        Precondition: alien_type is an integer
        """
        self._type = alien_type

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, alien_x, alien_y, alien_w, alien_h, alien_img, \
    alien_type):
        """
        Initializes an Alien object.

        The object inherits values from GImage unless otherwise specified.

        OBJECT ATTRIBUTES:
            alien_x:    horizontal location of the Alien
            alien_y:    vertical location of the Alien
            alien_w:    width of the image
            alien_h:    height of the image
            alien_img:  file of the Alien image
        """
        super().__init__(x = alien_x, y = alien_y, width = alien_w,
        height = alien_h, source = alien_img, format = (3,2))
        self._type = alien_type
        self._alienBolt = Sound('pew2.wav')
        self._alienDeath = Sound('pop2.wav')

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this
        alien

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        return bolt.isPlayerBolt() and \
        (self.contains((bolt.x-BOLT_WIDTH/2,bolt.y+BOLT_HEIGHT/2)) or \
        self.contains((bolt.x+BOLT_WIDTH/2, bolt.y+BOLT_HEIGHT/2)) or \
        self.contains((bolt.x-BOLT_WIDTH/2, bolt.y-BOLT_HEIGHT/2)) or \
        self.contains((bolt.x+BOLT_WIDTH/2, bolt.y-BOLT_HEIGHT/2)))

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def alienBoltPlay(self):
        """
        Plays the alien bolt sound.
        """
        self._alienBolt.play()

    def alienDeathPlay(self):
        """
        Plays the alien death sound.
        """
        self._alienDeath.play()


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because
    we need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set the
    starting velocity. This __init__ method will need to call the __init__ from
    GRectangle as a helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt
    by adding the velocity to the y-position.  However, the getter allows Wave
    to do this on its own, so this method is not required.

    INSTANCE ATTRIBUTES:
        x:         [int] contains horizontal location of the Bolt
        y:         [int] contains vertical location of the Bolt
        width:     [int] contains width of the Bolt
        height:    [int] contains height of the Bolt
        _velocity:  [int or float] the velocity in y direction
        fillcolor: [str] contains the Bolt color

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBoltY(self):
        """
        Returns y-coordinate of the current Bolt object.
        """
        return self.y

    def setBoltY(self, bolt_y):
        """
        Sets y-coordinate of current Bolt object.

        Parameter bolt_y: the Bolt's y-coordinate to change to
        Precondition: bolt_y is an integer
        """
        self.y = bolt_y

    def getBoltVelocity(self):
        """
        Returns velocity of the current Bolt object.
        """
        return self._velocity

    def setBoltVelocity(self, bolt_sp):
        """
        Sets velocity of current Bolt object.

        Parameter bolt_sp: the Bolt's velocity
        Precondition: bolt_sp is an integer or float
        """
        self._velocity = bolt_sp

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, bolt_x, bolt_y, bolt_w, bolt_h, bolt_sp, bolt_color):
        """
        Initializes an Bolt object.

        The object inherits values from GRectangle unless otherwise specified.

        OBJECT ATTRIBUTES:
            bolt_x:     horizontal location of the Bolt
            bolt_y:     vertical location of the Bolt
            bolt_w:     width of bolt
            bolt_h:     height of the bolt
            bolt_sp:    velocity of the bolt
        """
        super().__init__(x = bolt_x, y = bolt_y, width = bolt_w,
        height = bolt_h, fillcolor = bolt_color)
        self._velocity = bolt_sp

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns True if Bolt is fired by the player.
        """
        return self._velocity > 0

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
