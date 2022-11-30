# Grid System

At the lower level, the grid is made up of two arrays either holding one or zero. Array one will correlate to the X axis and array two will correlate to the Y axis.

## The Logic

In order to check/place a boat, there is some logic that can calculate the index required for each array. Here is the formula to insert a boat of length 1:

- y = POS Y
- x = CAPITALISE(POS X_alpha)
- x_num = CONVERT TO ASCII(x)
- x_num = x_num - 65	(65 is the ASCII integer for A so this will provide a number between 1 - 26)

- arr_x_axis[x_num] = 1
- arr_y_axis[y] = 1


Therefore now, if we wanted to check if a certain position has a ship present, we can follow a similar procedure however check if these two values from the arrays are a 1.