import os
import pandas as pd
from datetime import datetime


class Utilites:
    '''
    handle answer from pressure sensor
    '''

    def __init__(self, mas, flag):
        self.mas = mas
        self.flag = flag

    @classmethod
    def get_highlow(cls, txt):
        """
        :param txt: register_number, number_of_regs
        :return: (high, low) value
        """
        tmps = "0000" + txt
        tmpl = tmps[-2:]
        tmph = tmps[-4:-2]
        return tmph, tmpl

    @classmethod
    def convert_response(cls, mas):
        '''
        answ: answer
        '''
        answ = []
        for el in mas:
            i = str(hex(el))[2:]
            l, h = cls.get_highlow(i)
            answ.append(chr(int(h, 16)))
            answ.append(chr(int(l, 16)))
        return ''.join(answ)

    @classmethod
    def color(cls, flag):
        return 'red' if not flag else 'green'

    @classmethod
    def text_manage_control(cls, flag):
        if flag == False:
            return 'Manual'
        return 'Auto'

    @classmethod
    def get_values_from_response(cls, values):
        pressure = [p for p in values.registers]
        text = cls.convert_response(pressure)
        return text

    @classmethod
    def get_pressure(cls, client, address):
        pressure = client.read_holding_registers(address, 7)
        pressure = [p for p in pressure.registers]
        text = Utilites.convert_response(pressure)
        return text

    @classmethod
    def data_save(cls, **kwargs):
        now = datetime.now()
        df = pd.DataFrame(columns=kwargs.keys())
        row = pd.Series(kwargs, name=now.strftime("%I:%M:%S"))
        df.loc[now.strftime("%I:%M:%S")] = row
        df.to_csv(f'{now.strftime("%Y-%m-%d")}.csv', mode='a', header=False)
