""" ARAIP obstacle avoidance and seeing RGB Colors """
from controller import Robot
#create a robot instance 
robot=Robot()
print("Robot instance created!") #confirmation for robot created sucessfully 
#timestep(how often the robot updates)
TIME_STEP= int(robot.getBasicTimeStep())
#motor names 
left_motor= robot.getDevice('left wheel motor')
right_motor= robot.getDevice('right wheel motor')
#enable velocity control mode
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
#velocity control which runs the robot forever
left_motor.setVelocity(4.0)
right_motor.setVelocity(4.0)
#enable distance sensors
distance_sensors=[]
sensor_names= ['ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7']
for name in sensor_names:
    sensor= robot.getDevice(name)
    sensor.enable(TIME_STEP)
    distance_sensors.append(sensor)
#enable cameras
camera= robot.getDevice('camera')
camera.enable(TIME_STEP)
seen_color= set()
Obstacle_Thershold = 100
Turn_steps=25
Turn_counter=0
seen_colors = set() #keep track of colours already seen
#main loop:which runs until the simulation ends
while robot.step(TIME_STEP) !=-1:
    distances = [sensor.getValue() for sensor in distance_sensors]
    image=camera.getImage()
    width=camera.getWidth()
    height=camera.getHeight()
    x=width // 2
    y=height // 2
    #process sensor data and image
    r=camera.imageGetRed(image, width, x, y)
    g=camera.imageGetGreen(image, width, x, y)
    b=camera.imageGetBlue(image, width, x, y)
    
    red_count = 0
    green_count = 0
    blue_count= 0
    step= 5
    detected_color = None
    seen_color=[] # to show the color in order
    
    if r > 100 and g < 80 and b < 80:
        detected_color = 'red'
    elif g > 100 and r < 80 and b < 80:
        detected_color = 'green'
    elif b > 100 and r < 80 and g < 80:
        detected_color = 'blue'
    
    if detected_color and detected_color not in seen_colors:
        print(f"I see {detected_color}")
        seen_colors.add(detected_color)
        print("Summary: I have previously seen " + ", ".join(seen_colors))
        print(f"R={r}, G={g}, B={b}") #a debug print for seeing the camera RGB values

    front_obstacle = any(sensor_value > 80 for sensor_value in distances)
    
    if front_obstacle:
        print("Obstacle seen! Turning")
        is_turning = True
        Turn_counter = 0
        left_motor.setVelocity(4.0)
        right_motor.setVelocity(-4.0)
    else:
        left_motor.setVelocity(5.0)
        right_motor.setVelocity(5.0)
 