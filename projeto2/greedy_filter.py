#!/usr/bin/env python
# coding: utf-8

# Importação das bibliotecas a serem utilizadas
import pandas as pd
import os, os.path
import random

# Definição de constantes
STOCK_VALUE_INDEX = 1
FILTER_RATE_INDEX = 0
FILTER_HOLD_INDEX = 1
FILTER_DELAY_INDEX = 2
FILTER_PREVIOUS_INDEX = 3


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
    while (i < len(np_array)):
        if (getSignal(np_array, i, filter_rule[FILTER_PREVIOUS_INDEX], peaks, filter_rule[FILTER_RATE_INDEX]) == 1):
            stock_count = int(money/np_array[i][STOCK_VALUE_INDEX])
            money = money - stock_count * np_array[i][STOCK_VALUE_INDEX]
            i = i + filter_rule[FILTER_HOLD_INDEX]
            while(i < len(np_array)):
                if(getSignal(np_array, i, filter_rule[FILTER_PREVIOUS_INDEX], peaks, filter_rule[FILTER_RATE_INDEX]) == -1):
                    money = money + stock_count * np_array[i][STOCK_VALUE_INDEX]
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
    if (percentage_today_last_peak_valey > 1 and abs(percentage_today_last_peak_valey - 1) >= rate):
        signal = 1 # Buy
    elif(percentage_today_last_peak_valey < 1 and abs(percentage_today_last_peak_valey - 1) >= rate):
        signal = -1 # Sell
    else:
        signal = 0 # Same price
        
    if(signal == 1 and last_index == -1):
        return 1
    elif(signal == -1 and last_index == 1):
        return -1
    return 0


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

