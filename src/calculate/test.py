import math
import operator as op
from functools import reduce

import numpy as np
import tensorflow as tf

from prepareDF import prepareDf


def ncr(n, r):
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer / denom


def test(test_year, log_file, preDiff):
    earnings = 0
    max_lose = 0
    seed = 500
    lose_tolerance = 1
    log_file['msg'] += 'year %s\n-----------\n' % test_year
    new_model = tf.keras.models.load_model('epic_num_reader.model')
    x_train, x_test, y_train, y_test, x_test_rounds = prepareDf(test_year, preDiff)
    predictions = new_model.predict(x_test)
    success = 0
    round_success = 0
    fail = 0
    round_fail = 0
    round = 6
    for i in range(0, len(predictions)):
        if round != x_test_rounds[i]:
            matches = round_success + round_fail
            spent = ncr(matches, matches - lose_tolerance) * seed
            winnings = 0
            if round_success >= matches - lose_tolerance:
                winnings = ncr(round_success, matches - lose_tolerance)
                winnings = winnings * (math.pow(1.7, matches - lose_tolerance) * seed)
            round_earnings = winnings - spent
            earnings += round_earnings
            if earnings < max_lose:
                max_lose = earnings
            # if round_earnings < 0 and seed < 500:
            #     seed *= 2
            print('round %s' % round)
            print('--------------------')
            print('fail: ' + str(round_fail))
            print('success: ' + str(round_success))
            print('success ratio: %s\n' % str(float(round_success / (round_fail + round_success))))
            log_file['msg'] += 'round %s' % round
            log_file['msg'] += '\n--------------------\n'
            log_file['msg'] += 'fail: ' + str(round_fail)
            log_file['msg'] += ', success: ' + str(round_success)
            log_file['msg'] += ', ratio: %s\n' % str(float(round_success / (round_fail + round_success)))
            log_file['msg'] += ', 0 error round earnings: %s\n' % str(round_earnings)
            round_fail = 0
            round_success = 0
            round = x_test_rounds[i]

        pred = np.argmax(predictions[i])
        actual = y_test[i]
        if actual == pred:
            # print('success! actual dff: %s pred diff: %s' % (actual, pred))
            round_success += 1
            success += 1
        else:
            round_fail += 1
            fail += 1
    print('fail: ' + str(fail))
    log_file['msg'] += 'fail: ' + str(fail)
    print('success: ' + str(success))
    log_file['msg'] += ', success: ' + str(success)
    print('success ratio: ' + str(float(success / (success + fail))))
    log_file['msg'] += ', ratio: ' + str(float(success / (success + fail)))
    log_file['msg'] += ', 0 fail earnings: ' + str(earnings)
    log_file['msg'] += ', max-lost: ' + str(max_lose) + '\n'

# logFile = {'msg': ''}
# test(2005, logFile)
