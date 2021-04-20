import math
import time
from threading import Thread

import numpy  as np
import pandas as pd

from aperturedb import Status
from aperturedb import ParallelLoader

ENTITY_CLASS      = "EntityClass"
CONTRAINTS_PREFIX = "constraint_"
PROPERTIES  = "properties"
CONSTRAINTS = "constraints"

class EntityGeneratorCSV():

    '''
        ApertureDB Entity Data loader.
        Expects a csv file with the following columns:

            EntityClass,PROP_NAME_1, ... PROP_NAME_N,constraint_PROP1

        Example csv file:
        EntityClass,name,lastname,age,id,constaint_id
        Person,John,Salchi,69,321423532,321423532
        Person,Johna,Salchi,63,42342522,42342522
        ...
    '''

    def __init__(self, filename):

        self.df = pd.read_csv(filename)

        self.validate()

        self.df = self.df.astype('object')

        self.props_keys       = [x for x in self.header[1:] if not x.startswith(CONTRAINTS_PREFIX) ]
        self.constraints_keys = [x for x in self.header[1:] if x.startswith(CONTRAINTS_PREFIX) ]

    def __len__(self):

        return len(self.df.index)

    def __getitem__(self, idx):

        data = {
            "class": self.df.loc[idx, ENTITY_CLASS]
        }

        if len(self.props_keys) > 0:
            properties = {}
            for key in self.props_keys:
                # Handle Date data type
                if key.startswith("date:"):
                    prop = key[len("date:"):] # remove prefix
                    properties[prop] = {"_date": self.df.loc[idx, key]}
                else:
                    properties[key] = self.df.loc[idx, key]
            data[PROPERTIES] = properties

        if len(self.constraints_keys) > 0:
            constraints = {}
            for key in self.constraints_keys:
                if key.startswith("constraint_date:"):
                    prop = key[len("constraint_date:"):] # remove prefix
                    constraints[prop] = ["==", {"_date": self.df.loc[idx, key]} ]
                else:
                    prop = key[len("constraint_"):] # remove "prefix
                    constraints[prop] = ["==", self.df.loc[idx, key]]
            data[CONSTRAINTS] = constraints

        return data

    def validate(self):

        self.header = list(self.df.columns.values)

        if self.header[0] != ENTITY_CLASS:
            raise Exception("Error with CSV file field: " + HEADER_X_POS)

class EntityLoader(ParallelLoader.ParallelLoader):

    '''
        ApertureDB Entity Loader.

        This class is to be used in combination with a "generator".
        The generator must be an iterable object that generated "entity_data"
        elements:
            entity_data = {
                "class":       entity_class,
                "properties":  properties,
                "constraints": constraints,
            }
    '''

    def __init__(self, db, dry_run=False):

        super().__init__(db, dry_run=dry_run)

    def generate_batch(self, entity_data):

        q = []

        for data in entity_data:

            ae = {
                "AddEntity": {
                    "class": data["class"]
                }
            }

            if PROPERTIES in data:
                ae["AddEntity"][PROPERTIES] = data[PROPERTIES]

            if CONSTRAINTS in data:
                ae["AddEntity"][CONSTRAINTS] = data[CONSTRAINTS]

            q.append(ae)

        if self.dry_run:
            print(q)

        return q, []

    def print_stats(self):

        print("====== ApertureDB Entity Loader Stats ======")

        times = np.array(self.times_arr)
        print("Avg Query time(s):", np.mean(times))
        print("Query time std:", np.std (times))
        print("Avg Query Throughput (entities/s)):",
            1 / np.mean(times) * self.batchsize * self.numthreads)

        print("Total time(s):", self.ingestion_time)
        print("============================================")
