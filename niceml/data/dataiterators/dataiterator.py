class DataIterator(object):
    def __init__(self, data_generator):
        self.data_generator = data_generator
        self.cur_idx = 0
        self.item_count = len(self.data_generator)

    def __iter__(self):
        self.cur_idx = 0
        return self

    def __next__(self):
        if self.cur_idx < self.item_count:
            data = self.data_generator[self.cur_idx]
            data_info = self.data_generator.get_datainfo(self.cur_idx)
            self.cur_idx += 1
        else:
            raise StopIteration()
        return data_info, data
