import time
from IPython import display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import random

def init_board(pos_list, my_board):
    for j in range(len(pos_list)):
        my_board[pos_list[j][0], pos_list[j][1]] = 1
    # return my_board

# Input variables for the board
boardsize = 20        # board will be X by X where X = boardsize
pad = 2               # padded border, do not change this!
initial_cells = 1500  # this number of initial cells will be placed
                      # in randomly generated positions

# Get a list of random coordinates so that we can initialize
# board with randomly placed organisms
pos_list = []
for i in range(200):
    pos_list.append([random.randint(1, boardsize),
                     random.randint(1, boardsize)])

# Initialize the board
my_board = np.zeros((boardsize+pad, boardsize+pad))
init_board(pos_list, my_board)
pass
# Required line for plotting the animation
# Initialize the plot of the board that will be used for animation
fig = plt.gcf()
im = plt.imshow(my_board)

def animate(frame):
    im.set_data(update_board(my_board))
    return im,

def update_board(my_board):
    for i in range(50):
        count = 0
        x, y = random.randint(1, boardsize-2), random.randint(1, boardsize-2)
        if my_board[x,y]==1:
            for j in range(3):
                for k in range(3):
                    if my_board[x + j, y+k] == 1:
                        count +=1
            if count < 2:
                for j in range(3):
                    for k in range(3):
                        my_board[x + j, y + k] = 0
            elif count >7 :
                for j in range(3):
                    for k in range(3):
                        my_board[x + j, y + k] = 0
        else:
            for j in range(3):
                for k in range(3):
                    if my_board[x + j, y+k] == 1:
                        count +=1
            if count == 3:
                for j in range(3):
                    for k in range(3):
                        my_board[x + j, y + k] = 1

        new_board = my_board
        return  new_board

# This line creates the animation
anim = animation.FuncAnimation(fig, animate, frames=1000,
                               interval=50)
plt.show()



# def init():
#     ax.set_xlim(0, 2*np.pi)
#     ax.set_ylim(-1, 1)
#     return ln,
#
# def update(frame):
#     xdata.append(frame)
#     ydata.append(np.sin(frame))
#     ln.set_data(xdata, ydata)
#     return ln,
#
# ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
#                     init_func=init, blit=True)
# plt.show()