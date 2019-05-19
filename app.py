"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders
application. There is no need for any additional classes in this module. If you
need more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

Authors: Zain Khoja (znk4), Gracie Jing (kgj7)
Date: May 7, 2019
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when
    the game started, paused, completed, etc. It keeps track of that in an
    attribute called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
                STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships
                and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for
    the method update.

    You may have more attributes if you wish (you might want an attribute to
    store any score across multiple waves). If you add new attributes, they need
    to be documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    INSTANCE ATTRIBUTES:
        _last:  [bool] True if 's' was pressed during the last frame, False
                otherwise
        _prev:  [int] contains the previous state
        _level: [int] contains the number of waves completed
        _score: [int] contains the current score of the game
    """

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the game
        is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        #Initializing Game State
        self._state = STATE_INACTIVE
        self._wave = None
        self._text = GLabel(\
        text="Press 'S' to Play\n'M' to mute // 'P' to unmute",
        font_name = 'Arcade.ttf', font_size = 48, linecolor = 'white',
        x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
        self._prev = self._state
        self._last = False
        self._level = 0
        self._score = 0

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper. We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game. It
        displays a simple message on the screen. The application remains in this
        state so long as the player never presses a key.  In addition, this is
        the state the application returns to when the game is over (all lives
        are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the
        screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class should
        have an update() method, just like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the
        game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one
        animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you
        should describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        #Process the states. Send to helper methods.
        if self._state == STATE_INACTIVE:
            self._dismissWelcome()
        elif self._state == STATE_NEWWAVE:
            self._createWave()
        elif self._state == STATE_ACTIVE:
            self._wave.update(self.input, dt)
            self._didLoseLife()
            self._isGameOver()
        elif self._state == STATE_PAUSED:
            self._gamePaused()

        #Update previous state
        self._prev = self._state

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw
        a GObject, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to class
        Wave. We suggest the latter. See the example subcontroller.py from
        class.
        """
        #Draw background color
        GRectangle(width = GAME_WIDTH, height = GAME_HEIGHT, x = GAME_WIDTH/2,
        y = GAME_HEIGHT/2, fillcolor = 'black').draw(self.view)

        #Draw alien wave, ship, and defense line
        if self._wave != None:
            self._wave.draw(self.view)

        #Draw start text
        if self._text != None:
            self._text.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _dismissWelcome(self):
        """
        Dismisses the welcome screen text when the player presses 's'.
        """
        #Dismissing the Welcome Screen
        curr_keys = self._input.is_key_down('s')
        #Only change if we pressed keys THIS animation frame
        if curr_keys and not self._last:
            self._state = STATE_NEWWAVE
            self._text = None
        self._last = curr_keys

    def _createWave(self):
        """
        Creates a new Wave with the player's level and score. Then sets the
        state to STATE_ACTIVE.
        """
        self._wave = Wave(self._level, self._score)
        self._state = STATE_ACTIVE

    def _didLoseLife(self):
        """
        Checks to see if the player still has remaining lives after dying. If
        there are remaining lives, displays text and pauses the game.
        """
        if self._wave.getShip() == None and self._wave.getLives() > 0:
            self._text = GLabel(text="Press 'S' to Continue",
            font_name = 'Arcade.ttf', font_size = 48, linecolor = 'white',
            x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
            self._state = STATE_PAUSED

    def _gamePaused(self):
        """
        Checks the results of the game to see if the player has won or lost the
        game or completed a wave. If the game is still playing, this creates a
        new Wave.
        """
        curr_keys = self._input.is_key_down('s')
        if self._wave.getResult() == 1:
            self._text = GLabel(text="Game Over!",
            font_name = 'Arcade.ttf', font_size = 48, linecolor = 'white',
            x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
            self._state = STATE_COMPLETE
        elif self._wave.getResult() == 2:
            if self._level >= 2:
                self._text = GLabel(text="You won the game!",
                font_name = 'Arcade.ttf', font_size = 48, linecolor = 'white',
                x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
                self._state = STATE_COMPLETE
            else:
                self._text = GLabel(\
                text="You completed the wave.\nPress 'S' to Continue",
                font_name = 'Arcade.ttf', font_size = 48, linecolor = 'white',
                x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
                if curr_keys and not self._last:
                    self._level += 1
                    self._score = self._wave.getScore()
                    self._state = STATE_NEWWAVE
                    self._text = None
        if curr_keys and not self._last:
            self._wave.setShip(Ship(GAME_WIDTH/2, SHIP_BOTTOM, SHIP_WIDTH,
            SHIP_HEIGHT, 'ship.png'))
            if self._state == STATE_PAUSED:
                self._state = STATE_ACTIVE
            self._text = None
        self._last = curr_keys

    def _isGameOver(self):
        """
        Checks the results of the game to ensure that it is still playing. If
        the game is not over, this pauses the game.
        """
        if self._wave.getResult() != 0:
            self._state = STATE_PAUSED
