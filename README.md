first test of a wow bot, at most can stand in one place and find a target to attack

basic structure:
  tab till find a target that is attackable
    attempt to attack target
      if can't attack target then either out of range or wrong direction
        change direction
          try again
