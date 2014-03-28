#!/usr/bin/python

import sys
import hashlib
import copy

fig_player = '@'
fig_space = '.'
fig_wall = '#'
fig_box = 'o'
fig_place = 'x'
fig_placed_box = '*'

class Win(Exception):
  pass


def showField(state):

    (field, (rows, columns), player) = state
    state_hash = hashlib.md5(str(state)).hexdigest()
    print "State %s" % state_hash
    i = 0;
    sys.stdout.write(' ');
    for j in range(columns):
        sys.stdout.write(str(j))
    print
    for line in field:
        if i == player[0]:
          #gently copy this dammit line to prevent modifying game state
          line = line[:]
          line[player[1]] = fig_player
        print str(i) + '' +  ''.join(line)
        i += 1;

def loadField(file):
    field = []
    rows = 0
    columns = 0
    player_count = 0
    box_count = 0
    place_count = 0

    for line in open(file, 'r'):
        for char in line:
            if char == fig_player:
                player_count += 1
                player = (rows, line.find(fig_player))
            if char == fig_box:
                box_count += 1
            if char == fig_place:
                place_count += 1
            if char == fig_placed_box:
                box_count += 1
                place_count += 1

        l = line.strip()
        field.append(list(l))
        rows += 1

        if columns == 0:
            columns = len(l)
        if columns != len(l):
            print "Field must be recangular"
            exit(2)

    if player_count != 1:
        print "Field must have one player"
        exit(1)
    if box_count != place_count or box_count == 0:
        print "Wrong number of boxes and places"
        exit(1)

    field[player[0]][player[1]] = fig_space
    return (field, (columns, rows), player)

def checkWin(state):
    (field, size, (pr, pc)) = state

    for row in field:
      if row.count(fig_box) != 0:
        return False
    print "WIN!"
    return True

def makeMove(state):


    st = copy.deepcopy(state)
    (fld, size, (pr, pc)) = st
    field = copy.deepcopy(fld)

    left = (0, -1)
    right = (0, 1)
    up = (-1, 0)
    down = (1, 0)

    for (dr, dc) in (left, right, up, down):

      #new position
      new_pr = pr + dr
      new_pc = pc + dc

      if new_pr < 0 or new_pr >= size[0] or new_pc < 0 or new_pc >= size[1]:
        continue
      new_cell = field[new_pr][new_pc]

      #next nearest position
      next_pr = pr + 2*dr
      next_pc = pc + 2*dc
      if next_pc < 0 or next_pr < 0 or next_pr >= size[0] or next_pc >= size[1]:
        next_cell = fig_wall        #there is only walls outside game field
      else:
        next_cell = field[next_pr][next_pc]

      if new_cell == fig_wall:
        continue

      elif new_cell == fig_place or new_cell == fig_space:
        player = (new_pr, new_pc)
        yield (field, size, player)

      elif new_cell == fig_box:
        if next_cell == fig_space:                  #move box to free space
          field[next_pr][next_pc] = fig_box
          field[new_pr][new_pc] = fig_space
          player = (new_pr, new_pc)
          #TODO check box is in the corner and exclude this state - obviously,
          #we cannot do anything with this box now
          yield (field, size, player)
        elif next_cell == fig_place:                #move box to target place
          field[next_pr][next_pc] = fig_placed_box
          field[new_pr][new_pc] = fig_space
          player = (new_pr, new_pc)
          if checkWin((field, size, player)):
            raise Win()
          yield (field, size, player)
        # we can move box only on free space or into target place, so check next 
        # possible movement
        continue

      elif new_cell == fig_placed_box:
        if next_cell == fig_space:                  #move box from target place to free space
          field[next_pr][next_pc] = fig_box
          field[new_pr][new_pc] = fig_place
          player = (new_pr, new_pc)
          yield (field, size, player)
        elif next_cell == fig_place:                #move box from target place to another one
          field[next_pr][next_pc] = fig_placed_box
          field[new_pr][new_pc] = fig_place
          player = (new_pr, new_pc)
          if checkWin((field, size, player)):
            raise Win()
          yield (field, size, player)
        # we can move box only on free space or into target place, so check next 
        # possible movement
        continue



start_state = (field, (columns, rows), player) = loadField(sys.argv[1])
showField(start_state)

print "Rows %i columns %i, player at (%i, %i)" % (rows, columns, player[0], player[1])
state_hash = hashlib.md5(str(start_state)).hexdigest()

all_states = {state_hash: start_state}
tmp = {}

#for s in makeMove(start_state):
#  showField(s)

try:
  #while True:
  for x in range(2):

    for state in all_states.values():
      #h = hashlib.md5(str(state)).hexdigest()
      #print "For state %s" % h

      new_states = makeMove(state)
      for new_state in new_states:
          state_hash = hashlib.md5(str(new_state)).hexdigest()
          if not all_states.get(state_hash): # and not tmp.get(state_hash):
            tmp[state_hash] = copy.deepcopy(new_state)
          else:
            #print "Skipping %s" % state_hash
            pass

    for (k, v) in tmp.iteritems():
      all_states[k] = v
    tmp = {}
    print "Found %i states:" % len(all_states.keys())
    #print " ".join(all_states.keys())
    #exit(0)
except Win:
  print "Win!\nStates analyzed: %i" % (len(all_states.values()) + len(tmp.values()))

for s in all_states.values():
  showField(state)
  pass

