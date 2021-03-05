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
    file_lines = []
    with open(file_name, "r") as info_file:
        for line in info_file:
            file_lines.append(line.split())
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
    with open(file_name, "r") as info_file:
        file_line_count = 0
        for line in info_file:
            file_line_count+=1
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
    colors = ("red", "orange", "yellow", "green", "blue", "purple")
    if user_color in colors:
        result = False
    else:
        result = True
    return result

def create_wn_variables(t, wn):
    print(t.xcor(), t.ycor())
    wn_llx = -wn.window_width()/2 + t.xcor()
    wn_lly = -wn.window_height()/2 + t.ycor()
    wn_urx = wn.window_width()/2 + t.xcor()
    wn_ury = wn.window_height()/2 + t.ycor()
    print("create_wn_variables says: llx:", wn_llx, "lly:", wn_lly, "urx:", wn_urx, "ury:", wn_ury )
    return (wn_llx, wn_lly, wn_urx, wn_ury)

def get_new_tcoords(wn_llx, wn_lly, wn_urx, wn_ury):
    new_x = (wn_llx + wn_urx)/2
    new_y = (wn_lly + wn_ury)/2
    return (new_x, new_y)

def create_up(t, wn, user_information):
    t.setheading(90)    
    wn_llx, wn_lly, wn_urx, wn_ury = create_wn_variables(t, wn)
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
    t.setheading(270)
    wn_llx, wn_lly, wn_urx, wn_ury = create_wn_variables(t, wn)
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
    t.setheading(180)
    wn_llx, wn_lly, wn_urx, wn_ury = create_wn_variables(t, wn)
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
    t.setheading(0)
    wn_llx, wn_lly, wn_urx, wn_ury = create_wn_variables(t, wn)
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
    with open("final_project/CSCI141/player_info.txt", "a") as info_file:
        info_file.write("\n")
        for key in user_information:
            info_file.write(str(user_information[key]))
            info_file.write(" ")
    print("done is running")
    prompt = "You took "+ str(user_information["steps"]) + " steps! Press enter to end program."
    wn.textinput("garden says:", prompt)
    sort_leaderboard("final_project/CSCI141/player_info.txt")
    exit()


def turtle_listen(t, wn, user_information):
    turtle.listen()
    
    up = partial(create_up, t, wn, user_information)
    down = partial(create_down, t, wn, user_information)
    left = partial(create_left, t, wn, user_information)
    right = partial(create_right, t, wn, user_information)
    done = partial(create_done, t, wn, user_information)

    wn.onkey(up, "Up")
    wn.onkey(down, "Down")
    wn.onkey(left, "Left")
    wn.onkey(right, "Right")
    wn.onkey(done, "x")

def create_garden(wn):
    """ Draws garden with grey fence and dark green grid wit dimensions of about 2000px * 2000px.
        Arguements: wn- a turtle screen variable
    """

    #create the turtle that will draw, set no animation and make background green
    garden_turtle = turtle.Turtle()
    wn.tracer(0, 0)
    wn.bgcolor("SaddleBrown")

    #draw grid
    garden_turtle.width(20)
    garden_turtle.color("forestgreen")
    for i in range(100):
        #lets make the garden 2000 by 2000
        garden_turtle.setheading(0)
        garden_turtle.penup()
        garden_turtle.goto(-992, 990-(i*20))
        garden_turtle.pendown()
        garden_turtle.forward(1982)

    # for i in range(100):
    #     garden_turtle.setheading(270)
    #     garden_turtle.penup()
    #     garden_turtle.goto(1000-(i*20), 1000)
    #     garden_turtle.pendown()
    #     garden_turtle.forward(2000)

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
    # setup the window and create user turtle
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
    while user_color_invalid(user_information["color"]):
        user_information["color"] = wn.textinput("garden says:", "Looks like that color wasn't one of the options. What color would you like your turtle to be? (red, orange, yellow, green, blue, or purple)? ")
    wn.textinput("garden says:", "Looks like you're all set!. You can press enter to start and 'x' on your keyboard once you're done. Let's see how many steps you take!")
    user.color(user_information["color"])
    wn.update()

    # START PROGRAM #
    turtle_listen(user, wn, user_information)
    turtle.mainloop()

##### END FUCNTIONS #####

if __name__ == "__main__":
    main()