uses my WoW addon to print data to screen to use, then takes this data from a screenshot, and uses that data to interact with the game<br>

important things to consider: WoWs API doesn't make it easy to make bots, for example even if I have a target, the UI won't give their position location, etc but there are other options. No Z-axis data, etc It helps to understand the game mechanics (can't tab target an enemy behind you, etc)

Bot can successfully follow a predefined path. I extrapolated the Angular Velocity graph using the time it takes to rotate at specific angles, this is important to make the bot go in the correct direction. There are two Angular Velocities, one for standing still and another for moving.<br>
Since we can't directly get the velocity of the bots (positional) speed, I got an average speed, but the speed of the bot is effected by the Z-axis, and since we can't get this data from in-game, we would have to use our screenshots to get reliable info on the bots current speed. Therefore it checks the bots position every second to see if its within a radius of the next point.<br>
Using this we can reliably get the bot to follow a path.<br>
