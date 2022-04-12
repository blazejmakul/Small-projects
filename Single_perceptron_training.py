import matplotlib.pyplot as plt
from random import uniform
import numpy as np
import pyautogui as gui

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
zeros = []
ones = []
x = np.linspace(0,10,100)
adding_points = True

def onclick(event):
    global adding_points
    global w1,w2,wb 
    if event.button == 1:
        if adding_points:
            if event.xdata != None and event.ydata != None:
                zeros.append((event.xdata, event.ydata))
                plt.plot(event.xdata, event.ydata, 'bo')
        else:
            res = predict(event.xdata, event.ydata, w1,w2,wb)
            string = "This point is: "
            string += str(res)
            if res == 0:
                plt.plot(event.xdata, event.ydata, 'bo')
            else:
                plt.plot(event.xdata, event.ydata, 'ro')
            gui.alert(string, "Prediction")
    elif event.button == 3:
        if adding_points:
            if event.xdata != None and event.ydata != None:
                ones.append((event.xdata, event.ydata))
                plt.plot(event.xdata, event.ydata, 'ro')
    elif event.button == 2:
        if adding_points:
            if not zeros or not ones:
                gui.alert("Not enogh points!")
            else:
                result = gui.confirm("Do you want to visualize?", buttons=["NO", "YES"])
                print(result)
                adding_points = False
                points = []
                for zero, one in zip(zeros, ones):
                    points.append((zero, 0))
                    points.append((one, 1))
                visualize = False
                if result == "YES":
                    visualize = True
                print("Training in progres...")
                w1,w2,wb = train_perceptron(points, visualize)
                print("Training finished!")
                plt.plot(x, - ((w1*x+wb) / w2), '-r')
    plt.pause(0.5)

def activation_function(num):
    if num > 0:
        return 1
    else:
        return 0

def predict(x,y,w1,w2,wb):
    res = (w1*x) + (w2*y) + wb
    return activation_function(res)

def train_perceptron(points, visualize):
    w1 = uniform(0, 1)
    w2 = uniform(0, 1)
    wb = uniform(0, 1)
    finished = False
    counter = 0
    while not finished:
        print(w1,w2)
        counter += 1
        if counter > 200:
            break
        error_found = False
        if visualize: lines = plt.plot(x, - ((w1*x+wb) / w2), '-r')
        for point in points:
            yn = (w1*point[0][0]) + (w2*point[0][1]) + wb
            yn = activation_function(yn)
            err = point[1] - yn
            if err == 0:
                if point == points[-1] and not error_found:
                    finished = True
                    if visualize: 
                        lines.pop(0).remove()
                        plt.pause(0.1)
            else:
                error_found = True
                w1 += err * point[0][0]
                w2 += err * point[0][1]
                wb += err
                if visualize: 
                    lines.pop(0).remove()
                    lines = plt.plot(x, - ((w1*x+wb) / w2), '-r')
                    plt.pause(0.1)
        if visualize and lines: 
            lines.pop(0).remove()
    return w1,w2,wb

cid = fig.canvas.mpl_connect('button_press_event', onclick)
gui.alert("Aby dodać punkt 0 kliknij LPM, aby dodać 1 kliknij PPM, aby zakończyć dodawanie naciśnij klawisz środkowy myszy", "Instrukcja")
plt.show()