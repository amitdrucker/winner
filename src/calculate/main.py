from src.calculate.train import train

from src.calculate.test import test

logFile = {'msg': ''}
for i in range(2003, 2020):
    train(i)
    test(i, logFile)
    open('log.txt', 'w').write(logFile['msg'])
