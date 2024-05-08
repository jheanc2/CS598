from sense_hat import SenseHat
sense = SenseHat()
sense.clear()
x, y = 3, 5
colours = [[255,0,0], [0,255,0], [0,0,255], [255,255,0], [255,0,255], [0,255,255]]
colour = 0

sense.set_pixel(x, y, colours[colour])
while True:
    for event in sense.stick.get_events():
        sense.clear()
        print(event.direction, event.action)
        if event.action == 'pressed' and event.direction == 'up':
            if y > 0:
                y -= 1
        if event.action == 'pressed' and event.direction == 'down':
            if y < 7:
                y += 1
        if event.action == 'pressed' and event.direction == 'right':
            if x < 7:
                x += 1
        if event.action == 'pressed' and event.direction == 'left':
            if x > 0:
                x -= 1
        sense.set_pixel(x, y, colours[colour])
        if event.action == 'pressed' and event.direction == 'middle':
            sense.clear()
            exit(1)

