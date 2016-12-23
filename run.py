# The Fortress of Peril
# A very incomplete text adventure

# Adapted from some code I wrote to
# better learn OOP in Python. The 
# parser, entities, and loop would
# normally be their own modules.
# Only look/examine, move, and quit
# commands have been implemented.

# Requires Python 3


# import readline automatically allows for line
# editing and command history with input()
import readline

# if true, will print the parser's 
# interpretation of player commands
debug = True


# create classes for game objects

class Room(object):
    "Class for rooms in the world. Created with x, y, z \
    coordinates and descriptions."
    
    # these are class-level indexes that keep track
    # of all the rooms that have been created
    index = []
    name_index = {}
    loc_index = {}

    def __init__(self, name, description, x, y, z=0, ):
        "instantiate object and add to class-level indexes"
        if name in Room.name_index:
            raise KeyError('That name is already in use for another room')
        if (x, y, z) in Room.loc_index:
            raise KeyError('That location is already in use for another room')
        self.contents = []
        self.inhabitants = []
        self.name = name
        self.description = description
        self.x, self.y, self.z = x, y, z

        # This gives the room a unique value associated with it
        # Don't need to increment because of how len() works
        self.index = len(Room.index)

        self.coordinates = x, y, z
        self.loc = x, y, z
        
        Room.index.append(self)
        Room.name_index[name] = self
        Room.loc_index[(x, y, z)] = self
        Mob.loc_index[self] = []
        
    def lookup(query):
        """return an object based on a query \
        can take name (str), loc (tuple, or index (int)"""
        if isinstance(query, str):
            out = Room.name_index[query]
            return out
        if isinstance(query, int):
            out = Room.index[query]
            return out
        if isinstance(query, tuple):
            out = Room.loc_index[query]
            return out

    def __repr__(self):
        return "<%s: Room object located at x=%s, y=%s, z=%s,\
 inhabitants=%s, contents=%s>" % (self.name, self.x, self.y, self.z,
                                  self.inhabitants, self.contents)

    def __str__(self):
        return "<Room: %s>" % self.name


class Mob(object):
    "Class for creatures in the world"
    index = []
    name_index = {}
    loc_index = {}

    def __init__(self, name, loc, description,
                 takeable=False, inventory=[], health=10, ducats=0):
        self.name = name
        self.takeable = takeable
        self.description = description
        self.loc = loc
        self.inventory = inventory
        self.health, self.ducats = health, ducats
        self.index = len(Mob.index)
        Mob.index.append(self)

        Mob.name_index[name] = self

        Mob.loc_index[loc].append(self)
        Mob.index.append(self)
        self.loc.inhabitants.append(self)

        # add name to nouns list for parser
        tokens['nouns'].append(self.name.upper())

    def show_inventory(self):
        print('You are carrying:\n')
        for item in self.inventory:
            print(item.name)

            
    def take(self, obj):
        print(obj.name)
        print(items_present_at(self.loc))
        if obj.name.upper() in items_present_at(self.loc):
            item_present = True
        else:
            item_present = False
        if item_present and obj.takeable:
            self.inventory.append(obj)
            self.loc.inhabitants.remove(obj)
            print('You took the ' + obj.name)
        elif not item_present:
            print("You don't see that here.")
        elif not obj.takeable:
            print("You can't take that!")

    def lookup(query):
        "Lets you look up an object using index (int),\
        location (tuple), or name (str)"
        if isinstance(query, str):
            out = Mob.name_index[query]
            return out
        if isinstance(query, int):
            out = Mob.index[query]
            return out
        if isinstance(query, tuple):
            out = Mob.loc_index[query]
            return out

    def get_room_in_direction(self, direction):
        "Return# the room in a given direction"
        if direction not in tokens['directions']:
            raise LookupError('Not a valid direction')
        new_loc = get_direction_loc(self.loc.loc, direction)
        if new_loc not in Room.loc_index:
            return False
        else:
            return Room.loc_index[new_loc]

    def move(self, direction):
        intended_location = self.get_room_in_direction(direction)
        if intended_location:
            self.loc.inhabitants.remove(self)
            self.loc = intended_location
            self.loc.inhabitants.append(self)
            return intended_location
        else:
            return False

    def __repr__(self):
        return "<%s: Mob object located at %s,\
 inventory=%s, ducats=%s, health=%s>" % (self.name, self.loc, self.inventory,
                                         self.ducats, self.health)

    def __str__(self):
        return "<Mob: %s>" % self.name

    
def full_description(location):
    "Compile a full description of a location in the game, \
    including mobs and objects."
    output_string = player.loc.description + '\n'

    mob_list = player.loc.inhabitants
    if len(mob_list) == 1:
        mob_sighting = 'You see here %s.' % mob_list[0].description
    elif len(mob_list) == 2:
        mob_sighting = 'You see here %s and %s.' % (mob_list[0].description, mob_list[1].description)
    else:
        mob_sighting = 'You see here '
        for mob in mob_list[:-1]:
            mob_sighting += mob.description + ', '
        mob_sighting += 'and ' + mob_list[-1].description + '.'

    output_string += '\n' + mob_sighting + '\n'
    return output_string

    
def get_direction_loc(loc, direction):
    'Takes location tuple and string for direction, i.e. "north" \
    returns new location'
    loc = list(loc)
    if direction == 'NORTH':
        modified_loc = loc[0], loc[1] + 1, loc[2]
        return modified_loc
    if direction == 'EAST':
        modified_loc = loc[0] + 1, loc[1], loc[2]
        return modified_loc
    if direction == 'SOUTH':
        modified_loc = loc[0], loc[1] - 1, loc[2]
        return modified_loc
    if direction == 'WEST':
        modified_loc = loc[0] - 1, loc[1], loc[2]
        return modified_loc
    if direction == 'UP':
        modified_loc = loc[0], loc[1], loc[2] + 1
        return modified_loc
    if direction == 'DOWN':
        modified_loc = loc[0], loc[1], loc[2] - 1
        return modified_loc


# Add instantiated objects to allowed nouns list
[token['nouns'].append(item.name) for item in Room.name_index]


def items_present_at(location):
    "Checks if a game object is present at a location.\
    Returns false if not present."
    names = []
    for item in location.inhabitants:
        names.append(item.name.upper())

    return names


# define helper functions for parser and command execution

def check_token_type(token_list, type):
    "Grab the first token of a particular type from a list of tokens."
    for token in token_list:
        if token in tokens[type]:
            return token
    return False


def replace_synonyms(token_list, synonyms):
    "Replace all words in a list of tokens with given synonyms."
    out_list = []
    for token in token_list:
        if token in synonyms:
            out_list.append(synonyms[token])
        else:
            out_list.append(token)
    return out_list


def remove_filler_words(token_list, filler_list):
    "Compare token list with list of filler words and remove."
    for token in token_list:
        if token in filler_list:
            token_list.remove(token)
    return token_list


def parse_input(input):
    "Parse input string and return parsed dictionary."
    output_dictionary = {}
    input = input.split()
    input = [token.upper() for token in input]
    input = replace_synonyms(input, synonyms)
    input = remove_filler_words(input, tokens['filler'])
    if len(input) > 1:
        output_dictionary['remainder'] = input[1:]
    else:
        output_dictionary['remainder'] = False
    output_dictionary['verb'] = check_token_type(input, 'verbs')
    output_dictionary['noun'] = check_token_type(input, 'nouns')
    output_dictionary['direction'] = check_token_type(input, 'directions')

    return output_dictionary


def command_execute(commands, player):
    "Takes commands as parsed dictionary of tokens. \
    Choose command that fits criteria and execute."
    if debug:
        print(commands)
    if commands['verb'] == 'QUIT':
        exit_prompt = input("Are you sure you want to quit the game? ")
        if exit_prompt.upper() == 'Y' or exit_prompt.upper() == 'YES':
            exit()
    if commands['direction'] and not commands['verb'] or commands['verb'] == 'GO':
        if player.move(commands['direction']):
            print('You move %s to the %s.\n' % (
                commands['direction'].lower(),
                player.loc.name))
            print(full_description(player.loc.description))
        else:
            print("Sadly, you can't go %s from here." % commands['direction'].lower())
    elif commands['direction'] and commands['verb'] == 'LOOK':
        vista = player.get_room_in_direction(commands['direction'])
        if vista:
            print('To the north, you see the ' + vista.name + '.')
        else:
            print("You don't see anything in that direction.")
    elif commands['verb'] == 'LOOK' and not commands['remainder']:
        print(full_description(player.loc))
    elif commands['verb'] == 'LOOK' and commands['remainder']:
        if commands['noun'] in items_present_at(player.loc ):
            print("You're looking at " +
                  Mob.lookup(commands['noun'].lower()).description + '.')
        else:
            print("You don't see that here")
    elif commands['verb'] == 'GET' and commands['noun']:
        player.take(Mob.lookup(commands['noun'].lower()))
    elif commands['verb'] == 'GET' and commands['remainder']:
        print("You don't see that here.")
    elif commands['verb'] == 'GET' and not commands['remainder']:
        print("Take what?")
    elif commands['verb'] == 'INVENTORY':
        player.show_inventory()
    else:
        print("You can't do that.")


# Define the lexicon of words detected by the parser.
tokens = {
    'directions': [
        'NORTH',
        'SOUTH',
        'EAST',
        'WEST',
        'NORTHWEST',
        'NORTHEAST',
        'SOUTHEAST',
        'SOUTHWEST',
        'UP',
        'DOWN',
        ],
    'verbs':[
        'QUIT',
        'INVENTORY',
        'GO',
        'LOOK',
        'GET'
        ],
    'nouns':
     [
        'SELF',
        ],
    'filler':[
        'THE',
        'AT',
        'TO',
        'AND',
        'OF',
        'A',
        'AN',],
    }

synonyms = {
    'TAKE': 'GET',
    'L': 'LOOK',
    'SCRUTINIZE': 'LOOK',
    'EXAMINE': 'LOOK',
    'X': 'LOOK',
    'N': 'NORTH',
    'I': 'INVENTORY',
    'S': 'SOUTH',
    'E': 'EAST',
    'NE': 'NORTHEAST',
    'SE': 'SOUTHEAST',
    'NW': 'NORTHWEST',
    'SW': 'SOUTHWEST',
    'W': 'WEST',
    'U': 'UP',
    'D': 'DOWN',
    'WALK': 'GO',
    'MOVE': 'GO',
    'RUN': 'GO',
    'MOVE': 'GO',
    'YOURSELF': 'PLAYER',
    'SELF': 'PLAYER',
}


# instantiate game objects

gates = Room('gates',
             '''After weeks of difficult travel, you have arrived at the gates of the Fortress of Peril. Inside lies the Magical Dingus, the artifact required for your people's salvation...and your own. Adventurer, do you have the temerity to succeed where so many others have fallen?

The entrance to the Fortress is to the north.''',
             10, 10)

antechamber = Room('antechamber',
                   'This drafty antechamber is filled with tapestries depicting the battles of yore. The gates of the Fortress of Peril are behind you to the south.',
                   10, 11)


player = Mob('player', Room.lookup('gates'), 'yourself')
gatekeeper = Mob('gatekeeper', Room.lookup('gates'),
                 "the Fortress's ghoulish gatekeeper")
goblet = Mob('goblet', Room.lookup('gates'),
             "a beautiful emerald-encrusted goblet",
             takeable=True)

# game loop

# print room description on game start
print("\n" + full_description(player.loc.description))

# main loop
if __name__ == '__main__':
    while 1:
        query = input('> ')
        commands = parse_input(query)
        command_execute(commands, player)

