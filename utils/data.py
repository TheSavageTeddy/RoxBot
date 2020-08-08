import json
from collections import namedtuple
from utils.safe_math import NumericStringParser

def getJSON(file):
    with open(file, encoding='utf8') as data:
        return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

class FormatTime():
    def __init__(self):
        self.abbrv = {
            'seconds':'s',
            'second':'s',
            'secs':'s',
            'sec':'s',
            'minutes':'m',
            'minute':'m',
            'mins':'m',
            'min':'m',
            'hours':'h',
            'hour':'h',
            'hrs':'h',
            'hr':'h',
            'days':'d',
            'day':'d',
            'weeks':'w',
            'week':'w',
            'wks':'w',
            'wk':'w',
            'years':'y',
            'year':'y',
            'yrs':'y',
            'yr':'y'
        }
        self.abbrv_values = {
            's':1,
            'm':60,
            'h':3600,
            'd':86400,
            'w':604800,
            'y':31536000
        }
        self.abbrv_keys = [*self.abbrv]
    def clean(self, inp):
        tinp = inp
        for a in self.abbrv:
            tinp = tinp.replace(a, self.abbrv[a])
        return tinp
    def noSpaceFormat(self, split_input):
        try:
            float_res = float(split_input)
            return float_res
        except:
            res = []
            clean_input = self.clean(split_input)
            try:      
                clean_input = clean_input.replace(clean_input[-1], f"*{self.abbrv_values[clean_input[-1]]}")
                nsp = NumericStringParser()
                input_eval = nsp.eval(clean_input)
                res.append(input_eval)
            except:
                return None
            try:
                return sum(res)
            except:
                return None     
    def formatTime(self, time_input):
        ''' Function to turn time inputs into seconds '''
        split_input = time_input.split()
        if len(split_input) == 1:
            clean_input = self.clean(split_input[0])
            print(clean_input)
            try:
                float_input = float(clean_input)
                return float_input
            except:
                try:           
                    clean_input = clean_input.replace(clean_input[-1], f"*{self.abbrv_values[clean_input[-1]]}")
                    nsp = NumericStringParser()
                    input_eval = str(nsp.eval(clean_input))
                    return input_eval
                except:
                    return None
        elif not any(x in split_input for x in self.abbrv_keys):
            res = []
            for value in split_input:
                clean_input = self.clean(value)
                try:      
                    clean_input = clean_input.replace(clean_input[-1], f"*{self.abbrv_values[clean_input[-1]]}")
                    print(clean_input) 
                    nsp = NumericStringParser()
                    input_eval = nsp.eval(clean_input)
                    res.append(input_eval)
                except:
                    return None
            try:
                return sum(res)
            except:
                return None        
        else:
            res = []
            prev = []
            for item in split_input:
                if item in self.abbrv_keys:
                    prev.append(item)
                    res.append(self.noSpaceFormat(''.join(prev).replace(' ', '')))
                    prev = []
                else:
                    prev.append(str(self.noSpaceFormat(item)))
            return sum(res)

if __name__ == "__main__":
    while True:
        inp = input("Enter time string: ") 
        time_handler = FormatTime()
        print(time_handler.formatTime(inp))