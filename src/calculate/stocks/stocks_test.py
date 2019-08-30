from stocks.stocks_prepareDF import prepare_df_for_test


def simulated_calc_gain(batch):
    currently_investing = False
    sell_now = False
    gain = 0
    for row in batch:
        if sell_now:
            currently_investing = False
            curr_gain = row['Value'] - buy_price
            gain += curr_gain
            print('selling with gain %d' % curr_gain)
        elif currently_investing and not row['Will_Raise']:
            sell_now = True
        elif row['Will_Raise']:
            currently_investing = True
            buy_price = row['Value']
            print('buy at %d' % buy_price)
    if currently_investing:
        curr_gain = row['Value'] - buy_price
        gain += curr_gain
        print('selling with gain %d (last entry in batch)' % curr_gain)
    return gain


# def model_calc_gain(batch):
#     currently_investing = False
#     for row in batch:
#         if row['Will_Raise']:
#             currently_investing = True
#             but_price = ba


def test():
    x_test = prepare_df_for_test()
    gain = 0
    while len(x_test) > 0:
        batch_id = x_test['Batch_ID'].iloc[0]
        batch = x_test[x_test['Batch_ID'] == batch_id]
        batch_gain = simulated_calc_gain(batch)
        gain += batch_gain
        print('batch gain: %d total gain: %d' % (batch_gain, gain))


test()
