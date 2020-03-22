from robot_class import Robot

import math
import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns

# --------
# this helper function displays the world that a robot is in
# it assumes the world is a square grid of some given size
# and that landmarks is a list of landmark positions(an optional argument)
def display_world(world_size, position, landmarks=None):
    
    # using seaborn, set background grid to gray
    sns.set_style("dark")

    # Plot grid of values
    world_grid = np.zeros((world_size + 1, world_size + 1))

    # Set minor axes in between the labels (gca = "get current axes" of the given plt instance) similar to gcf = "get current figure"
    ax = plt.gca()
    cols = world_size + 1
    rows = world_size + 1

    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')

    ax.set_xticks([x for x in range(1, cols)], minor=True )
    ax.set_yticks([y for y in range(1, rows)], minor=True)
    
    # Plot grid on minor axes in gray (width = 1)
    plt.grid(which='minor', ls='-', lw=1, color='white')
    
    # Plot grid on major axes in larger width
    plt.grid(which='major', ls='-', lw=2, color='white')
    
    # Create an 'o' character that represents the robot
    # ha = horizontal alignment, va = vertical alignment
    ax.text(position[0], position[1], 'o', ha='center', va='center', color='r', fontsize=30)
    
    # Draw landmarks if they exists
    if landmarks:
        # loop through all path indices and draw a dot (unless it's at the car's location)
        for pos in landmarks:
            if pos != position:
                ax.text(pos[0], pos[1], 'x', ha='center', va='center', color='purple', fontsize=20)
    
    # Display final result
    plt.show()

    
# --------
# this routine makes the robot data
# the data is a list of measurements and movements: [measurements, [dx, dy]]
# collected over a specified number of time steps, N
#
def make_data(N, num_landmarks, world_size, measurement_range, motion_noise, 
              measurement_noise, distance, is_debug=False):
    # check if data has been made
    complete = False

    while not complete:
        data = []

        # make robot and landmarks
        robot = Robot(world_size, measurement_range, motion_noise, measurement_noise)
        if is_debug:
            robot.make_debug_landmarks(num_landmarks) 
        else :
            robot.make_landmarks(num_landmarks)
        seen = [False for row in range(num_landmarks)]
    
        # guess an initial motion
        orientation = random.random() * 2.0 * np.pi
        dx = np.cos(orientation) * distance
        dy = np.sin(orientation) * distance
    
        for k in range(0, N - 1):
            #print('Run: ', k)
            # collect sensor measurements in a list, Z
            Z = robot.sense()

            # check off all landmarks that were observed 
            for i in range(0, len(Z)):
                seen[Z[i][0]] = True
    
            # move
            while not robot.move(dx, dy):
                # if we'd be leaving the robot world, pick instead a new direction
                orientation = random.random() * 2.0 * np.pi
                dx = np.cos(orientation) * distance
                dy = np.sin(orientation) * distance

            # collect/memorize all sensor and motion data
            data.append([Z, [dx, dy]])

        # we are done when all landmarks were observed; otherwise re-run
        complete = (sum(seen) == num_landmarks)

    print(' ')
    print('Landmarks: ', robot.landmarks)
    print(robot)

    return data