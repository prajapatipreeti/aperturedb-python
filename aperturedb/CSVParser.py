import pandas as pd

from aperturedb import ParallelLoader

ENTITY_CLASS      = "EntityClass"
CONTRAINTS_PREFIX = "constraint_"
PROPERTIES  = "properties"
CONSTRAINTS = "constraints"


class CSVParser():
    """**ApertureDB General CSV Parser for Loaders.**
    ...
    """

    def __init__(self, filename):

        self.df = pd.read_csv(filename)

        self.validate()

        if len(self.df) == 0:
            print("Error: Dataframe empty. Is the CSV file ok?")

        self.df = self.df.astype('object')

        self.header = list(self.df.columns.values)

    def __len__(self):

        return len(self.df.index)

    def parse_properties(self, df, idx):

        properties = {}
        if len(self.props_keys) > 0:
            for key in self.props_keys:
                # Handle Date data type
                if key.startswith("date:"):
                    prop = key[len("date:"):]  # remove prefix
                    properties[prop] = {"_date": self.df.loc[idx, key]}
                else:
                    value = self.df.loc[idx, key]
                    if value == value:  # skips nan values
                        properties[key] = value

        return properties

    def parse_constraints(self, df, idx):

        constraints = {}
        if len(self.constraints_keys) > 0:
            for key in self.constraints_keys:
                if key.startswith("constraint_date:"):
                    prop = key[len("constraint_date:"):]  # remove prefix
                    constraints[prop] = [
                        "==", {"_date": self.df.loc[idx, key]}]
                else:
                    prop = key[len(CONTRAINTS_PREFIX):]  # remove "prefix
                    constraints[prop] = ["==", self.df.loc[idx, key]]

        return constraints

    def __getitem__(self, idx):

        Exception("__getitem__ not implemented!")

    def validate(self):

        Exception("Validation not implemented!")
