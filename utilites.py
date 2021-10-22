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
        if flag==False:
            return 'red'
        return 'green'
