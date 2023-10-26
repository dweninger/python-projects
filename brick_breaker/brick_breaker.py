import tkinter as tk

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 10
BRICK_WIDTH = 40
BRICK_HEIGHT = 20
BALL_RADIUS = 10
PADDLE_SPEED = 10
BALL_SPEED = 2
NUM_BRICKS = 60

# Main window
root = tk.Tk()
root.title("Brick Breaker")

# canvas for drawing
canvas = tk.Canvas(
    root, width=CANVAS_WIDTH, 
    height=CANVAS_HEIGHT, bg="black")
canvas.pack()

# paddle
paddle = canvas.create_rectangle(
    CANVAS_WIDTH // 2 - PADDLE_WIDTH // 2, 
    CANVAS_HEIGHT - PADDLE_HEIGHT,
    CANVAS_WIDTH // 2 + PADDLE_WIDTH // 2, 
    CANVAS_HEIGHT, fill="white"
)

# Initialize ball's position and speed
ball_x = CANVAS_WIDTH // 2
ball_y = CANVAS_HEIGHT // 2
ball_dx = BALL_SPEED
ball_dy = -BALL_SPEED

# list of bricks
bricks = []
for i in range(NUM_BRICKS):
    x1 = i % 12 * BRICK_WIDTH
    y1 = i // 12 * BRICK_HEIGHT
    x2 = x1 + BRICK_WIDTH
    y2 = y1 + BRICK_HEIGHT
    brick = canvas.create_rectangle(
        x1, y1, x2, y2, fill="red")
    bricks.append(brick)

# move paddle left
def move_paddle_left(event):
    if canvas.coords(paddle)[0] > 0:
        canvas.move(paddle, -PADDLE_SPEED, 0)

# move paddle right
def move_paddle_right(event):
    if canvas.coords(paddle)[2] < CANVAS_WIDTH:
        canvas.move(paddle, PADDLE_SPEED, 0)

# Bind arrow keys to paddle movement using <Key> events
root.bind("<Left>", move_paddle_left)
root.bind("<Right>", move_paddle_right)

# check collision with bricks
def check_collision():
    global ball_dx, ball_dy
    for brick in bricks:
        if canvas.coords(
            ball)[2] >= canvas.coords(
                brick)[0] and canvas.coords(
                    ball)[0] <= canvas.coords(
                        brick)[2] and \
           canvas.coords(
               ball)[3] >= canvas.coords(
                   brick)[1] and canvas.coords(
                       ball)[1] <= canvas.coords(
                           brick)[3]:
            canvas.delete(brick)
            bricks.remove(brick)
            ball_dy *= -1
            break

    if canvas.coords(
        ball)[0] <= 0 or canvas.coords(
            ball)[2] >= CANVAS_WIDTH:
        ball_dx *= -1
    if canvas.coords(ball)[1] <= 0:
        ball_dy *= -1

    if canvas.coords(ball)[3] >= CANVAS_HEIGHT:
        canvas.create_text(
            CANVAS_WIDTH // 2, 
            CANVAS_HEIGHT // 2, 
            text="Game Over", 
            fill="white", 
            font=("Helvetica", 24)
        )
        root.after(1000, root.quit)

    if canvas.coords(
        ball)[3] >= canvas.coords(paddle)[1] and \
       canvas.coords(
           ball)[2] >= canvas.coords(paddle)[0] and \
       canvas.coords(
           ball)[0] <= canvas.coords(paddle)[2]:
        ball_dy *= -1

    if not bricks:
        canvas.create_text(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2,
            text="You Win!", 
            fill="white", 
            font=("Helvetica", 24)
        )
        root.after(1000, root.quit)

# update ball's position
def update_ball():
    global ball_x, ball_y
    canvas.move(ball, ball_dx, ball_dy)
    ball_x, ball_y = canvas.coords(
        ball)[0] + BALL_RADIUS, canvas.coords(
            ball)[1] + BALL_RADIUS
    check_collision()
    root.after(10, update_ball)

# ball
ball = canvas.create_oval(
    ball_x - BALL_RADIUS, 
    ball_y - BALL_RADIUS, 
    ball_x + BALL_RADIUS, 
    ball_y + BALL_RADIUS, 
    fill="white"
)

update_ball()
root.mainloop()
 