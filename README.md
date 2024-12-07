first test of a wow bot, nothing special yet, at most can stand in one place and find a target to attack.<br>
uses a WoW addon to print data to screen, then take data from screen, and use that data to interact with the game<br>

basic structure:
  tab till find a target that is attackable
    attempt to attack target
      if can't attack target then either out of range or wrong direction
        change direction
          try again
