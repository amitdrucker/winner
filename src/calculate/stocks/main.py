from stocks.stocks_train import train

logFile = {'msg': ''}
preDiff = 0
for i in range(2018, 2019):
    train(i)
    # test(i, logFile, preDiff)
    # open('log.txt', 'w').write(logFile['msg'])
