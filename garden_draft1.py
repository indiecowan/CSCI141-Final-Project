# Author: Indie Cowan
# Date: March 5
# Description: Program takes user name and preferred turtle color and then sets user free to meander around a flower-filled garden as a turtle using the arrow keys. Once user is done, they press 'x' on the keyboard and the number of steps is displayed. Once they press enter to end, their info is written to the leaderboard and is then sorted to be displayed the next time the game is started up.
import turtle
from functools import partial
import random

##### FUNCTIONS #####

def draw_rectangle(t, width, height):
    """ Draw a rectangle using turtle t with size width x height
        Precondition: t’s pen is down
        Postcondition: t’s position and  orientation are the same as before
    """
    for i in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)

def draw_polygon(t, side_length, num_sides):
    """ Draw a polygon with num_sides sides, each with length side_lengthusing turtle t
        Precondition: t’s pen is down; num_sides > 2
        Postcondition: t’s position and orientation are the same as before
    """
    angle_turn = 360 / num_sides

    for i in range(num_sides):
        t.forward(side_length)
        t.left(angle_turn)

def draw_snowflake(t, side_length, num_sides):
    """ Use t to draw a snowflake made of ngon-sided polygons. The snowflake contains 10 copies of a polygon with
        num_sides and side_length, each drawn at a 36-degree angle from the previous one.
        Postcondition: t’s position and orientation are the same as before
    """
    for i in range(10):
        draw_polygon(t, side_length, num_sides)
        t.left(36)

def sort_leaderboard(file_name):
    """ Sorts a file from the third item in each line from biggest to smallest.
        Arguements: file_name must be a file that consists of lines with three space-separated strings each, the last being a number.
        Effects: Changes the passed-in file so that it is sorted.
    """

    # create list of lines that turn into lists with each item in a line
    file_lines = []
    with open(file_name, "r") as info_file:
        for line in info_file:
            file_lines.append(line.split())

    # sort lines into new list by number in 2nd index
    sorted_lines = []
    for file_line in file_lines:
        final_index = 0
        for sorted_line in sorted_lines:
            if int(file_line[2])<int(sorted_line[2]):
                final_index += 1
            else:
                break
        sorted_lines.insert(final_index, file_line)

    print(sorted_lines)

    # rewrite file so that it is now sorted
    #count how many lines are in file
    with open(file_name, "r") as info_file:
        file_line_count = 0
        for line in info_file:
            file_line_count+=1
    # rewrite, doing new line every time except for the last line
    with open(file_name, "w") as info_file:    
        lines_written = 0
        for info_list in sorted_lines:
            for item in info_list:
                info_file.write(item)
                info_file.write(" ")
            lines_written+=1
            if lines_written < file_line_count:
                info_file.write("\n")



def user_color_invalid(user_color):
    """ Takes a color and returns True if the color is invalid (not in the approved list  of colors in-function) and False if the color is valid.
    """
    colors = ("red", "orange", "yellow", "green", "blue", "purple")
    if user_color in colors:
        result = False
    else:
        result = True
    return result

def create_wn_variables(t, wn):
    """ Uses window attributes and turtle coordinates to create variables that are the x and y coordinates of the lower left corner of the window and the x and y coordinates of the upper right corner of the window.
        arguements: t- a turtle (the user's turtle), wn- the window the turtle is in
        returns: a tuple containing the llx, lly, urx, and ury in that order
    """
    wn_llx = -wn.window_width()/2 + t.xcor()
    wn_lly = -wn.window_height()/2 + t.ycor()
    wn_urx = wn.window_width()/2 + t.xcor()
    wn_ury = wn.window_height()/2 + t.ycor()
    return (wn_llx, wn_lly, wn_urx, wn_ury)

def get_new_tcoords(wn_llx, wn_lly, wn_urx, wn_ury):
    """ Uses the new coordinates of a window to find the coordinates that will center the turtle in the window again.
        Arguements: wn_llx- the lower left x coordinate of the window, wn_lly- the lower left y coordinate of the window, wn_urx- the upper right x coordinate of the window, wn_ury- the upper right y coordinate of the window
        Returns: A tuple containing the x and y coordinates that center the turtle in the window in that order.
    """
    new_x = (wn_llx + wn_urx)/2
    new_y = (wn_lly + wn_ury)/2
    return (new_x, new_y)

def create_up(t, wn, user_information):
    """ A function meant to be passed into a partial that will move the turtle passed in UP by 12px (unless the turtle is at the wall), and add a step to the user's information. 
        Arguements: t- the turtle to be 'moved' (it will move relative to the background but the window coordinates will be reset to turtle is always in the middle of the screen) wn- the window to be readjusted, user_information- the dictionary whose 2nd index contains the amount of steps the user has taken
        Effects: The coordinates of the canvas within the window will be readjusted (DOWN by 12px) so that it looks like turtle is moving. 
    """
    # turn turtle in right direction
    t.setheading(90)    

    # get window attributes
    wn_llx, wn_lly, wn_urx, wn_ury = create_wn_variables(t, wn)

    # move window/turtle if fence isn't blocking
    if t.ycor() < 970:
        print("wn_lly is", wn_lly, "so up")
        wn_lly += 12
        wn_ury += 12
        print("create_up says: llx:", wn_llx, "lly:", wn_lly, "urx:", wn_urx, "ury:", wn_ury )
        x, y = get_new_tcoords(wn_llx, wn_lly, wn_urx, wn_ury)
        wn.setworldcoordinates(wn_llx, wn_lly, wn_urx, wn_ury)
        t.goto(x,y)
        user_information["steps"] += 1
    else:
        print("wn_lly is", wn_lly, "so stays put")
    
    wn.update()
    

def create_down(t, wn, user_information):
    """ A function meant to be passed into a partial that will move the turtle passed in DOWN by 12px (unless the turtle is at the wall), and add a step to the user's information. 
        Arguements: t- the turtle to be 'moved' (it will move relative to the background but the window coordinates will be reset to turtle is always in the middle of the screen) wn- the window to be readjusted, user_information- the dictionary whose 2nd index contains the amount of steps the user has taken
        Effects: The coordinates of the canvas within the window will be readjusted (UP by 12px) so that it looks like turtle is moving. 
    """

    # turn turtle in right direction    
    t.setheading(270)

    # get window attributes
    wn_llx, wn_lly, wn_urx, wn_ury = create_wn_variables(t, wn)

    # move window/turtle if fence isn't blocking
    if t.ycor() > -970:
        print("wn_lly is", wn_lly, "so down")
        wn_lly -= 12
        wn_ury -= 12
        print("create_down says: llx:", wn_llx, "lly:", wn_lly, "urx:", wn_urx, "ury:", wn_ury )
        x, y = get_new_tcoords(wn_llx, wn_lly, wn_urx, wn_ury)
        wn.setworldcoordinates(wn_llx, wn_lly, wn_urx, wn_ury)
        t.goto(x,y)
        user_information["steps"] += 1
    else:
        print("wn_lly is", wn_lly, "so stay put")

    wn.update()

def create_left(t, wn, user_information):
    """ A function meant to be passed into a partial that will move the turtle passed in LEFT by 12px (unless the turtle is at the wall), and add a step to the user's information. 
        Arguements: t- the turtle to be 'moved' (it will move relative to the background but the window coordinates will be reset to turtle is always in the middle of the screen) wn- the window to be readjusted, user_information- the dictionary whose 2nd index contains the amount of steps the user has taken
        Effects: The coordinates of the canvas within the window will be readjusted (RIGHT by 12px) so that it looks like turtle is moving. 
    """

    # turn turtle in right direction 
    t.setheading(180)

    # get window attributes
    wn_llx, wn_lly, wn_urx, wn_ury = create_wn_variables(t, wn)

    # move window/turtle if fence isn't blocking
    if t.xcor() > -970:
        print("wn_llx is", wn_llx, "so left")
        wn_llx -= 12
        wn_urx -= 12
        print("create_left says: llx:", wn_llx, "lly:", wn_lly, "urx:", wn_urx, "ury:", wn_ury )
        x, y = get_new_tcoords(wn_llx, wn_lly, wn_urx, wn_ury)
        wn.setworldcoordinates(wn_llx, wn_lly, wn_urx, wn_ury)
        t.goto(x,y)
        user_information["steps"] += 1
    else:
        print("wn_llx is", wn_llx, "so stay put")

    wn.update()

def create_right(t, wn, user_information):
    """ A function meant to be passed into a partial that will move the turtle passed in RIGHT by 12px (unless the turtle is at the wall), and add a step to the user's information. 
        Arguements: t- the turtle to be 'moved' (it will move relative to the background but the window coordinates will be reset to turtle is always in the middle of the screen) wn- the window to be readjusted, user_information- the dictionary whose 2nd index contains the amount of steps the user has taken
        Effects: The coordinates of the canvas within the window will be readjusted (LEFT by 12px) so that it looks like turtle is moving. 
    """

    # turn turtle in right direction
    t.setheading(0)

    # get window attributes
    wn_llx, wn_lly, wn_urx, wn_ury = create_wn_variables(t, wn)

    # move window/turtle if fence isn't blocking
    if t.xcor() < 970:
        print("wn_llx is", wn_llx, "so right")
        wn_llx += 12
        wn_urx += 12
        print("create_right says: llx:", wn_llx, "lly:", wn_lly, "urx:", wn_urx, "ury:", wn_ury )
        x, y = get_new_tcoords(wn_llx, wn_lly, wn_urx, wn_ury)
        wn.setworldcoordinates(wn_llx, wn_lly, wn_urx, wn_ury)
        t.goto(x,y)
        user_information["steps"] += 1
    else:
        print("wn_llx is", wn_llx, "so stay put")

    wn.update()

def create_done(t, wn, user_information):
    """ Ties up all the loose ends and finishes the program. Adds user's info to the leaderboard, tells the user their step count, sorts the leaderboard and then ends the program.
    """

    # write user info to file
    with open("final_project/CSCI141/player_info.txt", "a") as info_file:
        info_file.write("\n")
        for key in user_information:
            info_file.write(str(user_information[key]))
            info_file.write(" ")

    # show user steps
    prompt = "You took "+ str(user_information["steps"]) + " steps! Press enter to end program."
    wn.textinput("garden says:", prompt)

    # sort the leaderboard and close program
    sort_leaderboard("final_project/CSCI141/player_info.txt")
    exit()


def turtle_listen(t, wn, user_information):
    """ Sets window up so that it's listening for correct key movements and will execute functions on arrow keys as well as 'x' on the keyboard.
        Arguements: t- main user turtle, wn- main screen user is on, user_information: dictionary with user info (2nd index must me steps)
    """
    
    # make window listen
    turtle.listen()
    
    # create functions with predetermined arguements
    up = partial(create_up, t, wn, user_information)
    down = partial(create_down, t, wn, user_information)
    left = partial(create_left, t, wn, user_information)
    right = partial(create_right, t, wn, user_information)
    done = partial(create_done, t, wn, user_information)

    # specify which keys do what
    wn.onkey(up, "Up")
    wn.onkey(down, "Down")
    wn.onkey(left, "Left")
    wn.onkey(right, "Right")
    wn.onkey(done, "x")

def create_garden(wn):
    """ Draws garden with grey fence, green background and flowers with dimensions of about 2000px * 2000px.
        Arguements: wn- a turtle screen variable
    """

    #create the turtle that will draw, set no animation and make background brown
    garden_turtle = turtle.Turtle()
    wn.tracer(0, 0)
    wn.bgcolor("SaddleBrown")

    # color garden ground green
    garden_turtle.width(20)
    garden_turtle.color("forestgreen")
    for i in range(100):
        #lets make the garden 2000 by 2000
        garden_turtle.setheading(0)
        garden_turtle.penup()
        garden_turtle.goto(-992, 990-(i*20))
        garden_turtle.pendown()
        garden_turtle.forward(1982)

    #draw fence
    heading = 0
    garden_turtle.width(10)
    garden_turtle.color("grey")
    for i in range(-1000, 1001, 2000):
        for j in range(-1000, 1001, 2000):
            garden_turtle.penup()
            garden_turtle.goto(i, j)
            garden_turtle.setheading(heading)
            garden_turtle.pendown()
            garden_turtle.forward(2000)
            if heading == 0:
                heading = 270
            elif heading == 270:
                heading = 90
            else:
                heading = 180

    #draw flowers
    garden_turtle.pensize(3)
    colors = ("red", "orange", "blue", "yellow", "blue", "purple")
    x_range = 900
    y_range = 900
    for i in range(70):

        #decide random qualities
        x = random.randint(-x_range, x_range + 1)
        y = random.randint(-y_range, y_range + 1)

        #draw flower stem
        garden_turtle.penup()
        garden_turtle.goto(x, y)
        garden_turtle.pendown()
        garden_turtle.color("darkgreen")
        draw_rectangle(garden_turtle, 3, 60)

        #draw flower petals
        sidelength = random.randint(20, 30)
        garden_turtle.color(colors[random.randint(0,5)])
        garden_turtle.penup()
        garden_turtle.goto(x, y)
        garden_turtle.pendown()
        draw_snowflake(garden_turtle, sidelength, 3)

    wn.update()

def main():
    # set up the window and create user turtle
    wn = turtle.Screen()
    wn.mode("world")
    wn.title("garden")
    user = turtle.Turtle()
    user.width(4)
    user.speed(0)
    user.shape("turtle")
    create_garden(wn)
    wn.tracer(0,0)
    
    # display leaderboard/past players
    leaderboard = []
    with open("final_project/CSCI141/player_info.txt") as info_file:
        for line in info_file:
            leaderboard.append(line.strip())
    leaderboard_text = "~WELCOME TO THE GARDEN~\n\nLEADERBOARD:\n"+str(leaderboard[0])+"\n"+str(leaderboard[1])+"\n"+str(leaderboard[2])+"\n\nPRESS ENTER TO BEGIN"
    wn.textinput("garden says:", leaderboard_text)

    # ask user for their information
    user_information = {"name": "", "color": "", "steps": 0}
    user_information["name"] = wn.textinput("garden says:", "Hello there! Welcome to the garden. What is your name?(one word pls) ")
    user_information["color"] = wn.textinput("garden says:", "What color would you like your turtle to be? (red, orange, yellow, green, blue, or purple)? ")
    # keep asking until color is valid
    while user_color_invalid(user_information["color"]):
        user_information["color"] = wn.textinput("garden says:", "Looks like that color wasn't one of the options. What color would you like your turtle to be? (red, orange, yellow, green, blue, or purple)? ")
    wn.textinput("garden says:", "Looks like you're all set!. You can press enter to start and 'x' on your keyboard once you're done. Use the arrow keys to move around. Let's see how many steps you take!")
    user.color(user_information["color"])
    wn.update()

    # START PROGRAM #
    turtle_listen(user, wn, user_information)
    turtle.mainloop()

##### END FUCNTIONS #####

if __name__ == "__main__":
    main()