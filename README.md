# WishiWashi_Game_Opencv
A simple game played on webcame for cleaning the windows. Based on opencv, Python.

To Run the game:

1) Open the dist folder
2) run game.exe
3) Follow the instructions on the command prompt.

Approach:

- The game uses webcamera (options for both internal and external are provided) for reading
  the frames in the real time. 

- I have used masking rather than motion detection and provided three options of cleaning 
  the windows( Hands, green or yellow color object)

- All the incoming frames are hazed by bitwise operation with the haze images in images 
  folder.

- Image is masked for the color of object and that much area is replaced with the webcame 
  frame through bitwise and segmentation operations.

- Portions of clock and percentage are included.

- Basic operations of fliping, drawing, contour detection are included. 
  
Download .rar file for full game (build files .exe)
