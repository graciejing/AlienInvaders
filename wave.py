"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the
Alien Invaders game.  Instances of Wave represent a single wave.  Whenever you
move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue.  If you do not know, ask on Piazza and we will answer.

Authors: Zain Khoja (znk4), Gracie Jing (kgj7)
Date: May 7, 2019
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you should create a NEW instance of Wave
    (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update. See subcontrollers.py from Lecture 24 for an example. This class
    will be similar to than one in how it interacts with the main class
    Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   [Ship object] the player ship to control
        _aliens: [2D list of Alien or None] the 2d list of aliens in the wave
        _bolts:  [list of Bolt]the laser bolts currently on screen
        _dline:  [GPath object] the defensive line being protected
        _lives:  [int >= 0] the number of lives left
        _time:   [number >= 0] the amount of time since the last Alien "step"

    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in class Invaders. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Invaders.  Only add the
    getters and setters that you need for Invaders. You can keep everything
    else hidden.

    You may change any of the attributes above as you see fit. For example, may
    want to keep track of the score.  You also might want some label objects to
    display the score and number of lives. If you make changes, please list the
    changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _direction:    [str] tracks whether aliens are moving left or right
    _go_down:      [bool] tracks whether the aliens have moved down
    _last:         [bool] tracks if 's' was pressed during the last frame
    _steps:        [int] number between 1 and BOLT_RATE that represents
    _result:       [int] tracks if player is playing (0), lost (1), won (2)
    _speed:        [int] tracks the current threshhold of _time for each step
    _mute:         [bool] determines whether sound is on or off
    _score:        [int] tracks the player's score
    _scoreLabel:   [GLabel object] prints the player's score on the screen
    _spriteList:   [list of GSprite objects] sprites for Alien animation
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns current Ship object.
        """
        return self._ship

    def setShip(self, new_ship):
        """
        Sets current Ship object.

        Parameter new_ship: a new Ship object
        Precondition: new_ship is a valid Ship
        """
        self._ship = new_ship

    def getLives(self):
        """
        Returns current number of lives.
        """
        return self._lives

    def getResult(self):
        """
        Returns whether the player has lost or not.
        """
        return self._result

    def getScore(self):
        """
        Returns the current score of the wave.
        """
        return self._score

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, num_waves, wave_score):
        """
        Initializes an Wave object.

        OBJECT ATTRIBUTES
            num_waves:  [int] contains the wave number
            wave_score: [int] contains the player's score
        """
        self._ship = Ship(GAME_WIDTH/2, SHIP_BOTTOM, SHIP_WIDTH, SHIP_HEIGHT,
        'ship.png')
        self._aliens = self._populate_aliens()
        self._bolts = []
        self._dline = GPath(points=[0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE],
        linewidth = 1, linecolor = [0.5, 0.5, 0.5, 1.0])
        self._lives = SHIP_LIVES
        self._time = ALIEN_SPEED
        self._direction = 'right'
        self._go_down = False
        self._last = False
        self._steps = random.randint(0, BOLT_RATE)
        self._result = 0
        if num_waves != 0:
            self._speed = ALIEN_SPEED/(num_waves+1)
        else:
            self._speed = ALIEN_SPEED
        self._mute = 1
        self._score = wave_score
        self._scoreLabel = GLabel(text="Score: " + str(self._score),
        font_name = 'Arcade.ttf', font_size = 36, linecolor = 'white',
        x = ALIEN_H_SEP+100, y = GAME_HEIGHT-ALIEN_V_SEP-25)

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Animates a single frame in the game.

        Parameter input: an input passed down from invaders
        Precondition: a valid input

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._ship != None:
            self._ship.moveShip(input)
        self._alienMove(dt)
        self._fireBolt(input)
        self._alienBolts()
        self._detectCollisions()
        self._checkResults()
        self._changeVolume(input)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the game objects to the view.

        Parameter view: the game view, used in drawing
        Precondition: a valid view
        """
        if self._ship != None:      #Draw ship
            self._ship.draw(view)
        for row in self._aliens:    #Draw aliens
            for alien in row:
                if alien != None:
                    alien.draw(view)
        self._dline.draw(view)      #Draw defense line
        for b in self._bolts:       #Draw bolts
            b.draw(view)
        #Draw score
        if self._scoreLabel != None:
            self._scoreLabel.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def _detectCollisions(self):
        """
        Detects if an alien bolt has collided with the ship.
        """
        for b in self._bolts:
            for i in range(0, len(self._aliens)):
                for j in range(0, len(self._aliens[i])):
                    if self._aliens[i][j] != None:
                        if self._aliens[i][j].collides(b):
                            if self._mute == 1:
                                self._aliens[i][j].alienDeathPlay()
                            #Update score
                            self._score += self._aliens[i][j].getType() * 100
                            self._scoreLabel.text = "Score: " + str(self._score)
                            self._aliens[i][j] = None
                            self._bolts.remove(b)
                            #Dynamically speed up waves
                            self._speed *= 0.97
            if self._ship != None:
                if self._ship.collides(b):
                    if self._mute == 1:
                        self._ship.shipDeathPlay()
                    self._ship = None
                    self._lives -= 1
                    self._bolts.clear()

    #HELPER METHODS FOR WAVE
    def _populate_aliens(self):
        """
        Populate a 2D array with Alien objects.
        """
        thanos_army = []
        alien_x = ALIEN_H_SEP + (ALIEN_WIDTH/2)
        alien_y = GAME_HEIGHT - (ALIEN_CEILING + (ALIEN_HEIGHT/2) + \
        (ALIEN_HEIGHT*ALIEN_ROWS) + (ALIEN_V_SEP*(ALIEN_ROWS-1)))
        image_index = 0
        row_counter = 0
        for row in range(ALIEN_ROWS):
            temp_row = []
            for column in range(ALIENS_IN_ROW):
                temp_row.append(Alien(alien_x, alien_y, ALIEN_WIDTH,
                ALIEN_HEIGHT, ALIEN_IMAGES[image_index], image_index+1))
                alien_x += (ALIEN_H_SEP + ALIEN_WIDTH)
            thanos_army.append(temp_row)
            #Reset the x value to the beginning of the row
            alien_x = ALIEN_H_SEP + (ALIEN_WIDTH/2)
            #Increment the y value upwards
            alien_y += (ALIEN_V_SEP + ALIEN_HEIGHT)
            #Ensure 2 rows of aliens per image
            row_counter += 1
            if row_counter == 2:
                image_index += 1
                if image_index >= len(ALIEN_IMAGES):
                    image_index = 0
                row_counter = 0
        return thanos_army

    def _determineDirection(self):
        """
        Determines the direction of the alien wave.
        """
        min_x = GAME_WIDTH
        max_x = 0
        #Find leftmost x value
        for row in self._aliens:
            for a in row:
                if a != None:
                    if a.getAlienX() < min_x:
                        min_x = a.getAlienX()
                    if a.getAlienX() > max_x:
                        max_x = a.getAlienX()
        #Determine direction
        if max_x >= GAME_WIDTH-ALIEN_H_SEP-ALIEN_WIDTH/2:
            self._direction = 'left'
        if min_x <= ALIEN_H_SEP+ALIEN_WIDTH/2:
            self._direction = 'right'

    def _alienMove(self, dt):
        """
        Moves each Alien in _alien in a certain direction.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        start_direction = self._direction
        self._determineDirection()
        #Check for change in direction
        if start_direction != self._direction:
            self._go_down = True
        #Walk the aliens
        if self._time >= self._speed:
            if self._go_down == True:
                self._go_down = self._bustDown()
            else:
                for row in self._aliens:
                    for a in row:
                        if a != None:
                            if self._direction == 'right':
                                a.setAlienX(a.getAlienX() + ALIEN_H_WALK)
                            if self._direction == 'left':
                                a.setAlienX(a.getAlienX() - ALIEN_H_WALK)
                            #Animate aliens
                            a.frame = (a.frame+1) % 2
            self._time = 0
            self._steps -= 1
        else:
            self._time += dt

    def _bustDown(self):
        """
        Moves an Alien down.
        """
        for row in self._aliens:
            for a in row:
                if a != None:
                    a.setAlienY(a.getAlienY() - ALIEN_V_WALK)
        return False

    def _fireBolt(self, input):
        """
        Creates a new Bolt object and fires it from the ship.

        This method also checks to see if the ship has already shot and has a
        bolt on screen. If there is a bolt, the ship must wait to shoot. When
        the bolt flies off screen, a new bolt may be fired.

        Parameter input: an input passed down from invaders
        Precondition: a valid input
        """
        pew = input.is_key_down('spacebar')
        if self._ship != None:
            bolt_x = self._ship.getShipX()
            bolt_y = self._ship.getShipY() + SHIP_HEIGHT/2 + BOLT_HEIGHT/2
            safety = False
            #Check if there is already a player bolt
            for b in self._bolts:
                if b.isPlayerBolt():
                    safety = True
            #Press 'spacebar' to shoot
            if pew and not self._last and not safety:
                if self._mute == 1:
                    self._ship.shipBoltPlay()
                self._bolts.append(Bolt(bolt_x, bolt_y, BOLT_WIDTH,
                BOLT_HEIGHT, BOLT_SPEED, 'green'))
        for b in self._bolts:
            b.setBoltY(b.getBoltY() + b.getBoltVelocity())
            if (b.getBoltY() - BOLT_HEIGHT/2) >= GAME_HEIGHT or \
            (b.getBoltY() + BOLT_HEIGHT/2) <= 0:
                self._bolts.remove(b)
        self._last = pew

    def _alienBolts(self):
        """
        Creates a new Bolt object and fires from a random alien.
        """
        #Find random nonempty column
        rand_col = random.randint(0, ALIENS_IN_ROW-1)
        while rand_col == None:
            rand_col = random.randint(0, ALIENS_IN_ROW-1)
        #Find bottommost alien in column
        bottom_index = 0
        shooter = self._aliens[bottom_index][rand_col]
        while shooter == None and bottom_index < ALIEN_ROWS:
            shooter = self._aliens[bottom_index][rand_col]
            bottom_index += 1
        #Fire the bolt from the shooter
        if shooter != None and self._time >= self._speed:
            bolt_x = shooter.getAlienX()
            bolt_y = shooter.getAlienY() - ALIEN_HEIGHT/2 - BOLT_HEIGHT/2
            if self._steps <= 1:
                if self._mute == 1:
                    shooter.alienBoltPlay()
                self._bolts.append(Bolt(bolt_x, bolt_y, BOLT_WIDTH,
                BOLT_HEIGHT, -BOLT_SPEED, 'red'))
                self._steps = random.randint(0, BOLT_RATE)

    def _checkResults(self):
        """
        Checks the state of the game between playing, won, and lost.
        """
        #Check loss conditions
        if self._lives <= 0:
            self._result = 1
        for row in self._aliens:
            for a in row:
                if a != None:
                    if a.getAlienY() - ALIEN_HEIGHT/2 < DEFENSE_LINE:
                        self._result = 1
        #Check win conditions
        allNone = True
        for row in self._aliens:
            for a in row:
                if a != None:
                    allNone = False
        if allNone:
            self._result = 2

    def _changeVolume(self, input):
        """
        Allows the user to mute and unmute the game sounds.
        """
        if input.is_key_down('m') and self._mute == 1:
            self._mute = 0
        elif input.is_key_down('p') and self._mute == 0:
            self._mute = 1


    # HELPER METHODS FOR THE STATES GO HERE
