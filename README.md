uses a WoW addon to print data to screen to use, then takes this data from a screenshot, and uses that data to interact with the game<br>

``[[helps to understand the WoW API and the game mechanics.]]`` <br>

Bot can follow a predefined path. I extrapolated the Angular Velocity graph using the time it takes to rotate at specific angles, this is important to make the bot go in the correct direction. There are two Angular Velocities, one for standing still and another while moving.<br>

As bot follows a path it makes micro adjustments of the angle towards the point, if bot gets stuck it will jump. <br>

Using this we can reliably get the bot to follow a path, which I successfully was able to complete in `wowbot.py`<br>

Has a basic search enemy function that'll keep casting/pressing 1 until enemy state is dead.<br>

![data](https://github.com/user-attachments/assets/bc2066c4-fc69-4b4b-81aa-ac61f9fcb00d)
<br>(this is a screenshot that our program uses to get info about the player ingame: Health, Power, X, Y, Angle, Target, Casting)<br>

No Z-axis data available in UI. <br>

(Why this method of botting would be better than some of the alternatives:) No DLL injection, or altering the game process. With a little bit of randomization this method would have a low probability as being detected as a bot.
