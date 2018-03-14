from __future__ import division
import pickle
import matplotlib.pyplot as plt
import math

# open data
fp =  open("DSC_0008.txt", "r")
data = pickle.load(fp)
# print(data)

# pagackes data as ditionary {color: time, x, y}
organized_data = {'red': {'t': [], 'x': [], 'y': []}, 'green': {'t': [], 'x': [],
'y': []}, 'blue': {'t': [], 'x': [], 'y': []}, 'yellow': {'t': [], 'x': [], 'y': []}}

rbdist = 300 # distance between centers of r and b (stationary) dots in mm

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


def calculate_angles(data, color1, color2):
    t1_list = data[color1]['t']
    t2_list = data[color2]['t']
    x1_list = data[color1]['x']
    x2_list = data[color2]['x']
    y1_list = data[color1]['y']
    y2_list = data[color2]['y']

    # print(data[color2])
    # print(data[color1])
    t_theta_list = []
    theta_list = []


    # print(t1_list);
    # print(t2_list);
    for t1 in t1_list:
        # diff = t1_list[-1]
        # if index < len(t2_list):
        # found = False
        if t1 in t2_list:
            # # if (abs(t2 - t1)) < tolerence and not found:
            # if t2 == t1:
            #     # diff =  abs(t2-t1)
            #     break

        #if t1 in t2_list:
            index2 = t2_list.index(t1)
            index1 = t1_list.index(t1)
            x1 = x1_list[index1]
            x2 = x2_list[index2]
            y1 = y1_list[index1]
            y2 = y2_list[index2]
            theta = calculate_angle(x1, x2, y1, y2)

            t_theta_list.append(t1)
            theta_list. append(theta)
                # found = True;
    return t_theta_list, theta_list

def calculate_angle(x1, x2, y1, y2):
    y = y1 - y2
    x = x2 - x1
    theta = 0
    if y:
        theta = math.atan(x/y)
    print(theta)
    return theta

def calculate_cart(dist, data, color1,color2):
    ##  Calculates cart position
    ## Dist is the distance between two points that do not change distance
    ## data is the dataset used (a dictionary holding the data from the colors)
    ## Color1 is the color of the sticker attached to the cart_pos
    ## Color2 is the color of a second sticker attached either to the cart,
    ##      or to the pendulum bob of the first sticker's pendulum
    t1_list = data[color1]['t']
    t2_list = data[color2]['t']
    x1_list = data[color1]['x']
    x2_list = data[color2]['x']
    y1_list = data[color1]['y']
    y2_list = data[color2]['y']

    #Calculate initial cart position in pixels
    
    cart_zero_pix = [x1_list[0], y1_list[0]] 
    # initialize the difference measuring vector
    delta = []

    for t1 in t1_list: #for every element in t1_list
        t1_index = t1_list.index(t1) #This is the index
        try:
            t2_index = t2_list.index(t1) #check if t2 has the same time somewhere
        except:
            pass
        else:
            #Find distance between two dots
            # print(x2_list[t2_index],x1_list[t1_index])
            delx = x2_list[t2_index] - x1_list[t1_index]
            dely = y2_list[t2_index] - y1_list[t1_index]
            deltaxy = math.sqrt(delx**2 +dely**2 )
            delta.append(deltaxy)
    # plt.figure(3)
    # plt.plot(delta)
    #Find the average distance between the dots
    avepix = sum(delta)/float(len(delta))
    #Calculate how many pixels per unit distance between the dots
    pixperdist = avepix/dist
    # print(pixperdist)
    
    #calculate position compared to initial position of cart
    cartrelpix_x=[]
    cartrelpix_y =[]
    cartrelpix_x[:] = [x - cart_zero_pix[0] for x in x1_list]
    cartrelpix_y[:] = [y - cart_zero_pix[1] for y in y1_list]
    
    cart_pos = []
    for relpix in cartrelpix_x:
        k=cartrelpix_x.index(relpix)
        #Identify if left or right of origin
        cartsign = 1
        if cartrelpix_x[k]<0:
            cartsign = -1
        cart_pos.append(cartsign*math.sqrt(cartrelpix_x[k]**2 +cartrelpix_y[k]**2 )*pixperdist)
    return t1_list, cart_pos

# print(organized_data['blue']['t'])
theta_data1 = calculate_angles(organized_data, 'yellow', 'blue')
theta_data2 = calculate_angles(organized_data, 'green', 'red')

# print(theta_data[0])
fig1 = plt.figure(1)
plt.plot(theta_data1[0], theta_data1[1], label = 'Yellow Pendulum')
plt.plot(theta_data2[0], theta_data2[1], label = 'Green Pendulum')
plt.ylabel("Theta (rad)")
plt.xlabel('Time (s)')
plt.title('Double Pendulum')
plt.legend(['With Escapement','Without Escapement'])

#plt.plot(organized_data['yellow']['x'], organized_data['yellow']['y'], 'y')
#plt.plot(organized_data['blue']['x'], organized_data['blue']['y'], 'b')

plt.show()


cart_data = calculate_cart(rbdist, organized_data,'blue','red')
plt.figure(2)
plt.plot(cart_data[0],cart_data[1])
plt.ylabel("X-position of cart (mm)")
plt.xlabel('Time (s)')
plt.title('Cart on Double Pendulum')

plt.show()

# with open("singlependsWITHesc1angles.txt", "wb") as fp:
#     pickle.dump(theta_data1, fp)
# 
# with open("singlependWOesc1angles.txt", "wb") as fp:
#     pickle.dump(theta_data2, fp)