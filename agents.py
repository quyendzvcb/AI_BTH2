import numbers
import collections
import collections.abc


class Thing:
    """This represents any physical object that can appear in an
    Environment.
    You subclass Thing to get the things you want. Each thing can have a
    .__name__ slot (used for output only)."""

    def __repr__(self):
        return "<{}>".format(getattr(self, "__name__", self.__class__.__name__))

    def is_alive(self):
        """Things that are 'alive' should return true."""
        return hasattr(self, "alive") and self.alive

    def show_state(self):
        """Display the agent's internal state. Subclasses should
        override."""
        print("I don't know how to show_state.")

    def display(self, canvas, x, y, width, height):
        """Display an image of this Thing on the canvas."""

    # Do we need this?
    pass


class Food(Thing):
    pass


class Water(Thing):
    pass


class Agent(Thing):
    """An Agent is a subclass of Thing with one required instance
    attribute."""

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None or not isinstance(program, collections.abc.Callable):
            print(
                "Can't find a valid program for {}, falling back to default.".format(
                    self.__class__.__name__
                )
            )

            def program(percept):
                return eval(input("Percept={}; action?".format(percept)))

        self.program = program

    def can_grab(self, thing):
        """Return True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False


class BlindDog(Agent):
    location = 1

    def movedown(self):
        self.location += 1

    def eat(self, thing):
        '''returns True upon success or False otherwise'''
        if isinstance(thing, Food):
            return True
        return False

    def drink(self, thing):
        ''' returns True upon success or False otherwise'''
        if isinstance(thing, Water):
            return True
        return False


def program(percepts):
    '''Returns an action based on the dog's percepts'''
    for p in percepts:
        if isinstance(p, Food):
            return 'eat'
        elif isinstance(p, Water):
            return 'drink'
    return 'move_down'


# ----------------------------------------------------------------------------------------------------------------------#


class Environment:
    """Abstract class representing an Environment. 'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        """Return the percept that the agent sees at this point. (Implement this.)"""
        raise NotImplementedError

    def execute_action(self, agent, action):
        """Change the world to reflect this action. (Implement this.)"""
        raise NotImplementedError

    def default_location(self, thing):
        """Default location to place a new thing with unspecified location."""
        return None

    def exogenous_change(self):
        """If there is spontaneous change in the world, override this."""
        pass

    def is_done(self):
        """By default, we're done when we can't find a live agent."""
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do. If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for agent, action in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def list_things_at(self, location, tclass=Thing):
        """Return all things exactly at a given location."""
        if isinstance(location, numbers.Number):
            return [
                thing
                for thing in self.things
                if thing.location == location and isinstance(thing, tclass)
            ]
        return [
            thing
            for thing in self.things
            if all(x == y for x, y in zip(thing.location, location))
            and isinstance(thing, tclass)
        ]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this.)"""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = (
                location if location is not None else self.default_location(
                    thing)
            )
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: {} at {}".format(thing, thing.location))
            print(
                "  from list: {}".format(
                    [(thing, thing.location) for thing in self.things]
                )
            )
        if thing in self.agents:
            self.agents.remove(thing)


class Park(Environment):
    def percept(self, agent):
     ##############################################################################
     # TODO: return a list of things that are in our agent's location (our solution
     # is 2 lines of code, but don't worry if you deviate from this)
     ##############################################################################
        # BEGIN OF YOUR CODE #
     ##############################################################################
        things = self.list_things_at(agent.location)
        return things
 ##############################################################################
 # END OF YOUR CODE #
 ##############################################################################

    def execute_action(self, agent, action):
     ##############################################################################
     # TODO: changes the state of the environment based on what the agent does.
     # (our solution is 15 lines of code, but don't worry if you deviate from this)
     ##############################################################################
     # BEGIN OF YOUR CODE #
     ##############################################################################
        if action == "move_down":
            print(
                f"BlindDog decided to move down at location: {agent.location}")
            agent.movedown()
        elif action == "eat":
            foods = self.list_things_at(agent.location, Food)
            if foods != 0:
                agent.eat(foods[0])
                print(
                    f"{str(agent)} ate {str(foods[0])} at location: {agent.location}")
                self.delete_thing(foods[0])
                agent.performance += 1
        elif action == "drink":
            waters = self.list_things_at(agent.location, Water)
            if waters != 0:
                agent.drink(waters[0])
                print(
                    f"{str(agent)} drank {str(waters[0])} at location: {agent.location}")
                self.delete_thing(waters[0])
                agent.performance += 1

 ##############################################################################
 # END OF YOUR CODE #
 ##############################################################################
    def is_done(self):
        '''By default, we're done when we can't find a live agent,
        but to prevent killing our cute dog, we will stop before itself - when there is
        no more food or water'''
 ##############################################################################
 # TODO: By default, we're done when we can't find a live agent, but to prevent
 # killing our cute dog, we will stop before itself - when there is no more
 # food or water. (our solution is 3 lines of code, but don't worry if you
 # deviate from this)
 ##############################################################################
 # BEGIN OF YOUR CODE #
 ##############################################################################
        agents_dead = not any(agent.is_alive() for agent in self.agents)
        no_resources = not any(isinstance(thing, Food) or isinstance(
            thing, Water) for thing in self.things)
        return agents_dead or no_resources
 ##############################################################################
 # END OF YOUR CODE #
 ###########################################################################

##############################################################################


class Obstacle(Thing):
    """Something that can cause a bump, preventing an agent from
    moving into the same square it's in."""
    pass


class Wall(Obstacle):
    pass


class Direction:
    R = "right"
    L = "left"
    U = "up"
    D = "down"

    def __init__(self, direction):
        self.direction = direction

    def __add__(self, heading):
        """>>> d = Direction('right')
    >>> l1 = d.__add__(Direction.L)
    >>> l2 = d.__add__(Direction.R)
    >>> l1.direction
 'up'
 >>> l2.direction
 'down'
 >>> d = Direction('down')
 >>> l1 = d.__add__('right')
 >>> l2 = d.__add__('left')
 >>> l1.direction == Direction.L
 True
 >>> l2.direction == Direction.R
 True """
        if self.direction == self.R:
            return {
                self.R: Direction(self.D),
                self.L: Direction(self.U),
            }.get(heading, None)
        elif self.direction == self.L:
            return {
                self.R: Direction(self.U),
                self.L: Direction(self.D),
            }.get(heading, None)
        elif self.direction == self.U:
            return {
                self.R: Direction(self.R),
                self.L: Direction(self.L),
            }.get(heading, None)
        elif self.direction == self.D:
            return {
                self.R: Direction(self.L),
                self.L: Direction(self.R),
            }.get(heading, None)

    def move_forward(self, from_location):
        """>>> d = Direction('up')
 >>> l1 = d.move_forward((0, 0))
 >>> l1
 (0, -1)
 >>> d = Direction(Direction.R)
 >>> l1 = d.move_forward((0, 0))
 >>> l1
 (1, 0)
 """
 # get the iterable class to return
        iclass = from_location.__class__
        x, y = from_location
        if self.direction == self.R:
            return iclass((x + 1, y))
        elif self.direction == self.L:
            return iclass((x - 1, y))
        elif self.direction == self.U:
            return iclass((x, y - 1))
        elif self.direction == self.D:
            return iclass((x, y + 1))


class XYEnvironment(Environment):
 """This class is for environments on a 2D plane, with locations
 labelled by (x, y) points, either discrete or continuous.
 Agents perceive things within a radius. Each agent in the
 environment has a .location slot which should be a location such
 as (0, 1), and a .holding slot, which should be a list of things
 that are held."""

 def __init__(self, width=10, height=10):
    super().__init__()
    self.width = width
    self.height = height
    self.observers = []
 # Sets iteration start and end (no walls).
    self.x_start, self.y_start = (0, 0)
    self.x_end, self.y_end = (self.width, self.height)
 perceptible_distance = 1


 def things_near(self, location, radius=None):
        """Return all things within radius of location."""
        if radius is None:
            radius = self.perceptible_distance
            radius2 = radius * radius
        return [(thing, radius2 - distance_squared(location,
thing.location))
    for thing in self.things if distance_squared(location, thing.location) <= radius2]



'''---------------------------------------------------------------------------'''

if __name__ == "__main__":
 # t = Thing()
 # print(repr(t))
    park=Park()
    dog=BlindDog(program)
    dogfood=Food()
    water=Water()

    park.add_thing(dog, 1)
    park.add_thing(dogfood, 5)
    park.add_thing(water, 7)

    park.run(10)
