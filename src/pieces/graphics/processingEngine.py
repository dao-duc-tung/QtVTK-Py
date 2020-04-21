from typing import Dict

from src.pieces.vtkModels import *


class ProcessingEngine:
    def __init__(self):
        self.__models: Dict[str, VtkModel] = {}

    def registerModel(self, model: VtkModel):
        self.__models[model.name] = model

    def getModel(self, name: str):
        if name in self.__models:
            return self.__models[name]

    def removeModel(self, name: str):
        if name in self.__models:
            del self.__models[name]
