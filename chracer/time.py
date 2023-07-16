import datetime

class Time:
    def __init__(self, us: int):
        self._us = us

    @property
    def us(self): return self._us

    def to_datetime(self):
        epoch_start = datetime.datetime(1601, 1, 1)
        delta = datetime.timedelta(microseconds=self._us)
        return epoch_start + delta 
    
    def validate(self, debug=False):
        try:
            assert self.us >= 0, 'INVALID Time (less than 0)'
        except Exception as e:
            if debug: print('base::Time -> 0x{0:X} {1}'.format(self.us, e))
            return False
        return True

class TimeTicks(Time):
    def to_datetime(self):
        return None

    def validate(self, debug=False):
        return True