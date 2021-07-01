import math

## definition of a 'constant' term

def A1(momentum1, momentum2, theta1, theta2):
    return (momentum1*momentum2*math.sin(theta1 - theta2))/(1 + (math.sin(theta1 - theta2))**2)

def A2(momentum1, momentum2, theta1, theta2):
    return (((momentum1)**2 - 2*momentum1*momentum2*math.cos(theta1 - theta2) + 2*(momentum2)**2)*math.sin(2*(theta1 - theta2)))/(2*(1 + (math.sin(theta1 - theta2))**2))

## definition of the time derivatives of quantities relevant to the lagrangian

def theta1_prime(momentum1, momentum2, theta1, theta2):
    return (momentum1 - momentum2*(math.cos(theta1 - theta2)))/(1 + (math.sin(theta1-theta2))**2)

def theta2_prime(momentum1, momentum2, theta1, theta2):
    return (2*momentum2 - momentum1*math.cos(theta1 - theta2))/(1 + (math.sin(theta1 - theta2))**2)

def momentum1_prime(momentum1, momentum2, theta1, theta2):
    return -2*9.81*math.sin(theta1) - A1(momentum1, momentum2, theta1, theta2) + A2(momentum1, momentum2, theta1, theta2)

def momentum2_prime(momentum1, momentum2, theta1, theta2):
    return -9.81*math.sin(theta2) + A1(momentum1, momentum2, theta1, theta2) - A2(momentum1, momentum2, theta1, theta2)


## this uses the Runge-Kutta method to get the next coordinate
def update_4vector(Z, timestep):
    ## input is Z
    
    Z_i = []
    for x in Z:
        Z_i.append(x)
    Z_1 = []
    Z_1.append(timestep*momentum1_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_1.append(timestep*momentum2_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_1.append(timestep*theta1_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_1.append(timestep*theta2_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))

    ## change input to Z + 1/2*Z_1
    Z_i = []
    index = 0
    for x in Z_1:
        Z_i.append(Z[index] + 0.5*x)
        index += 1

    Z_2 = []
    Z_2.append(timestep*momentum1_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_2.append(timestep*momentum2_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_2.append(timestep*theta1_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_2.append(timestep*theta2_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))

    ##change input to Z + 1/2*Z_2
    Z_i = []
    index = 0
    for x in Z_2:
        Z_i.append(Z[index] + 0.5*x)
        index += 1

    Z_3 = []    
    Z_3.append(timestep*momentum1_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_3.append(timestep*momentum2_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_3.append(timestep*theta1_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_3.append(timestep*theta2_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))

    ##change input to Z + Z_3
    Z_i = []
    index = 0
    for x in Z_3:
        Z_i.append(Z[index] + x)
        index += 1

    Z_4 = []
    Z_4.append(timestep*momentum1_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_4.append(timestep*momentum2_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_4.append(timestep*theta1_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))
    Z_4.append(timestep*theta2_prime(Z_i[0], Z_i[1], Z_i[2], Z_i[3]))

    index = 0
    blah = [0.0,0.0,0.0,0.0]
    while index < 4:
        blah[index] = Z[index] + 1.0/6*(Z_1[index] + 2*Z_2[index] + 2*Z_3[index] + Z_4[index])
        index += 1

    return blah

## add new data to the old data
## flip_regime is the maximum
## simulation time while waiting
## for the double pendulum to flip
## flip_regime should be less then
## 1000.01

def initialize(dimension):
    text = ''
    output = open('greatdata.txt', 'w')
    output.write(str(dimension) + '\n')
    for x in xrange(dimension):
        text += '1005  '
    for x in xrange(dimension):
        output.write(text + '\n')
    output.close()

def updateData(flip_regime):

    Z = []

    reference = open('greatdata.txt', 'r')

    ## read the file phase

    dimension = reference.readline()
    dimension = int(dimension)
    print type(dimension)

    data = []
    for x in xrange(dimension):
        row = reference.readline().split('  ')
        row.pop()
        index = 0
        ## convert each element into float
        for y in row:
            row[index] = float(row[index])
            index += 1
        data.append(row)

    print data[dimension - 1][dimension - 1]
    ## delete old greatdata, since it's been loaded into data
    reference.close()
    output = open('greatdata.txt', 'w')

    Z = [0.0, 0.0, 0.0, 0.0]
    theta_max = 3.141592653589793
    increment = 2.0/(dimension - 1)
    for x in xrange(dimension):
        theta1 = -1*theta_max + theta_max*(x)*increment
        if (x + 1) % 50 == 0:
            print 'x' + str(x + 1)
        for y in xrange(dimension - x):
            if data[x][y] <= 1005:
                theta2 = -1*theta_max + theta_max*(y)*increment
                ## start at the initial values: no momentum, mass 1 has angle theta1, mass 2 has angle theta2
                Z = [0.0, 0.0, theta1, theta2]
                t = 0
##                if 2*math.cos(theta1) + math.cos(theta2) >= 1:
##                    t = 1010
                while t <= flip_regime:
                    ## change t
                    Z_next = update_4vector(Z, 0.001)
                    t += 0.001
                    ## if the angle of mass 1 intersects with the line 3.1415 or -3.1415
                    if ((Z[2] <= theta_max) & (Z_next[2] > theta_max)) or ((Z[2] > -1*theta_max) & (Z_next[2] < -1*theta_max)):
                        break
                    ## if the angle of mass 2 intersects with the line 3.1415 or -3.1415
                    if (Z[3] <= theta_max) & (Z_next[3] > theta_max) or ((Z[3] > -1*theta_max) & (Z_next[3] < -1*theta_max)):
                        break
                    Z = []
                    for z in Z_next:
                        Z.append(z)
            ## all the text saving is trying to do is to create a 401x401 grid, whose data points are the time it took for the flip to occur. this would then be analyzed and graphed in matlab
            ## it also takes advantage of the symmetry of the graph. this feature could be removed, if a certain section needs to be zoomed in at.
                data[x][y] = t
                data[dimension - 1 - x][dimension - 1 - y] = t

    ## rewrite greatdata with the elements
    ## found inside the array 'data'

    output.write(str(dimension) + '\n')
    
    for x in xrange(dimension):
        blah = ''
        for y in xrange(dimension):
            blah += str(data[x][y]) + '  '
        output.write(blah + '\n')

    output.close()


while(True):
    startup = raw_input('Would you like to (initalize), (update) or to (view) data?')
    if startup == 'update':
        a = input('Give the flip regime ')
        a = float(a)
        updateData(a)
    if startup == 'initialize':
        a = input('Give the dimension of the image ')
        a = int(a)
        initialize(a)
    if startup == 'view':
        reference = open('greatdata.txt', 'r')
        output = open('greatdata2.txt', 'w')
        dimension = int(reference.readline())
        for x in xrange(dimension):
            output.write(reference.readline())
        reference.close()
        output.close()
