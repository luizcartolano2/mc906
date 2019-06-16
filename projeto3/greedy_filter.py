#!/usr/bin/env python
# coding: utf-8
# import das bibliotecas
import os
import pandas as pd
import random
import time
from greedy_filter import *
from math import inf
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


def get_average_variation(np_array, window_size, today_index):
    lambda_function = lambda x : abs(x)
    if (today_index > window_size+1):
        slice_array = np_array[today_index - window_size: today_index]
    else:
        slice_array = np_array[1:today_index]
    return lambda_function(slice_array).mean()


def fuzzy_pct_triangle(i_x_filter, i_risk, defuzzy_method):
    
    if i_x_filter < 0:
        i_x_filter = 0
    elif i_x_filter > 1:
        i_x_filter = 1
    
    # input porcentagem pro ultimo pico
    x_filter = np.arange(0, 1, 0.01)
    x_lo = fuzz.trimf(x_filter, [0, 0, 0.04])
    x_md = fuzz.trimf(x_filter, [0.03, 0.04, 0.05])
    x_hi = fuzz.trapmf(x_filter, [0.04, 0.06, 1, 1])

    # input risco
    x_risk = np.arange(0, 101, 1)
    risk_lo = fuzz.trimf(x_risk, [0, 0, 50])
    risk_md = fuzz.trimf(x_risk, [25, 50, 75])
    risk_hi = fuzz.trimf(x_risk, [50, 100, 100])

    
    # output porcentagem
    x_pct = np.arange(0, 101, 1)
    pct_lo = fuzz.trapmf(x_pct, [0, 0, 25, 50])
    pct_md = fuzz.trimf(x_pct, [25, 50, 75])
    pct_hi = fuzz.trapmf(x_pct, [50, 75, 100, 100])

    
    # ativa o fuzzy no valor do input    
    x_level_lo = fuzz.interp_membership(x_filter, x_lo, i_x_filter)
    x_level_md = fuzz.interp_membership(x_filter, x_md, i_x_filter)
    x_level_hi = fuzz.interp_membership(x_filter, x_hi, i_x_filter)
    risk_level_lo = fuzz.interp_membership(x_risk, risk_lo, i_risk)
    risk_level_md = fuzz.interp_membership(x_risk, risk_md, i_risk)
    risk_level_hi = fuzz.interp_membership(x_risk, risk_hi, i_risk)

    # regras
    # Rule 1 --> high x_filter AND low_risk
    rule1 = np.fmax(x_level_hi, risk_level_lo)
    activation_hi = np.fmin(rule1, pct_hi)
    # Rule 2 --> low x_filter OR high_risk
    rule2 = np.fmin(x_level_lo, risk_level_hi)
    activation_lo = np.fmin(rule2, pct_lo)
    # Rule 3 --> medium x_filter
    activation_md = np.fmin(x_level_md, pct_md)

    # Aggregate all three output membership functions together
    aggregated = np.fmax(activation_lo, np.fmax(activation_md, activation_hi))

    # Calculate defuzzified result
    pct = fuzz.defuzz(x_pct, aggregated, defuzzy_method)
    
    return pct


def fuzzy_risk_triangle(i_vol, i_beta, defuzzy_method):

    if i_vol < 0:
        i_vol = 0
    elif i_vol > 50:
        i_vol = 50
        
    if i_beta < 0.9:
        i_beta = 0.9
    elif i_beta > 1.2:
        i_beta = 1.2
    
    # input volatilidade
    x_vol = np.arange(0, 51, 1)
    vol_lo = fuzz.trimf(x_vol, [0, 0, 25])
    vol_md = fuzz.trimf(x_vol, [10, 25, 40])
    vol_hi = fuzz.trimf(x_vol, [30, 50, 50])

    
    # input beta
    x_beta = np.arange(0.9, 1.2, 0.01)
    beta_lo = fuzz.trimf(x_beta, [0.9, 0.9, 1.05])
    beta_md = fuzz.trimf(x_beta, [0.9, 1.05, 1.2])
    beta_hi = fuzz.trimf(x_beta, [1.1, 1.2, 1.2])

    # output risk
    x_risk = np.arange(0, 101, 1)
    risk_lo = fuzz.trimf(x_risk, [0, 0, 50])
    risk_md = fuzz.trimf(x_risk, [30, 70, 100])
    risk_hi = fuzz.trimf(x_risk, [90, 100, 100])

    
    # fuzzyfica os valores
    vol_level_lo = fuzz.interp_membership(x_vol, vol_lo, i_vol)
    vol_level_md = fuzz.interp_membership(x_vol, vol_md, i_vol)
    vol_level_hi = fuzz.interp_membership(x_vol, vol_hi, i_vol)
    beta_level_lo = fuzz.interp_membership(x_beta, beta_lo, i_beta)
    beta_level_md = fuzz.interp_membership(x_beta, beta_md, i_beta)
    beta_level_hi = fuzz.interp_membership(x_beta, beta_hi, i_beta)

    # regras
    # Rule 1 --> low vol OR beta
    rule1 = np.fmax(vol_level_lo, beta_level_lo)
    activation_lo = np.fmin(rule1, risk_lo)
    # Rule 2 --> high vol OR beta
    rule2 = np.fmax(vol_level_hi, beta_level_hi)
    activation_hi = np.fmin(rule2, risk_hi)
    # Rule 3 --> medium vol to medium risk
    activation_md = np.fmin(vol_level_md, risk_md)
    
    # Aggregate all three output membership functions together
    aggregated = np.fmax(activation_lo, np.fmax(activation_md, activation_hi))

    # Calculate defuzzified result
    risk = fuzz.defuzz(x_risk, aggregated, defuzzy_method)

    return risk


# Importação das bibliotecas a serem utilizadas
import pandas as pd
import os, os.path
import random

# Definição de constantes
STOCK_VALUE_INDEX = 1
STOCK_BETA_INDEX = 3
FILTER_RATE_INDEX = 0
FILTER_HOLD_INDEX = 1
FILTER_DELAY_INDEX = 2
FILTER_PREVIOUS_INDEX = 3
FILTER_THRESHOLD_INDEX = 4


def greedy_filter_rule(np_array, filter_rule, money):
    """
        Funcao gulosa para realizar a compra e venda das acoes com base na regra do filtro
        :param: np - array com as informacoes de data e valor das acoes
        :param: filter_rule - parametros da regra de filtro (x,h,d,p)
        :param: money - budget inicial que sera investido
        :return: budget ao final do tempo de investimento
    """
    i = 1
    stock_count = 0
    peaks = findPeakAndValley(np_array)
    stock_count = 0
    while (i < len(np_array)):
        signal_compra = getSignal(np_array, i, filter_rule[FILTER_PREVIOUS_INDEX], peaks, filter_rule[FILTER_RATE_INDEX])
        if (signal_compra > 0):
            stock_count = stock_count + int(signal_compra * money/np_array[i][STOCK_VALUE_INDEX])
            money = money - int(signal_compra * money/np_array[i][STOCK_VALUE_INDEX]) * np_array[i][STOCK_VALUE_INDEX]
            #print ("Comprou no dia: "+ str(i)+" totalizando: "+ str(stock_count)+ " e sobrou: "+ str(money))
            i = i + filter_rule[FILTER_HOLD_INDEX]
            while(i < len(np_array)):
                signal_venda = getSignal(np_array, i, filter_rule[FILTER_PREVIOUS_INDEX], peaks, filter_rule[FILTER_RATE_INDEX])
                if (signal_venda < 0):
                    money = money + int(round(stock_count * signal_venda * -1)) * np_array[i][STOCK_VALUE_INDEX]
                    stock_count = stock_count - int(round(stock_count * signal_venda * -1))
                    #print ("Vendeu no dia: "+ str(i)+ " e sobrou: " +str(stock_count)+ " e temos: "+ str(money))
                    break
                i = i + filter_rule[FILTER_DELAY_INDEX]
        i = i + 1
    
    return money + stock_count * np_array[len(np_array) - 1][STOCK_VALUE_INDEX]


def getSignal (np, today_index, previous_days, peaks, rate):
    """
        :param: np - array com as informacoes de data e valor das acoes
        :param: today_index - indice do dia a ser analisado
        :param: previous_days - quantidade de dias anteriores(p) que serao usados na analise
        :param: peaks - lista com as datas nas quais houveram picos(ou vales)
        :param: rate - taxa de crescimento
        :return: 1 - sinal de compra/ -1 - sinal de venda / 0 - sinal neutro
    """
    last_index_peak_valley = 0
    last_index = 0
    if (today_index > previous_days):
        for i in range(today_index - previous_days, today_index):
            if i in peaks:
                last_index_peak_valley = i
                if (np[i][STOCK_VALUE_INDEX]/np[i-1][STOCK_VALUE_INDEX] > 1):
                    last_index = 1 # Peak
                else:
                    last_index = -1 # Valley
    else:
        for i in range(0, today_index):
            if i in peaks:
                last_index_peak_valley = i
                if (np[i][STOCK_VALUE_INDEX]/np[i-1][STOCK_VALUE_INDEX] > 1):
                    last_index = 1 # Peak
                else:
                    last_index = -1 # Valley
    percentage_today_last_peak_valey = np[today_index][STOCK_VALUE_INDEX]/np[last_index_peak_valley][STOCK_VALUE_INDEX]
    if(i > 0):
        #print(get_average_variation(np[:,2], previous_days, today_index))
        #print(np[i][STOCK_BETA_INDEX])
        risk = fuzzy_risk_triangle(get_average_variation(np[:,2], previous_days, today_index), np[i][STOCK_BETA_INDEX], 'centroid')
        #print("Risk: ", risk, "Percentage", round(abs(percentage_today_last_peak_valey - 1),4))
        percentage = fuzzy_pct_triangle(abs(percentage_today_last_peak_valey - 1), risk, 'centroid')
        #print ("Percentage Last PEak: ", abs(percentage_today_last_peak_valey-1))
        if (percentage_today_last_peak_valey > 1 and abs(percentage_today_last_peak_valey - 1) >= rate):
            signal = 1 # Buy
        elif(percentage_today_last_peak_valey < 1 and abs(percentage_today_last_peak_valey - 1) >= rate):
            signal = -1 # Sell
        else:
            signal = 0 # Same price
        #print (percentage, percentage_today_last_peak_valey, rate)
        if(signal == 1 and last_index == -1):
            return 0.01 * percentage
        elif(signal == -1 and last_index == 1):
            return -0.01 * percentage
        else:
            return 0
    else:
        return 0


def get_average_variation(np_array, window_size, today_index):
    lambda_function = lambda x : abs(x)
    if (today_index > window_size+1):
        slice_array = np_array[today_index - window_size: today_index]
    else:
        slice_array = np_array[1:today_index]
    return lambda_function(slice_array).mean()



def findPeakAndValley(np):
    """
        Funcao que encontra todos os picos e vales em um conjunto de dados
        :param: np - dados a serem analisados
        :return: peakValleyArray - array com os picos e vales do conjunto fornecido
    """
    peakValleyArray = []
    for i in range (1, len(np) - 1):
        if (np[i][STOCK_VALUE_INDEX] / np[i - 1][STOCK_VALUE_INDEX] > 1 and np[i + 1][STOCK_VALUE_INDEX] / np[i][STOCK_VALUE_INDEX] < 1):
            peakValleyArray.append(i)
        if (np[i][STOCK_VALUE_INDEX] / np[i - 1][STOCK_VALUE_INDEX] < 1 and np[i + 1][STOCK_VALUE_INDEX] / np[i][STOCK_VALUE_INDEX] > 1):
            peakValleyArray.append(i)
    return peakValleyArray
