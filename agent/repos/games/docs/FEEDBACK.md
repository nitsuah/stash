# games feedback

## Arcade main

- the arcade "pink" top section is too low on mobile (might be top padding) so it overlaps too far into the play section of the main screen.
- on mobile the titles of the games are a bit too big and wrap down into the card and get kind of truncated. maybe make the titles a bit smaller on mobile or reduce the padding between the grid tiles and the cards or the top section "selection your game" and the grid of game cards.
- the bottom part of the arcade has too much left/right/side padding and should extend the full width of the screen on mobile. the bottom section is also a bit too tall and should be reduced in height a bit (or the bottom padding removed) so that the orange segment of the joystick/buttons/coininsert are just closer to the bottom of the screen (just remove the bottom padding slightly).

## Game Input Standardization

For our games we need to rework some of the landscape vs portrait orientation and adding different standard inputs for mobile. we also need to standardize our pause menu and buttons that appear on the top (during portrait mode) and buttons that should appear on the top bar or left as settings buttons when in landscape mode. more detaisl for all games below.

## Asteroids

- should load in landscape perspective on mobile and not portrait. the game is designed to be played in landscape and should load that way by default. if the user rotates their phone to portrait, it should show a "please rotate your phone" message or something like that. also add two joy sticks. one to control WASD movement and one to control the mouse aiming. the mouse aiming should be a virtual joystick that is a bit larger than the movement joystick and should be on the right side of the screen. the movement joystick should be on the left side of the screen. also add a "shoot" button on the right side of the screen that is above the aiming joystick. also add a "pause" button in the top right corner of the screen that pauses the game and shows a pause menu with options to resume, restart, or quit to main menu. there should also be a "reload" button. make these similar to the "settings" button that already exists.

## FPS game

- same as asteroids, landscape and both joysticks. make these  re-usable components that we can re-use in other 3d input games. also add a "shoot" button on the right side of the screen that is above the aiming joystick. also add a "pause" button in the top right corner of the screen that pauses the game and shows a pause menu with options to resume, restart, or quit to main menu. there should also be a "reload" button. make these similar to the "settings" button that already exists.

## Breakout - Touch input

- add a "pause" button in the top right corner of the screen that pauses the game and shows a pause menu with options to resume, restart, next to the current "back" to main menu button. there should also be a "reload" button. make these similar to the "settings" button that already exists. use icons instead of text to optimize for mobile. make these a re-usable component that can be used in all the games.
- the game should respond to touch input on mobile. the paddle should follow the user's finger on the screen. if the user touches the left side of the screen, the paddle should move left. if the user touches the right side of the screen, the paddle should move right. if the user touches and holds their finger on the screen, the paddle should stay in that position until they lift their finger. if the user swipes their finger left or right, the paddle should move in that direction at a speed proportional to the swipe speed. make it intuitive and responsive to touch input.

## space invaders - Plus Pad & Points

- add "point" indicators when the user successfully hits an enemy. the points should appear above the enemy and float up and fade out. also add our re-usable "pause", restart, back to arcade buttons in the top right corner of the screen that pauses the game and shows a pause menu with options to resume, restart, next to the current "back" to main menu button. there should also be a "reload" button. make these similar to the "settings" button that already exists. use icons instead of text to optimize for mobile. make these a re-usable component that can be used in all the games.
- PLUS PAD - like a gameboy color - add a shoot button to the right side of the lower section of the screen (or the far right side of the screen on mobile landscape) and also a + paddle that responds to user input like a Gameboy color. make this a re-usable component that can be used in all the games. the paddle should respond to touch input on mobile. the paddle should follow the user's finger on the screen. if the user touches the left side of the screen, the paddle should move left. if the user touches the right side of the screen, the paddle should move right. if the user touches and holds their finger on the screen, the paddle should stay in that position until they lift their finger. if the user swipes their finger left or right, the paddle should move in that direction at a speed proportional to the swipe speed. make it intuitive and responsive to touch input. if the user presses on the top part of the + pad it hsould move the player upwards and vice versa for downwards. if the user presses on the left part of the + pad it should move the player left and vice versa for right. if the user presses on the center of the + pad it should stop the player from moving in any direction. make this a re-usable component that can be used in all the games.

## Flappy bird

- the "how to play" appears too big and overlaps the game on portrait mode on mobile. it doesnt need to appear by default. just show a "start game" button instead. also make the "how to play" smaller and more compact so that it doesn't overlap the game. also add our re-usable "pause", restart, back to arcade buttons in the top right corner of the screen that pauses the game and shows a pause menu with options to resume, restart, next to the current "back" to main menu button. there should also be a "reload" button. make these similar to the "settings" button that already exists. use icons instead of text to optimize for mobile. make these a re-usable component that can be used in all the games.
