class PandasData(object):
    def __init__(self, dataframe, columns):
        self.dataframe = dataframe
        self.columns = columns

    def __getitem__(self, index):
        jsons = self.dataframe.iloc[index].to_json()
        return json.loads(jsons)

    def get_unlabeled_set(self, labeled_indexes, n):
        unlabeled = set()
        for ix in self.dataframe.index:
            if ix not in labeled_indexes:
                unlabeled.add(ix.item())
                if len(unlabeled) >= n:
                    return unlabeled
        return unlabeled

