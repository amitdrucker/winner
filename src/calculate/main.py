from train import train
from test import test

logFile = {'msg': ''}
preDiff = 0
for i in range(2019, 2002, -1):
    train(i, preDiff)
    test(i, logFile, preDiff)
    open('log.txt', 'w').write(logFile['msg'])
