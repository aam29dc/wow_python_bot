first test of a wow bot, nothing special yet, at most can stand in one place and find a target to attack and clicks the `1` ability on toolbar<br>

uses a WoW addon to print data to screen to use, then takes that data from the screen, and uses that data to interact with the game<br>

important things to consider: WoWs API doesn't make it easy to make bots, for example even if I have a target, the UI won't give their position location (from what I've researched so far..), etc but there are other options

basic (attack) structure:
  tab till find a target that is attackable
    attempt to attack target
      if can't attack target then either out of range or wrong direction
        change direction
          try again
