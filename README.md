# <ins> Adaship </ins>
<img src="https://user-images.githubusercontent.com/54953569/208610400-1f40ba59-a1cd-4357-9c99-1b3189157a2b.png" width="150" height="150">

This repository is for part of my submission for the Advance Programming Module Part B at Ada College.


It is recommended that you run this repository on a windows machine however, if you would like to use replit, please follow this link: 
https://replit.com/@aaron1brooker/Battleships-Replit-Version?v=1

This uses the branch https://github.com/aaron1brooker/Battleships/tree/replit-version. The only difference is that to clear the console in windows the command is "cls" but in replit it is "clear". This rectifies this issue.

### <ins> High-Level Overview/Challenge Outline </ins>

For this assignment, we were given the opportunity to create/expand upon the commonly known game ‘Battleships’ in a coding language of our choice. The requirements were organised into three separate milestones, each varying in complexity.

Our first milestone was to create a minimal viable product, which included a working Battleships game, a configuration file that would determine the grid size as well as the boats on the grid, and finally, a computerised opponent that used a random-based algorithm.

On completing this milestone, we could expand the application by adding an additional game mode called ‘Salvo Battleships’ and improve the grid's capabilities so that it could support grid dimensions between 5x5 and 80x80. 

Our end goal for the application was the ‘Beta Release’ - the third milestone of the project. In order to complete this milestone, we were required to create another game variant of Battleships called ‘Hidden Mines’, have an improved computer player that would not work on a purely random-based strategy and be able to dynamically add or delete boats within the configuration file. 

It is to note that we as the developers were not limited to these requirements and were able to add additional functionality if we felt that it would help improve the overall quality of the game.

#### <ins> Proposed Solution </ins>

The core element of this project was the grid itself because each different variant of the Battleships game would require making use of it. I wanted to ensure that all complexity of the grid would be abstracted from the user. This meant that all they would have to do to interact with the grid was input the coordinates. The coordinates would be made up of the x-axis (a letter-based system) and the y-axis (a number-based system). Luckily, the y component of the graph would be no problem when handling dimensions of up to 80 rows however, unfortunately, the x-axis would not be so simple. I ended up deciding that I would follow a similar concept to Microsoft Excel Spreadsheets where once the columns are greater than 26, it will add an additional letter. This is also a similar system to what hexadecimal uses when representing a value.

In addition to the grid, the next vital component of the game was the player themselves (either computerised or not). I realised that the grid and the player would both be linked quite heavily as each player would have their own grid. Therefore, I decided that these two components would share the same class so that they could work together. Furthermore, I felt that both the computerised player and the real player would also be linked and share the same class because, in the requirements, both players would be required to automatically place and guess ships on the grid.

These components, as well as the game class itself, would conclude the front-end of the project however, I still had one element left to plan and that was the configuration file. I wanted to ensure that this would be separate from the front-end components as the functionality differs quite a lot. Hence, in the ‘backend’ there would be, the configuration/game setup components as well as a potential database that would store the high scores of each player when playing the game.

In order for the reader to visualise these components better, I have created a UML Diagram to show how I originally planned to have this game setup:

<img src="https://user-images.githubusercontent.com/54953569/208611972-88d756c5-0867-4937-8321-83d9fe8e4d09.png" width="500" height="500">

#### <ins> Development Plan </ins>

As the UML diagram illustrates, there is a lot of work required to get this project finished within the time frame. That being the case, I decided to use an Agile methodology because I could then add these extra features incrementally. This also meant that, if time constraints did become an issue, then I would still have a working product as each ‘version’ of the sprint would be a working product that I could submit.

Furthermore, because of these time constraints, I wanted to use a programming language that was highly adaptable and simple to use - this led me to Python. I did consider using C++ as I enjoy using the strong types that the language enforces because it can catch out errors as well as provide a powerful intellisense. However, I was able to supplement Python with a module from typing that would allow me to declare types for variables which resulted in my developer experience being much more enjoyable.

Finally, I decided to use GitHub as my version control. When I had finished developing an epic (a stage of development), I ensured that the new commits were on a different branch and then create a “pull request”. Usually, another developer would have reviewed this code however due to the nature of this being an academic project, I reviewed my own code carefully - to see if I could spot other ways of improving. I also added descriptions on each pull request to allow the reader of this documentation to see what the “pull request” was trying to achieve.

### <ins> My Development Journey </ins>

My primary focus of this project was to adopt a good coding standard so that it would be easy to maintain and add additional features in the future. I decided to write a list of the best practices for embarking on Python projects so that I could always refer to it throughout my development journey:

- The naming convention needs to be consistent (Snake case for variables and functions. Pascal case for classes).
- Appropriate comments to describe what the algorithm is trying to do. Also, provide a description for each method to explain what it is doing.
- Where possible, use the imported types module for the inputs and outputs of methods.
- Encapsulate the relevant files in an appropriately named directory.
- Try to keep the overall solution to a low complexity. This is important because it is a game that the user interacts with and therefore they do not want it to be slow as it could be frustrating.

As mentioned, I created a pull request for each epic. In each linked pull request, you will see all the relevant commits, a diagram or pseudo code to illustrate the key components of the epic and finally, a quick description of what I found most challenging in the epic. I have also purposely not deleted the branch so that anyone can look at the code's state at different times of the lifecycle of this project.

#### <ins> Epic/Stage 1 - Logically setting up the grid and allowing for user input </ins>

Pull request - https://github.com/aaron1brooker/Battleships/pull/1 <br />
Code Branch - https://github.com/aaron1brooker/Battleships/tree/grid-foundations

Stories that relate to this epic:
- Allow for the configuration file to be read and acted appropriately (e.g. initialising variables to these values).
- Users can input where they want their ships placed.
- Print a grid to show where they are (Note: This needs to be very basic as we will advance it in the future of the project).

A quick video demonstration of what this epic achieved:

https://user-images.githubusercontent.com/54953569/208616176-9c065f1d-7e06-43eb-88d7-de22ba585a6e.mp4

As you can see on the code branch, I created the fundamental classes for the game which were the player's grid and game setup. To elaborate on my comment mentioning that the most challenging part of this epic was the ‘grid mechanics’, I feel that the reason why I was getting stuck initially was that I was trying to over-engineer the problem which led me to failure. In fact, the solution I ended up going with was far simpler (one array which held each position of the grid) and could be understood easier, leading to a more maintainable code base. To understand more, I would recommend reading my [GridExplained.md](https://github.com/aaron1brooker/Battleships/blob/main/src/grid_components/GridExplained.md) up to and including the header ‘The Logic V1’. 

#### <ins> Epic/Stage 2 - Player v Computer Basic Game </ins>

Pull Request - https://github.com/aaron1brooker/Battleships/pull/2 <br />
Code Branch - https://github.com/aaron1brooker/Battleships/tree/basic-game-computer

Stories that relate to this epic:
- A simulated player can randomly place the boats correctly on the grid.
- A simulated/real player can make guesses about where the opponent's boats are.
- A winner can be identified by an opponent's boats all being destroyed.

A quick demonstration of what this epic achieved:

https://user-images.githubusercontent.com/54953569/208618141-fbda0334-891d-4f86-b4ca-88c8cfaff265.mp4

This was by no means the finished product however it was a starting point for the game. What I realised after developing this epic was that I needed to allow the user to track their guesses as currently, a user would have to physically write down the position and outcome. This however was planned as mentioned at the planning stage but I wanted to isolate this component in a different epic.

Also, you can see that I made a small comment on the pull request mentioning to add a description for the method. This shows how I was trying to maintain good coding practises as I wanted to ensure that a stranger to the project would be able to understand what was going on.

Once again, please read the pull request description to see what I found most challenging in the epic.

#### <ins> Epic/Stage 3 - MVP/Alpha Release </ins>

Pull Request - https://github.com/aaron1brooker/Battleships/pull/3 <br />
Code Branch - https://github.com/aaron1brooker/Battleships/tree/alpha-game
 
Stories that relate to this epic:
- Create a Menu for the user to either choose quit or play game.
- Allow for a real user to place unplaced and placed ships until user inputs continue
- Allow a real user to auto-place one or all ships.
- Give the user the option to move on from placing their ships as well as an option to look at the placing rules.
- Provide the user with a grid for their guesses and show where they have hit or missed a boat.
- Allow the user to reset or quit the game at any time.
 
A quick demonstration of what this epic achieved:

https://user-images.githubusercontent.com/54953569/208619219-2b1fda14-2aa2-44f4-8169-0669be97c54a.mp4

In this epic, I essentially wanted to ‘complete’ the traditional version of battleships - this led to many stories. To prevent myself from losing track of how the game would work, I decided to create a high-level overview of the game in the form of a flow chart - this can be found in the pull request description. It meant that when I wanted to test my solution, I could follow this flowchart and see whether it was running correctly.

Throughout this project, I always tested my solution regularly as I was following the concept of ‘fail fast resolve effectively’. This meant that no serious bugs would ever come to light as they would always be caught early.

In addition to ‘what I found most challenging’ was the refactoring element. The reason is that it is hard to find the right balance between concise code as well as understandable code. That is why I tried to follow, as much, the rule of one line one instruction. However, sometimes I would break this rule if I felt that it was directly related, e.g. making the users input upper case.


#### <ins> Epic/Stage 4 - Salvo Game and Increased Board Size </ins>

Pull Request - https://github.com/aaron1brooker/Battleships/pull/4 <br />
Code Branch - https://github.com/aaron1brooker/Battleships/tree/salvo-game

Stories that relate to this epic:
- The game needs to be able to support up to 80 columns and rows.
- Implement the ‘Salvo’ variant of Battleships (player v computer).
- Add an autofire option to both games.
- Implement two-player Battleships.
- Implement two-player Salvo Battleships.

A quick demonstration of what this epic achieved:

https://user-images.githubusercontent.com/54953569/208620379-ed164115-51cb-4d0b-86a6-38f58f0f006e.mp4

This epic was definitely challenging as I had to enhance the current grid system to allow columns and rows of up to 80. To explain how I did this, I would recommend reading the last two headers of [GridExplained.md](https://github.com/aaron1brooker/Battleships/blob/main/src/grid_components/GridExplained.md).


#### <ins> Epic/Stage 5 - Hidden Mines Battleships </ins>

Pull Request - https://github.com/aaron1brooker/Battleships/pull/5 <br />
Code Branch - https://github.com/aaron1brooker/Battleships/tree/beta-release

Stories that relate to this epic:
- Allow for mines to be auto placed without the players seeing their position.
- Create a method that would calculate the positions affected if a mine was hit.
- Encapsulate these new methods into a class and allow the user to play the new Battleships variant, Hidden Mines.

A quick demonstration of what this epic achieved:

https://user-images.githubusercontent.com/54953569/208621310-eeaef56d-97bc-464f-956d-939dd6bc334d.mp4

This epic was the most challenging aspect of the whole project in my opinion and unfortunately led me to not be able to finish all requirements that I set out in my plan (this will be discussed later). Please read the pull request description for more information.

### <ins> Evaluation </ins>

#### <ins> Refactoring Showcase </ins>

Throughout the process of creating this project, I would always refactor as I went along because this strategy works better for me. However, there were some cases where I would first, purely focus on the problem to solve then refactor/clean up the code after.

In the example I am about to share of where I refactored, I need to provide some context first. When creating the additional Salvo Battleships game, I realised that both games would place boats in the same way. Therefore, I decided to capitalise on using inheritance because I would then be able to write the one method which could be shared over the two different child classes.

The first link below will take you to the pre-parent class addition and the second will be the post-parent class addition.

Note - even though you may not think much has been refactored here, please bare in mind that the other game class would also be longer plus, additional features had been added in the post-refactored link

Not Refactored:
https://github.com/aaron1brooker/Battleships/blob/alpha-game/src/games/traditional_battleships.py#L11

Refactored:
https://github.com/aaron1brooker/Battleships/blob/main/src/games/traditional_battleships.py#L12

In regards to code refactoring and ‘cleaning up’ code, I wanted to mention that throughout the project, I would always use the code formatter “Black”. This meant that all my code looked and followed the same principle creating an easier environment for other developers to read my code.

#### <ins> Advanced Programming Principles </ins>

In this project, I believe that I have showcased many Advanced Programming Principles and the code base is a good example for other projects to go by. My reasons for this are as follows:

- As previously mentioned in the refactoring part of this documentation, I have used inheritance with classes. In each main component where there is a class, there will be a parent class and child classes. The motivation behind this was to minimize repeated code as well as allow for future games to be easily added. This is because you can simply inherit all of the key components from the parent class, e.g. in the class ‘PlayerGrid’, and use its methods. Therefore, you do not need to rewrite any functions and add to the current system which will also make the implementation of a new feature easier. (Example 1 - https://github.com/aaron1brooker/Battleships/blob/main/src/games/salvo_battleship.py, Example 2 - https://github.com/aaron1brooker/Battleships/blob/main/src/grid_components/mines_grid.py)
- Another good example of these principles are using types to highlight the input and output of functions. I think this because, when maintaining a project, I have felt that knowing what it is returning is useful to help understand more about what is going on as a whole. <img src="https://user-images.githubusercontent.com/54953569/208622258-482e752f-b85a-4a7a-9743-fdc8f8d111e1.png" width="500" height="75">

- The final principle I would like to showcase is the logging system. Even though it is a simple implementation of it, I have found that it has been extremely useful when debugging problems. Unfortunately, mistakes can be made when programming and bugs can be created, that's why logging the reason why something has gone wrong will allow us as advanced programmers to debug the problem quicker. <img src="https://user-images.githubusercontent.com/54953569/208623149-1e79e324-26d5-4efc-9b9e-c1c6fed317c9.png" width="500" height="75">

#### <ins> Improved Algorithms and Reflection </ins>

Sadly, I was unable to complete all the requirements that I had originally set out due to time constraints however this is not all negative. If I developed with the Waterfall methodology, I wouldn't have a finished program therefore this shows the importance of using an Agile approach if working under pressure as you will at least be able to deliver something.

On the other hand, if I did do this project again, I would take into consideration the latter requirements at the start and figure out how it would all work. This was because I felt that a large portion of my time was planning each algorithm. If I did a majority of the planning at the start rather than in phases, this could have allowed me to finish all of the requirements.

Even though I did not improve the computerised player, I still researched how I could have improved it. This would have been done by using the ‘Hunt Algorithm’ which explores nearby spaces once the computer player has randomly hit a boat. The interesting part is that most humans when playing Battleships follow this concept. Therefore this could have resulted in a more exciting game to play with a tougher opponent.

Overall I enjoyed this project as there were plenty of challenges along the way and it allowed me to test my capabilities in problem-solving.
