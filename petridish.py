"""
  Petri Dish (a cellular automaton simulator)
  Developed by Kharidiron <kharidiron@gmail.com>
  Created: Aug 15, 2013
  Last modified: August 15, 2013
  @author: Rion Parsons
"""

import sys
import pygame
from pygame.locals import *
import numpy
import re

class Application:
  """ Core application class.  Eveything is in this. """
  def __init__(self):
    """class object constructor"""
    self.running = True
    self._display_surf = None
    self.window_dims = self.window_weight, self.window_height = 640, 500
    self.board_dims = self.board_weight, self.board_height = 640, 464
    self.menubar_size = self.window_height - self.board_height
    self.menubar = {}
    self.buildmenu = False
    self.buildboard = False
    self.block_size = 15
    self.margin = 1
    self.neighborhood_select = False# True: von Neumann, False: Moore
    self.count_self = False
    self.radiusstring = "1"
    self.radius = 1
    self.ui_focus = "none"
    self.shifted = False
    self.ruleerror = False
    self.radiuserror = False
    self.screenregions = {}
    self.boardcells = {}
    self.ruleset = "wireworld" #Options are: conway, brian, wireworld
    self.cellstates = ["white", "navy", "maroon", "gold", "darkgreen"]
    self.rulefocus = False
    self.radiusfocus = False
    self.neighborhood = ""
    self.rules = ()
    self.cellnumbers = False

    if self.ruleset == "conway":
      # This is the typical ruleset for Conway's Game of Life
      self.totalcellstates = 2
      self.rulestring = "B3/S23"
    elif self.ruleset == "brian":
      # Brian's Brain - Three cell states: Alive, dying and dead. Once alive,
      # will always proceed to dying and then dead
      self.totalcellstates = 2
      self.rulestring = "B2/"
    elif self.ruleset == "wireworld":
      # Wireworld - Four cell states: Empty space, Electron head, Electron tail, and Conductor
      # Can be used for some simple, nifty electronics demos
      self.totalcellstates = 4
      self.rulestring = "B12/"

    self.grid_size = (self.block_size + self.margin)
    self.cols = self.board_weight / self.grid_size
    self.rows = self.board_height / self.grid_size
    self.grid = numpy.zeros(self.cols*self.rows, dtype="int").reshape(self.rows, self.cols)
    self.newgrid = numpy.zeros(self.cols*self.rows, dtype="int").reshape(self.rows, self.cols)
    self.oldgrid = numpy.zeros(self.cols*self.rows, dtype="int").reshape(self.rows, self.cols)

    self.count = 0
    self.playing = False
    self.clock = pygame.time.Clock()

  def on_init(self):
    """Initializes the application itself, including spawing the display."""
    pygame.init()
    self._display_surf = pygame.display.set_mode(self.window_dims)
    self._caption = pygame.display.set_caption("Petri Dish - A CA Simulator")
    pygame.font.init()
    if pygame.font:
      self.font = pygame.font.Font(None,30)
    else:
      self.font = None
    self.fontobject = pygame.font.Font(None,20)
    self._running = True
 
  def on_event(self, event):
    """"""
    keyvalue = ""
    if event.type == pygame.QUIT:
      self._running = False
    if event.type == pygame.KEYUP:
      if event.key == K_LSHIFT or event.key == K_RSHIFT:
        self.shifted = False
    elif event.type == pygame.KEYDOWN:
      if event.key == K_LSHIFT or event.key == K_RSHIFT:
        self.shifted = True
      if self.ui_focus == "none":
        if event.key == pygame.K_p:
          self.on_play()
        elif event.key == pygame.K_c:
          self.on_clear()
        elif ( (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE) ):
          self._running = False
      else:
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
          self.ui_focus = "none"
        elif event.key == pygame.K_BACKSPACE:
          exec "self."+ self.ui_focus +" = self."+ self.ui_focus +"[0:-1]"
        else:
          if not self.shifted:
            if event.key == K_a: keyvalue += "a"
            elif event.key == K_b: keyvalue += "b"
            elif event.key == K_c: keyvalue += "c"
            elif event.key == K_d: keyvalue += "d"
            elif event.key == K_e: keyvalue += "e"
            elif event.key == K_f: keyvalue += "f"
            elif event.key == K_g: keyvalue += "g"
            elif event.key == K_h: keyvalue += "h"
            elif event.key == K_i: keyvalue += "i"
            elif event.key == K_j: keyvalue += "j"
            elif event.key == K_k: keyvalue += "k"
            elif event.key == K_l: keyvalue += "l"
            elif event.key == K_m: keyvalue += "m"
            elif event.key == K_n: keyvalue += "n"
            elif event.key == K_o: keyvalue += "o"
            elif event.key == K_p: keyvalue += "p"
            elif event.key == K_q: keyvalue += "q"
            elif event.key == K_r: keyvalue += "r"
            elif event.key == K_s: keyvalue += "s"
            elif event.key == K_t: keyvalue += "t"
            elif event.key == K_u: keyvalue += "u"
            elif event.key == K_v: keyvalue += "v"
            elif event.key == K_w: keyvalue += "w"
            elif event.key == K_x: keyvalue += "x"
            elif event.key == K_y: keyvalue += "y"
            elif event.key == K_z: keyvalue += "z"
            elif event.key == K_0: keyvalue += "0"
            elif event.key == K_1: keyvalue += "1"
            elif event.key == K_2: keyvalue += "2"
            elif event.key == K_3: keyvalue += "3"
            elif event.key == K_4: keyvalue += "4"
            elif event.key == K_5: keyvalue += "5"
            elif event.key == K_6: keyvalue += "6"
            elif event.key == K_7: keyvalue += "7"
            elif event.key == K_8: keyvalue += "8"
            elif event.key == K_9: keyvalue += "9"
            elif event.key == K_BACKQUOTE: keyvalue += "`"
            elif event.key == K_MINUS: keyvalue += "-"
            elif event.key == K_EQUALS: keyvalue += "="
            elif event.key == K_LEFTBRACKET: keyvalue += "["
            elif event.key == K_RIGHTBRACKET: keyvalue += "]"
            elif event.key == K_BACKSLASH: keyvalue += "\\"
            elif event.key == K_SEMICOLON: keyvalue += ";"
            elif event.key == K_QUOTE: keyvalue += "\'"
            elif event.key == K_COMMA: keyvalue += ","
            elif event.key == K_PERIOD: keyvalue += "."
            elif event.key == K_SLASH: keyvalue += "/"
          elif self.shifted:
            if event.key == K_a: keyvalue += "A"
            elif event.key == K_b: keyvalue += "B"
            elif event.key == K_c: keyvalue += "C"
            elif event.key == K_d: keyvalue += "D"
            elif event.key == K_e: keyvalue += "E"
            elif event.key == K_f: keyvalue += "F"
            elif event.key == K_g: keyvalue += "G"
            elif event.key == K_h: keyvalue += "H"
            elif event.key == K_i: keyvalue += "I"
            elif event.key == K_j: keyvalue += "J"
            elif event.key == K_k: keyvalue += "K"
            elif event.key == K_l: keyvalue += "L"
            elif event.key == K_m: keyvalue += "M"
            elif event.key == K_n: keyvalue += "N"
            elif event.key == K_o: keyvalue += "O"
            elif event.key == K_p: keyvalue += "P"
            elif event.key == K_q: keyvalue += "Q"
            elif event.key == K_r: keyvalue += "R"
            elif event.key == K_s: keyvalue += "S"
            elif event.key == K_t: keyvalue += "T"
            elif event.key == K_u: keyvalue += "U"
            elif event.key == K_v: keyvalue += "V"
            elif event.key == K_w: keyvalue += "W"
            elif event.key == K_x: keyvalue += "X"
            elif event.key == K_y: keyvalue += "Y"
            elif event.key == K_z: keyvalue += "Z"
            elif event.key == K_0: keyvalue += ")"
            elif event.key == K_1: keyvalue += "!"
            elif event.key == K_2: keyvalue += "@"
            elif event.key == K_3: keyvalue += "#"
            elif event.key == K_4: keyvalue += "$"
            elif event.key == K_5: keyvalue += "%"
            elif event.key == K_6: keyvalue += "^"
            elif event.key == K_7: keyvalue += "&"
            elif event.key == K_8: keyvalue += "*"
            elif event.key == K_9: keyvalue += "("
            elif event.key == K_BACKQUOTE: keyvalue += "~"
            elif event.key == K_MINUS: keyvalue += "_"
            elif event.key == K_EQUALS: keyvalue += "+"
            elif event.key == K_LEFTBRACKET: keyvalue += "{"
            elif event.key == K_RIGHTBRACKET: keyvalue += "}"
            elif event.key == K_BACKSLASH: keyvalue += "|"
            elif event.key == K_SEMICOLON: keyvalue += ":"
            elif event.key == K_QUOTE: keyvalue += "\""
            elif event.key == K_COMMA: keyvalue += "<"
            elif event.key == K_PERIOD: keyvalue += ">"
            elif event.key == K_SLASH: keyvalue += "?"
          exec "self."+self.ui_focus+" += keyvalue"
    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        mouseposition = pygame.mouse.get_pos()
        self.check_clicked(mouseposition)

  def on_loop(self):
    """"""
    if self.playing == True:
      self.count = self.count + 1
      self.evolveBoard()
      if numpy.array_equal(self.grid, self.newgrid):
        print "No evolution is occuring stead-state static"
        self.playing = False
      elif numpy.array_equal(self.oldgrid, self.newgrid):
        print "No evolution is occuring: stead-state oscillatory"
        self.playing = False
      else:
        self.oldgrid = numpy.copy(self.grid)
        self.grid = numpy.copy(self.newgrid)
      if self.count == 2:
        self.playing = False

  def on_render(self):
    """"""
    if self.buildmenu == False:
      self.screenregions["menu"] = self.draw_menubar((0,0),(640,self.menubar_size-1))
      self.menubar["ui_tb_rules"] = self.draw_textbox((50,5),"Rules:",120, self.playing, self.ruleerror, self.rulefocus, self.rulestring)
      self.menubar["ui_rd_vonneumann"] = self.draw_radio((190,10), "von Neumann", self.neighborhood_select)
      self.menubar["ui_rd_moore"] = self.draw_radio((190,25), "Moore", not self.neighborhood_select)
      self.menubar["ui_tb_radius"] = self.draw_textbox((350,5), "Radius:", 35, self.playing, self.radiuserror, self.radiusfocus, self.radiusstring)
      self.menubar["ui_cb_self"] = self.draw_checkbox((485,5), False)
      self.menubar["ui_bn_play"] = self.draw_button((510,5), "Play/Pause", False)
      self.menubar["ui_bn_clear"] = self.draw_button((595,5), "Clear", False)
      self.buildmenu = True
    else:
      self.draw_menubar((0,0),(640,self.menubar_size-1))
      self.draw_textbox((50,5),"Rules:",120, self.playing, self.ruleerror, self.rulefocus, self.rulestring)
      self.draw_radio((190,10), "von Neumann", self.neighborhood_select)
      self.draw_radio((190,25), "Moore", not self.neighborhood_select)
      self.draw_textbox((350,5), "Radius:", 35, self.playing, self.radiuserror, self.radiusfocus, self.radiusstring)
      self.draw_checkbox((485,5), self.count_self)
      self.draw_button((510,5), "Play/Pause", False)
      self.draw_button((594,5), "Clear", False)

    if self.buildboard == False:
      (self.screenregions["board"],self.boardcells) = self.init_gameboard((0, self.menubar_size), self.board_dims)
      self.buildboard = True
    else:
      self.draw_gameboard((0, self.menubar_size), self.board_dims)

    pygame.display.flip()

  def on_cleanup(self):
    """"""
    pygame.quit()

  def on_execute(self):
    """"""
    if self.on_init() == False:
      self._running = False

    while( self._running ):
      for event in pygame.event.get():
        self.on_event(event)
      self.clock.tick(80)
      self.on_loop()
      self.on_render()
    self.on_cleanup()

  def draw_menubar(self, position, size):
    """"""
    gap = 2
    pygame.draw.rect(self._display_surf, pygame.Color("darkgrey"), position+size)
    pygame.draw.polygon(self._display_surf, pygame.Color("lightgrey"), [[0,0],[0,size[1]],[5,size[1]-5],[size[0]-5,5], [size[0],0]])
    menubar = pygame.draw.rect(self._display_surf, pygame.Color("grey"), (position[0]+gap, position[1]+gap, size[0]-(2*gap), size[1]-(2*gap)))
    return menubar

  def draw_textbox(self, position, text, width, isRunning, isError, isFocus, usertext):
    """"""
    size = (width, self.menubar_size-10)
    textspace = len(text)*7
    if isError:
      textbox = pygame.draw.rect(self._display_surf, pygame.Color("pink"), position+size)
    else:
      if not isRunning:
        textbox = pygame.draw.rect(self._display_surf, pygame.Color("white"), position+size)
      else:
        textbox = pygame.draw.rect(self._display_surf, pygame.Color("lightgrey"), position+size)
    if isFocus:
      pygame.draw.rect(self._display_surf, pygame.Color("green"), position+size, 1)
      self._display_surf.blit(self.fontobject.render(usertext+"|", 1, pygame.Color("black")), (position[0]+5,position[1]+7))
    else:
      pygame.draw.rect(self._display_surf, pygame.Color("black"), position+size, 1)
      self._display_surf.blit(self.fontobject.render(usertext, 1, pygame.Color("black")), (position[0]+5,position[1]+7))
    self._display_surf.blit(self.fontobject.render(text, 1, pygame.Color("black")), (position[0]-textspace,position[1]+7))
    return textbox

  def draw_radio(self, position, text, isSelected):
    """"""
    radio = pygame.draw.circle(self._display_surf, pygame.Color("white"), (position[0], position[1]),7)
    pygame.draw.circle(self._display_surf, pygame.Color("black"), (position[0], position[1]),7, 1)
    self._display_surf.blit(self.fontobject.render(text, 1, pygame.Color("black")), (position[0]+10,position[1]-6))
    if isSelected:
      pygame.draw.circle(self._display_surf, pygame.Color("black"), (position[0], position[1]),4)
    return radio

  def draw_checkbox(self, position, isChecked):
    """"""
    size = (15,15)
    text = "Count self?"
    textspace = len(text)*8
    checkbox = pygame.draw.rect(self._display_surf, pygame.Color("white"), (position[0], position[1]+6)+size)
    pygame.draw.rect(self._display_surf, pygame.Color("black"), (position[0], position[1]+6)+size, 1)
    self._display_surf.blit(self.fontobject.render(text, 1, pygame.Color("black")), (position[0]-textspace,position[1]+7))
    if isChecked:
      pygame.draw.rect(self._display_surf, pygame.Color("black"), (position[0]+3, position[1]+9)+(size[0]-6, size[1]-6))
    return checkbox

  def draw_button(self, position, text, isClicked):
    """"""
    textspace = len(text)*8
    size = (textspace, self.menubar_size-10)
    if isClicked == True:
      button = pygame.draw.rect(self._display_surf, pygame.Color("green"), position+size)
    else:
      button = pygame.draw.rect(self._display_surf, pygame.Color("lightgrey"), position+size)
    pygame.draw.rect(self._display_surf, pygame.Color("black"), position+size, 1)
    self._display_surf.blit(self.fontobject.render(text, 1, pygame.Color("black")), (position[0]+4,position[1]+7))
    return button

  def init_gameboard(self, position, size):
    """"""
    boardcells = {}
    gameboard = pygame.draw.rect(self._display_surf, pygame.Color("black"), position+size)
    for c in xrange(self.cols):
      for r in xrange(self.rows):
        boardcells[(r, c)] = pygame.draw.rect(self._display_surf, pygame.Color("white"), (c*self.grid_size, (r*self.grid_size)+self.menubar_size, self.block_size, self.block_size))
    return (gameboard, boardcells)

  def draw_gameboard(self, position, size):
    """"""
    pygame.draw.rect(self._display_surf, pygame.Color("black"), position+size)
    for c in xrange(self.cols):
      for r in xrange(self.rows):
        pygame.draw.rect(self._display_surf, pygame.Color(self.cellstates[self.grid[r,c]]), (c*self.grid_size, (r*self.grid_size)+self.menubar_size, self.block_size, self.block_size))
        if self.cellnumbers:
          self._display_surf.blit(self.fontobject.render(str(self.grid[r,c]), 1, pygame.Color("black")), (c*self.grid_size+4, (r*self.grid_size)+self.menubar_size+2))

  def check_clicked(self, position):
    """"""
    if not self.playing:
      self.ui_focus = "none"
      self.rulefocus = False
      self.radiusfocus = False
      for screenelement, screenregion in self.screenregions.items():
        if screenregion.collidepoint(position):
          if screenelement == "menu":
            for element, region in self.menubar.items():
              if region.collidepoint(position):
                exec "self."+element+"()"
                break
          elif screenelement == "board":
            for element, region in self.boardcells.items():
              if region.collidepoint(position):
                self.ui_cell_toggle(element)
                break
          else:
            break

  def ui_tb_rules(self):
    """"""
    if self.playing == False:
      self.ui_focus = "rulestring"
      self.rulefocus = True
    else:
      pass
  def ui_rd_vonneumann(self):
    """"""
    if self.playing == False:
      if self.neighborhood_select == True:
        pass
      else:
        self.neighborhood_select = True
    else:
      pass
  def ui_rd_moore(self):
    """"""
    if self.playing == False:
      if self.neighborhood_select == False:
        pass
      else:
        self.neighborhood_select = False
    else:
      pass
  def ui_tb_radius(self):
    """"""
    if self.playing == False:
      self.ui_focus = "radiusstring"
      self.radiusfocus = True
    else:
      pass
  def ui_cb_self(self):
    """"""
    if self.playing == False:
      if self.count_self == True:
        self.count_self = False
      else:
        self.count_self = True
    else:
      pass
  def ui_bn_play(self):
    """"""
    self.on_play()
  def ui_bn_clear(self):
    """"""
    self.on_clear()

  def ui_cell_toggle(self, cell):
    """"""
    self.grid[cell] = (self.grid[cell]+1)%self.totalcellstates

  def on_play(self):
    """"""
    self.ruleerror = False
    self.radiuserror = False
    rulepattern = re.compile("(([BS]|)\d*)/(([BS]|)\d*)")
    if not rulepattern.match( self.rulestring ):
      print "Bad rule format"
      self.ruleerror = True
      return -1
    self.rules  = self.inputToRules()

    radiuspattern = re.compile("\d{1}")
    if len(self.radiusstring) > 1 or not radiuspattern.match( self.radiusstring ):
      print "Bad radius format"
      self.radiuserror = True
      return -1
    self.radius = int(self.radiusstring)

    if self.playing == False:
      self.playing = True
      self.neighborhood = self.getNeighborhood()
    else:
      self.playing = False

  def on_clear(self):
    """reset the gamebaord to an empty state"""
    self.grid = numpy.zeros(self.cols*self.rows, dtype="int").reshape(self.rows, self.cols)
    self.newgrid = numpy.zeros(self.cols*self.rows, dtype="int").reshape(self.rows, self.cols)
    self.oldgrid = numpy.zeros(self.cols*self.rows, dtype="int").reshape(self.rows, self.cols)
    self.count = 0

  def inputToRules(self):
    """convert user input into a usable set of rules"""
    rules = re.split("/",self.rulestring)
    if len(rules) == 2:
      if len(rules[0]) < 1 or rules[0][0] != "B": #"S/B style:"
        birth = map(int,list(rules[1][:]))
        survive = map(int,list(rules[0][:]))
      else: #"B/S style:"
        birth = map(int,list(rules[0][1:]))
        survive = map(int,list(rules[1][1:]))
      return (birth, survive)
    else:
      print "Bad rule format"
      self.ruleerror = True
      return -1
 
  def getNeighborhood(self):
    """base on a neighborhood type and radius, determine the equation that describes all the neighbors locations"""
    neighborhood = "["
    for ry in xrange(-self.radius,self.radius+1,1):
      for rx in xrange(-self.radius,self.radius+1,1):
        if ((ry != 0) or (rx != 0)):
          if (self.neighborhood_select):
            if ((abs(rx) + abs(ry)) <= self.radius):
              arg = "".join(("scratchgrid[rr+",str(ry),",cc+",str(rx),"],"))
              neighborhood += "".join(arg)
            else:
              pass
          elif (not self.neighborhood_select):
            arg = "".join(("scratchgrid[rr+",str(ry),",cc+",str(rx),"],"))
            neighborhood += "".join(arg)          
    neighborhood = neighborhood[:-1]
    neighborhood += "".join("]")
    return neighborhood

  def evolveBoard(self):
    """evolve the gameboard one step"""
    scratchgrid = numpy.hstack((self.grid[:,-self.radius:], self.grid, self.grid[:,:self.radius]))
    scratchgrid = numpy.vstack((scratchgrid[-self.radius:,:], scratchgrid, scratchgrid[:self.radius,:]))
    scratchgrid2 = numpy.copy(scratchgrid)
    for c in xrange(self.cols):
      cc = c + self.radius
      for r in xrange(self.rows):
        rr = r + self.radius
        neighbors = eval(self.neighborhood)
        if self.count_self:
          neighbors = scratchgrid[rr, cc] + neighbors
        scratchgrid2[rr,cc] = self.updateCell(self.grid[r,c], neighbors)
    self.newgrid = scratchgrid2[self.radius:-self.radius,self.radius:-self.radius]
    del scratchgrid
    del scratchgrid2

  def updateCell(self, cellstate, neighbors):
    """given the state of a cell and its neighbors, based on some rules, update the cell"""
    birth, survive = self.rules
    if self.ruleset == "conway":
      if cellstate == 0:
        if neighbors.count(1) in birth:
          return 1 #"dead -> alive"
        else:
          return 0 #"dead -> dead"
      elif cellstate == 1:
        if neighbors.count(1) in survive:
          return 1 #"alive -> alive"
        else:
          return 0 #"alive -> dead"
      else:
        print "State not accounted for"
        self.playing = False
    elif self.ruleset == "brian":
      if cellstate == 0:
        if neighbors.count(1) in birth:
          return 1 #"dead -> alive"
        else:
          return 0 #"dead -> dead"
      elif cellstate == 1:
        return 2 #"alive -> dying"
      if cellstate == 2:
          return 0 #"dying -> dead"
      else:
        print "State not accounted for"
        self.playing = False
    elif self.ruleset == "wireworld":
      if cellstate == 0:
        return 0 # "empty space"
      elif cellstate == 1:
        return 2 # "electron head -> electron tail"
      elif cellstate == 2:
        return 3 #"electron tail -> conductor"
      elif cellstate == 3:
        if neighbors.count(1) in birth:
          return 1 #"conductor -> electron head"
        else:
          return 3 #"conductor -> conductor"
    else:
      print "Unknown ruleset."
      self.playing = False


if __name__ == "__main__" :
  PetriDish = Application()
  PetriDish.on_execute()

