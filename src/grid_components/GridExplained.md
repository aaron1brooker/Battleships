# Grid System

## Attempt 1 - Failed Implementation of Grid
The grid system took two iterations at the lower level design of how it was going to operate. My first idea, which I partially implemented, looked like this:

The grid is made up of two arrays either holding one or zero. Array one will correspond to the X axis and array two will correspond to the Y axis. To determine if a position on the grid is occupied is calculated by indexing into the x grid and the y grid arrays with the provided coordinates. If both of the values are 1 then this position would mean a boat is present. However, this led to problems when entering more than one boat as they would not correctly show, leading me to redesign this solution.

## Current Implemention of Grid
The grid is made up of a single-dimensional array where each index corresponds to a point in the grid. For example, if the grid was 3 by 3 then the array would hold 9 different indexes. Here is a visual representation:

[1,2,3,4,5,6,7,8,9]

- 1 2 3 
- 4 5 6
- 7 8 9

## The Logic

When the user is prompted to supply the coordinates of where they would like the boat placed, an example of a valid response would be “E1”. In order for the system to locate this position, it needs to find the index where the row values are present (e.g. using the grid above, if we wanted to find 5, the row values would be 4,5,6). Then it would add the letter value to find the index so that it can position the boat (e.g. 5 is the second in the row data so it would add 1). Here is how it looks in a pseudo form:

- y = POS Y
- x = CAPITALISE(POS X_alpha)
- x_num = CONVERT TO ASCII(x)
- x_num = x_num - 65	(65 is the ASCII integer for A so this will provide a number between 1 - 26)

- index_row = y * length of x axis
- index_value = index_row + x_num

Please note that the above example is an abstract representation. Feel free to read the code to see how it is actually done and handles other parameters like direction and size.
