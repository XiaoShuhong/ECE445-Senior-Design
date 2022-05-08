# In-built Libraries
import copy
import pprint
import os
import time
from collections import OrderedDict
import json

# Third-Party Libraries
import spacy

# inWhat Imports
from inWhat.datagenie import DataGenie
from inWhat.recommendgenie import RecommendGenie


class inWhat:
    """
    Class exposed to users to interact with the package. Exposes modules in the package via
    public methods

    """

    def __init__(self, data_root=None,):
        # inputs
        self.data_root = data_root
        self.pathDict = { "im2index" : os.path.join(data_root, "init_data/im2index.json"),
                     "category2IMGS" : os.path.join(data_root, "init_data/category2IMGS.json"),
                     "im2type" :  os.path.join(data_root, "init_data/im2type.json"),
                     "embeddings" : os.path.join(data_root, "init_data/embeddings.npy"),
                     "imgDatabaseFolder" : os.path.join(data_root, "figure_data/polyvore_outfits/images/")
                   }

        # Load constants: thresholds, mappings, scores

        # Initialize intermediate/output variables

        # Others

        # Initialize internal Class Instances

        self.data_genie_instance = DataGenie(self,self.pathDict)  
        self.recommend_genie_instance = RecommendGenie(self) 
        