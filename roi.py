import csv
import os

C = 1
input_dir = r''
input_folder = 'history.csv'
output_dir = r''
output_folder = 'outputC{}.csv'.format(str(C))



in_f = csv.reader(open(os.path.join(input_dir, input_folder), 'r'))
in_rows = list(in_f)
in_rows.pop(0)

out_f = csv.writer(open(os.path.join(output_dir, output_folder), 'w', newline=''))
out_f.writerow(['dailyVolumeToken0', 'dailyVolumeToken1', 'dailyVolumeUSD', 'date', 
                'reserve0', 'reserve1', 'reserveUSD', 'liquidityDepth', 'priceOfA', 'ratio', 
                'ratioChange', 'buy', 'sell', 'holdA', 'holdB', 'HoldAsB', 'HoldAsA', 
                'dailyROIA', 'dailyROIB', 'ROIAsB', 'TotROIA', 'TotROIB', 
                'TotROIAsB', '1'])

columns_numbers = []
for j in range(23):
    columns_numbers.append(str(j+1))
columns_numbers.append(str(2))
out_f.writerow(columns_numbers)
amount_of_eth = 1
amount_of_uni = 1
previous_ratio = 0
previous_total_roi_a = 1
previous_total_roi_b = 1

for i in range(0, len(in_rows)):
    current_row = in_rows[i]
    reserve0 = float(in_rows[i][4])
    reserve1 = float(in_rows[i][5])

    hold_a = (amount_of_eth * reserve0) / reserve1
    #hold_b = (amount_of_uni * reserve1) / reserve0
    hold_b = 1
    hold_a_b = hold_b + ((hold_a * reserve1) / reserve0)
    hold_a_a = hold_a + ((hold_b * reserve1) / reserve0)
    liquidity_depth = reserve0 * reserve1
    price_of_a = reserve1 / reserve0
    ratio = liquidity_depth / price_of_a
    
    
    if i==0:
        daily_roi_a = 1
        daily_roi_b = 1
        daily_roi_a_b = daily_roi_a * daily_roi_b
        daily_roi_a_a = daily_roi_a * daily_roi_a
        total_roi_a = previous_total_roi_a
        total_roi_b = previous_total_roi_b
        total_roi_a_b = total_roi_a * total_roi_b
        total_roi_a_a = total_roi_a * total_roi_a
        ratio_change = 0
        buy_signal = 0
        sell_signal = 0
        previous_ratio = ratio
    else:
        #daily_roi_a = 1 + ((float(in_rows[i][4]) - float(in_rows[i-1][4])) / float(in_rows[i][4]))
        #daily_roi_b = 1 + ((float(in_rows[i][5]) - float(in_rows[i-1][5])) / float(in_rows[i][5]))
        #daily_roi_a_b = daily_roi_a * daily_roi_b
        #daily_roi_a_a = daily_roi_a * daily_roi_a
        daily_roi_a = 1 + (float(in_rows[i][4]) / float(in_rows[i-1][4]))
        daily_roi_b = 1 + (float(in_rows[i][5]) / float(in_rows[i-1][5]))
        daily_roi_a_b = daily_roi_a * daily_roi_b
        #daily_roi_a_a = daily_roi_a * daily_roi_a
        total_roi_a = previous_total_roi_a * daily_roi_a
        total_roi_b = previous_total_roi_b * daily_roi_b
        total_roi_a_b = total_roi_a * total_roi_b
        #total_roi_a_a = total_roi_a * total_roi_a

        previous_total_roi_a = total_roi_a
        previous_total_roi_b = total_roi_b
        ratio_change = "{:.2%}".format(1 - (ratio / previous_ratio))
        if ratio > previous_ratio:
            buy_signal = ratio_change * C
            sell_signal = 0
        else:
            buy_signal = 0
            sell_signal = ratio_change * C
        previous_ratio = ratio
    
    
    
    
    current_row.append(liquidity_depth)
    current_row.append(price_of_a)
    current_row.append(ratio)
    current_row.append(ratio_change)
    current_row.append(buy_signal)
    current_row.append(sell_signal)
    current_row.append(hold_a)
    current_row.append(hold_b)
    current_row.append(hold_a_b)
    current_row.append(hold_a_a)
    current_row.append(daily_roi_a)
    current_row.append(daily_roi_b)
    current_row.append(daily_roi_a_b)
    #current_row.append(daily_roi_a_a)
    current_row.append(total_roi_a)
    current_row.append(total_roi_b)
    current_row.append(total_roi_a_b)
    #current_row.append(total_roi_a_a)
    current_row.append(str(i+3))
    out_f.writerow(current_row)
        
