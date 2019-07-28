import numpy as np
import tensorflow as tf

from prepareDF import prepareDf


def test(test_year, log_file, preDiff):
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
            print('round %s' % round)
            print('--------------------')
            print('fail: ' + str(round_fail))
            print('success: ' + str(round_success))
            print('success ratio: %s\n' % str(float(round_success / (round_fail + round_success))))
            log_file['msg'] += 'round %s' % round
            log_file['msg'] += '--------------------'
            log_file['msg'] += 'fail: ' + str(round_fail)
            log_file['msg'] += 'success: ' + str(round_success)
            log_file['msg'] += 'success ratio: %s\n' % str(float(round_success / (round_fail + round_success)))
            round_fail = 0
            round_success = 0
            round = x_test_rounds[i]

        pred = np.argmax(predictions[i])
        actual = y_test[i]
        if (actual <= 4 and actual <= pred <= 4) \
                or (actual > 4 and actual >= pred > 4):
            # print('success! actual dff: %s pred diff: %s' % (actual, pred))
            round_success += 1
            success += 1
        else:
            round_fail += 1
            fail += 1
    print('fail: ' + str(fail))
    log_file['msg'] += 'fail: ' + str(fail)
    print('success: ' + str(success))
    log_file['msg'] += 'success: ' + str(success)
    print('success ratio: ' + str(float(success / (success + fail))))
    log_file['msg'] += 'success ratio: ' + str(float(success / (success + fail))) + '\n'

# logFile = {'msg': ''}
# test(2005, logFile)
