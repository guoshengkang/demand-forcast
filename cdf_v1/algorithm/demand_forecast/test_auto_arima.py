#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-12 17:41:13
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import numpy as np
from pyramid.arima import auto_arima

wineind = np.array([
    # Jan    Feb    Mar    Apr    May    Jun    Jul    Aug    Sep    Oct    Nov    Dec
    15136, 16733, 20016, 17708, 18019, 19227, 22893, 23739, 21133, 22591, 26786, 29740, 
    15028, 17977, 20008, 21354, 19498, 22125, 25817, 28779, 20960, 22254, 27392, 29945, 
    16933, 17892, 20533, 23569, 22417, 22084, 26580, 27454, 24081, 23451, 28991, 31386, 
    16896, 20045, 23471, 21747, 25621, 23859, 25500, 30998, 24475, 23145, 29701, 34365, 
    17556, 22077, 25702, 22214, 26886, 23191, 27831, 35406, 23195, 25110, 30009, 36242, 
    18450, 21845, 26488, 22394, 28057, 25451, 24872, 33424, 24052, 28449, 33533, 37351, 
    19969, 21701, 26249, 24493, 24603, 26485, 30723, 34569, 26689, 26157, 32064, 38870, 
    21337, 19419, 23166, 28286, 24570, 24001, 33151, 24878, 26804, 28967, 33311, 40226, 
    20504, 23060, 23562, 27562, 23940, 24584, 34303, 25517, 23494, 29095, 32903, 34379, 
    16991, 21109, 23740, 25552, 21752, 20294, 29009, 25500, 24166, 26960, 31222, 38641, 
    14672, 17543, 25453, 32683, 22449, 22316, 27595, 25451, 25421, 25288, 32568, 35110, 
    16052, 22146, 21198, 19543, 22084, 23816, 29961, 26773, 26635, 26972, 30207, 38687, 
    16974, 21697, 24179, 23757, 25013, 24019, 30345, 24488, 25156, 25650, 30923, 37240, 
    17466, 19463, 24352, 26805, 25236, 24735, 29356, 31234, 22724, 28496, 32857, 37198, 
    13652, 22784, 23565, 26323, 23779, 27549, 29660, 23356]
).astype(np.float64)



stepwise_fit = auto_arima(wineind, start_p=0, start_q=0, max_p=15, max_q=15, m=7,
                          start_P=0, seasonal=False, d=1, D=1, trace=False,
                          error_action='ignore',  # don't want to know if an order does not work
                          suppress_warnings=True,  # don't want convergence warnings
                          stepwise=True)  # set to stepwise

# rs_fit = auto_arima(wineind, start_p=1, start_q=1, max_p=3, max_q=3, m=12,
#                     start_P=0, seasonal=True, n_jobs=-1, d=1, D=1, trace=True,
#                     error_action='ignore',  # don't want to know if an order does not work
#                     suppress_warnings=True,  # don't want convergence warnings
#                     stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
#                     n_fits=1)

print(stepwise_fit.__doc__)
print('-'*30)
p,d,q=stepwise_fit.order
print(p,d,q)
print('-'*30)
print(stepwise_fit.seasonal_order)


y_fit=stepwise_fit.predict_in_sample()
print(len(wineind),len(y_fit))
print(y_fit)

next_25 = stepwise_fit.predict(n_periods=25)
print(type(next_25))
