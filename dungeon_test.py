"""Creates procedurally a dungeon"""
# 1. Divides the map into squares (from 2x2 to 4x8)
# 2. Creates rooms in some of those squares (ex: 50%)
# 2.5 Checks to see if there's enough rooms
# 3. Joins the rooms with paths
# 4. Makes every room accesible

# To visualize the squares
import matplotlib.pyplot as plt

import random

dimensions = (360, 180) #cells per map

x_division = random.randint(2,8)
y_division = random.randint(2,4)

x_room_max = dimensions[0]/x_division
y_room_max = dimensions[1]/y_division

# Collects the rooms upper left and down right cell coordinates
# (0,0) is the upmost leftmost one, with the numbers going up
# if the cells move down and right
rooms=[]
enough_rooms = False
emergency_flag = 0

#while enough_rooms == False or emergency_flag<5:
for i in range(0, dimensions[0], int(x_room_max)):
    for j in range(0, dimensions[1], int(y_room_max)):
        if random.random() <= 0.5:

            # Room has the two coordinates of the rectangle
            room=[]
            room.append((i,j))
            room_ratio_flag = 0
            while room_ratio_flag>=2 or room_ratio_flag<=0.5:
                x_room_dim = random.randint(5,int(x_room_max))
                y_room_dim = random.randint(5,int(y_room_max))
                room_ratio_flag = x_room_dim/y_room_dim
            #print(room_ratio_flag)
            room.append( (i + x_room_dim , j + y_room_dim) )

            rooms.append(room)

#Checks to see if there's enough or too many rooms
if rooms and len(rooms) <= 10:
    enough_rooms = True

emergency_flag += 1

x_rooms_coords = []
y_rooms_coords = []
for i in rooms:
    for j in i:
        x_rooms_coords.append(j[0])
        y_rooms_coords.append(j[1])



print("number of x divisions" + str(x_division))
print("number of y divisions" + str(y_division))
print("number of rooms" + str(rooms))

plt.scatter(x_rooms_coords, y_rooms_coords, s=100)

# Set chart title and label axes.
plt.title("Rooms coords", fontsize=24)
plt.xlabel("X coords", fontsize=14)
plt.ylabel("Y coords", fontsize=14)
# Set size of tick labels.
plt.tick_params(axis='both', which='major', labelsize=14)

plt.show()



"""The last step is to join them with paths"""
# 1. We select the first room
# 2. We join it with the next one in the row
# 3. We repeat for all the rooms
# 4. We repeat for all the columns
# 5. If this doesn't work, we generate another floor OR
# 6. We generate a 1 by 1 room somewhere to solve the problem