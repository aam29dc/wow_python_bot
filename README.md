uses my WoW addon to print data to screen to use, then takes this data from a screenshot, and uses that data to interact with the game<br>

important things to consider: WoWs API doesn't make it easy to make bots, for example if I have a target, the UI won't give their position location, but there are other options.<br>
No Z-axis data. It helps to understand the game mechanics (like you can't tab target an enemy behind you, etc).

Bot can successfully follow a predefined path. I extrapolated the Angular Velocity graph using the time it takes to rotate at specific angles, this is important to make the bot go in the correct direction. There are two Angular Velocities, one for standing still and another while moving.<br>
Since we can't directly get the velocity of the bots (positional) speed, I got an average speed, but speed is effected by the Z-axis (since our speed was determined by (X,Y)), and since we can't get this (Z) data from in-game, we would have to use our screenshots to get reliable info on the bots current position. Therefore it checks the bots position every second to see if its within a radius of the next point.<br>
As bot follows a path it makes micro adjustments of the angle towards the point, since the point isn't exact it will contain a margin of error, and if bot gets stuck it will jump. There are ofc better methods if the bot gets stuck but this is fine for now.<br>
Using this we can reliably get the bot to follow a path, which I successfully was able to complete in `wowbot.py`<br>

![data](https://github.com/user-attachments/assets/bc2066c4-fc69-4b4b-81aa-ac61f9fcb00d)
<br>(this is a screenshot that our program uses to get info about the player ingame: Health, Power, X, Y, Angle, Target, Casting)

(Why this method of botting would be better than some of the alternatives:) No DLL injection, or altering the game process. With a little bit of randomization this method would have a low probability as being detected as a bot.
