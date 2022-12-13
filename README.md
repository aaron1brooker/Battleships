# Battleships

## High-Level Overview

Creating a Battleships game that supports multiple different game modes. 
1) A single-player game where the opposition is a simulated player.
2) A two-player game.
3) One player v computer (salvo - the number of shots per turn is determined by the number of ships the shooter has) game.
4) Two-player game (salvo) game.
5) One player v computer (hidden mines) game.
6) Two player game (hidden mines) game.
7) Computer v computer (hidden mines).

The code will be written in Python due to its flexible nature compared to a strongly typed language like C++. Another reason for the choice of the language is that Python also supports a game library called PyGame which can produce a UI for the user to play the game. This is a simple module that I have had experience with before hence why I have chosen this language. A negative of Python is that it is not that efficient compared to C++ however we do not have any low latency requirements and the program will be relatively small therefore it would not make a noticeable difference if we opted to use C++.

I will be developing in an agile methodology as I anticipate I will be adding additional features/updates to the game hence why I am choosing this approach.

Finally, I will be using GitHub as my version control. When I have finished developing a story, I will ensure that the development was on a different branch and then create a “pull request”. Usually, another developer would review this code however due to the nature of this being an academic project, I will review my own code carefully - to see if I can spot other ways of improving. I can also add descriptions on each pull request to allow the examiner to see what the “pull request” was trying to achieve.

## Stage 1 - Logically setting up the grid and allowing for user input

If you would like to understand more about this PR, please read the description:

https://github.com/aaron1brooker/Battleships/pull/1

I have also purposely not deleted the branch so for more insight on the code at this point look at:

https://github.com/aaron1brooker/Battleships/tree/grid-foundations

The stories related to this stage:

- Allow for the configuration file to be read and acted appropriately (e.g. setting variables to these values).
- Users can input where they want their ships placed.
- Print a grid to show where they are (Note: This needs to be very basic as we will advance it in the future of the project).

## Stage 2 - Basic game player vs computer

If you would like to understand more about this PR, please read the description:

https://github.com/aaron1brooker/Battleships/pull/2

I have also purposely not deleted the branch so for more insight on the code at this point look at:

https://github.com/aaron1brooker/Battleships/tree/basic-game-computer

The stories related to this stage:
- A simulated player can randomly place the boats correctly on the grid.
- A simulated/real player can make guesses about where the real player's boats are.
- A winner can be identified by an opponents boats all being destroyed.

## Stage 3 - MVP/Alpha Release

If you would like to understand more about this PR, please read the description:

https://github.com/aaron1brooker/Battleships/pull/3

I have also purposely not deleted the branch so for more insight on the code at this point look at:

https://github.com/aaron1brooker/Battleships/tree/alpha-game

The stories related to this stage:
- Create a Menu for the user to either choose quit or play game.
- Allow for real user to place unplaced and placed ships until user inputs continue
- Allow real user to auto place one or all ships.
- Give the user the option to move on from placing their ships as well as an option to look at the placing rules.
- Provide the user a grid for their guesses and show where they have hit or missed a boat.
- Allow the user to reset or quit the game at any time.


