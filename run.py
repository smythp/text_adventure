debug = False


class Room(object):

    # these are class-level indexes that keep track
    # of all the rooms that have been created
    index = []
    name_index = {}
    loc_index = {}

    # instantiate object and add to class-level indexes
    def __init__(self, name, description, x, y, z=0, ):
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

        
        # return a dictionary based on a query
        # can take name (str), loc (tuple, or index (int)
    def lookup(query):
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


# class for creatures in the world
class Mob(object):
    index = []
    name_index = {}
    loc_index = {}

    def __init__(self, name, loc, description,
                 inventory=[], health=10, ducats=0):
        self.name = name
        self.description = description
        self.loc = loc
        self.inventory = inventory
        self.health, self.ducats = health, ducats
        self.index = len(Mob.index)
        Mob.index.append(self)
        if name in Mob.name_index:
            Mob.name_index[name].append(self)
        else:
            Mob.name_index[name] = [self]
        Mob.loc_index[loc].append(self)
        Mob.index.append(self)
        self.loc.inhabitants.append(self)

    # lets you look up an object using index (int),
    # location (tuple), or name (str)
    def lookup(query):
        if isinstance(query, str):
            out = Mob.name_index[query]
            return out
        if isinstance(query, int):
            out = Mob.index[query]
            return out
        if isinstance(query, tuple):
            out = Mob.loc_index[query]
            return out

    # return the room in a given direction
    def get_room_in_direction(self, direction):
        if direction not in Constants.valid_directions:
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

    def __repr__(self):
        return "<%s: Mob object located at %s,\
 inventory=%s, ducats=%s, health=%s>" % (self.name, self.loc, self.inventory,
                                         self.ducats, self.health)

    def __str__(self):
        return "<Mob: %s>" % self.name


class Constants(object):
    valid_directions = ('N',
                        'S',
                        'E',
                        'W',
                        'U',
                        'D',
                        'NORTH',
                        'SOUTH',
                        'EAST',
                        'WEST',
                        'UP',
                        'DOWN',
                        'NE',
                        'SE',
                        'NW',
                        'SW',
                        'NORTHEAST',
                        'SOUTHEAST',
                        'NORTHWEST',
                        'SOUTHWEST', )


def full_description(location):
    "Compile a full description of a location in the game, \
    including mobs and objects."
    output_string = '\n' + player.loc.description + '\n'

    mob_list = player.loc.inhabitants
    if len(mob_list) == 1:
        mob_sighting = 'You see here %s.' % mob_list[0].description
    elif len(mob_list) == 2:
        mob_sighting = 'You see here %s and %s.' % (mob_list[0].description, mob_list[1].description)
    else:
        mob_sighting = 'You see here'
        for mob in mob_list[:-1]:
            mob_sighting += mob.description + ', '
            mob_sighting += 'and ' + mob.description + '.'

    output_string += '\n' + mob_sighting + '\n'
    return output_string

    
# takes location tuple and string for direction, i.e. "north"
# returns new location
def get_direction_loc(loc, direction):
    loc = list(loc)
    if direction == 'N' or direction == 'NORTH':
        modified_loc = loc[0], loc[1] + 1, loc[2]
        return modified_loc
    if direction == 'E' or direction == 'EAST':
        modified_loc = loc[0] + 1, loc[1], loc[2]
        return modified_loc
    if direction == 'S' or direction == 'SOUTH':
        modified_loc = loc[0], loc[1] - 1, loc[2]
        return modified_loc
    if direction == 'W' or direction == 'WEST':
        modified_loc = loc[0] - 1, loc[1], loc[2]
        return modified_loc
    if direction == 'U' or direction == 'UP':
        modified_loc = loc[0], loc[1], loc[2] + 1
        return modified_loc
    if direction == 'D' or direction == 'DOWN':
        modified_loc = loc[0], loc[1], loc[2] - 1
        return modified_loc


def debug_indexes():
    print('''Room location index:
    ''')
    print(Room.loc_index)
    print('''Room index:
    ''')
    print(Room.index)
    print('''Room name index:
    ''')
    print(Room.name_index)
    print('''Mob location index
    ''')
    print(Mob.loc_index)
    print('''Mob index:
    ''')
    print(Mob.index)
    print('''Mob name index:
    ''')
    print(Mob.name_index)


# Lexicon for parser

tokens = {
    'directions': [
        'NORTH',
        'SOUTH',
        'EAST',
        'WEST',
        ],
    'verbs':[
        'QUIT',
        'GO',
        'L',
        'LOOK',
        'RUN',
        'WALK',
        'EAT',
        'KILL',
        ],
    'nouns':
     [
        'BEAR',
        'PRINCESS',
        ],
    'filler':[
        'THE',
        'TO',
        'AND',
        'OF',
        'A',
        'AN',],
    }


synonyms = {
    'L': 'LOOK',
    'SCRUTINIZE': 'LOOK',
    'EXAMINE': 'LOOK',
    'X': 'LOOK',
    'N': 'NORTH',
    'S': 'SOUTH',
    'E': 'EAST',
    'W': 'WEST',
    'WALK': 'GO',
    'MOVE': 'GO',
    'RUN': 'GO',
    'AMBLE': 'GO',
    }


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
    output_dictionary = {}
    input = input.split()
    input = [token.upper() for token in input]
    input = replace_synonyms(input, synonyms)
    input = remove_filler_words(input, tokens['filler'])

    output_dictionary['verb'] = check_token_type(input, 'verbs')
    output_dictionary['noun'] = check_token_type(input, 'nouns')
    output_dictionary['direction'] = check_token_type(input, 'directions')

    return output_dictionary


def command_execute(commands, player):
    if debug:
        print(commands)
    if commands['verb'] == 'QUIT':
        exit_prompt = input("Are you sure you want to quit the game? ")
        if exit_prompt.upper() == 'Y' or exit_prompt.upper() == 'YES':
            exit()
    if commands['direction'] and not commands['verb'] or commands['verb'] == 'GO':
        player.move(commands['direction'])
        print('You move %s to the %s.' % (
            commands['direction'].lower(),
            player.loc.name))
        print(full_description(player.loc.description))
    elif commands['verb'] and commands['direction'] and commands['verb'] == 'LOOK':
        print(entities.player.get_room_in_direction(commands['direction']))
    elif commands['verb'] and commands['verb'] == 'LOOK':
        print('You are at', player.loc.name, str(player.loc.loc))
    elif commands['verb'] and commands['verb'] == 'MAP':
        for location in entities.Room.index:
            print(location.name, str(location.loc))
    else:
        pass

    
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
        'IN',
        'OUT',
        'EXIT',
        'N',
        'S',
        'E',
        'W',
        'U',
        'D',
        'NW',
        'NE',
        'SE',
        'NW',
        ],
    'verbs':[
        'QUIT',
        'GO',
        'LOOK',
        ],
    'nouns':
     [
        'BEAR',
        'PRINCESS',
        ],
    'filler':[
        'THE',
        'TO',
        'AND',
        'OF',
        'A',
        'AN',],
    }

synonyms = {
    'L': 'LOOK',
    'SCRUTINIZE': 'LOOK',
    'EXAMINE': 'LOOK',
    'X': 'LOOK',
    'N': 'NORTH',
    'S': 'SOUTH',
    'E': 'EAST',
    'W': 'WEST',
    'U': 'UP',
    'D': 'DOWN',
    'WALK': 'GO',
    'MOVE': 'GO',
    'RUN': 'GO',
    'MOVE': 'GO',
    }


gates = Room('gates',
             '''After weeks of difficult travel, you have arrived at the gates of the Fortress of Peril. Inside lies the Magical Dingus, the artifact required for your people's salvation...and your own. Adventurer, do you have the temerity to succeed where so many others have fallen?

The entrance to the Fortress is to the north.''',
             10, 10)

antechamber = Room('antechamber',
                   'This drafty antechamber is filled with tapestries depicting the battles of yore.',
                   10, 11)


player = Mob('Player', Room.lookup('gates'), 'yourself')
gatekeeper = Mob('gatekeeper', Room.lookup('gates'),
                 "the Fortress's ghoulish gatekeeper")


# print room description on game start
print()
print(full_description(player.loc.description))

# game loop
while 1:
    query = input('> ')
    commands = parse_input(query)
    command_execute(commands, player)