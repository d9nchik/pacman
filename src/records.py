import os


class Records:

    def __init__(self, records_file) -> None:
        super().__init__()
        self.records_file = records_file
        self.records = []
        self.read_scores()

    def read_scores(self) -> None:
        if not os.path.isfile(self.records_file):
            return

        with open(self.records_file) as f:
            for line in f:
                self.records.append(int(line))

    def write_scores(self) -> None:
        with open(self.records_file, 'w') as f:
            for record in self.records[:-1]:
                print(record, file=f)
            print(self.records[-1], file=f, end='')

    def get_scores(self):
        return tuple(self.records)

    def add_score(self, score: int) -> None:
        self.records.append(score)
        self.records = sorted(self.records, key=lambda x: -x)[:10]
        self.write_scores()
