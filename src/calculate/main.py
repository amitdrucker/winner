from train import train
from test import test

logFile = {'msg': ''}
preDiff = 3
for i in range(2003, 2020):
    train(i, preDiff)
    test(i, logFile, preDiff)
    open('log.txt', 'w').write(logFile['msg'])
