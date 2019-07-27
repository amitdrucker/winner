from train import train
from test import test

logFile = {'msg': ''}
for i in range(2003, 2020):
    train(i)
    test(i, logFile)
    open('log.txt', 'w').write(logFile['msg'])
