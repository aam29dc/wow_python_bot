uses a WoW addon to print data to screen to use, then takes this data from a screenshot, and uses that data to interact with the game<br>

``[[helps to understand the WoW API and the game mechanics.]]`` <br>

Bot can successfully follow a predefined path. I extrapolated the Angular Velocity graph using the time it takes to rotate at specific angles, this is important to make the bot go in the correct direction. There are two Angular Velocities, one for standing still and another while moving.<br>

As bot follows a path it makes micro adjustments of the angle towards the point, since the point isn't exact it will contain a margin of error, and if bot gets stuck it will jump. There are ofc better methods if the bot gets stuck but this usually works. Like we could 180 around and go back, then try another angle, etc.<br>

Using this we can reliably get the bot to follow a path, which I successfully was able to complete in `wowbot.py`<br>


Has a basic search enemy function that'll keep casting/pressing 1 until enemy state is dead.<br>

![data](https://github.com/user-attachments/assets/bc2066c4-fc69-4b4b-81aa-ac61f9fcb00d)
<br>(this is a screenshot that our program uses to get info about the player ingame: Health, Power, X, Y, Angle, Target, Casting)<br>

No Z-axis data available. Speed is effected by the Z-axis, and since we can't get this (Z) data from in-game, we use our screenshots to get reliable info on the bots current position and speed.<br>

``[[Ideas]]``

Can implement paths easily by using WoWs maps (from a online database), then color code it in Paint to create paths read by the program. Then pull waypoints from the online db for quests, towns, etc. Bot would choose a path based on the position of the quest giver, etc. Would require some sort of trial and error testing on the paths or a good enough algorithm if bot gets stuck: If bot gets stuck we can simply go reverse and change slight direction on node of path, as of now the bot only jumps if stuck.

Write an algoritm that corrects paths in the map for no collisions, for self correcting behavior and a system that gets better over time rather than hardcoding. Start off with a path developed in the map, program reads it, stores the path, and bot uses it and self corrects nodes in path for no collision, and faster destination. <br>

If we use static elements in the UI, inventory management, going to vendors, learning new skills, etc can all be done. So basically a fully functional bot can be written using this method.<br>

The downsides: some elements of data aren't available for more accurate readings on gamestate, like the position of the target enemy their angle, etc A fix to this would be to turn to an angle that cannot attack the target and based on this angle we can derive an angle that would make our character look straight at the target. Some skills from classes in the game could make things easier. Again it helps to understand the WoW API and game mechanics when developing a bot this way.<br>

``[[no injections]]``
(Why this method of botting would be better than some of the alternatives:) No DLL injection, or altering the game process. With a little bit of randomization this method would have a low probability as being detected as a bot.
