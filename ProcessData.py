import pickle
import matplotlib.pyplot as plt
import math

# open data
fp =  open("one_pendulum_test2.txt", "r")
data = pickle.load(fp)

# pagackes data as ditionary {color: time, x, y}
organized_data = {'red': {'t': [], 'x': [], 'y': []}, 'green': {'t': [], 'x': [],
'y': []}, 'blue': {'t': [], 'x': [], 'y': []}, 'yellow': {'t': [], 'x': [], 'y': []}}

# Organize Data
for i in data:
    color = i[0]
    center = i[1]
    x = center[0]
    y = center[1]
    t = i[2]

    t_list = organized_data.get(color)['t']
    x_list = organized_data.get(color)['x']
    y_list = organized_data.get(color)['y']

    t_list.append(t)
    x_list.append(x)
    y_list.append(y)

    organized_data[color] = {'t': t_list, 'x': x_list, 'y': y_list}


def calculate_angles(data, color1, color2, tolerence):
    t1_list = data[color1]['t']
    t2_list = data[color2]['t']
    x1_list = data[color1]['x']
    x2_list = data[color2]['x']
    y1_list = data[color1]['y']
    y2_list = data[color2]['y']

    t_theta_list = []
    theta_list = []

    print(t1_list)
    print(t2_list)
    for t1 in t1_list:
        index = t1_list.index(t1)
        if index < len(t2_list):
            if (abs(t2_list[index] - t1)) < tolerence:
                x1 = x1_list[index]
                x2 = x2_list[index]
                y1 = y1_list[index]
                y2 = y2_list[index]
                theta = calculate_angle(x1, x2, y1, y2)

                t_theta_list.append(t1)
                theta_list.append(theta)
    return t_theta_list, theta_list

def calculate_angle(x1, x2, y1, y2):
    y = y1 - y2
    x = x2 - x1
    theta = 0
    if y:
        theta = math.atan(x/y)
    return theta

print(organized_data['yellow']['t'])
theta_data = calculate_angles(organized_data, 'yellow', 'blue', .001)
print(theta_data)
plt.plot(theta_data[0], theta_data[1])
#plt.plot(organized_data['yellow']['x'], organized_data['yellow']['y'], 'y')
#plt.plot(organized_data['blue']['x'], organized_data['blue']['y'], 'b')

plt.show()
