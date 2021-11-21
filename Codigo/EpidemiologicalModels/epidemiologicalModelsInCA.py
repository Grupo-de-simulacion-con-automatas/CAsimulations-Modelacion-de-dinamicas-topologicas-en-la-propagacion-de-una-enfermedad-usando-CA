import EpidemiologicalModels.AgeManagement as AgeManagement

def createAgeMatrix(ranges, system):
    return AgeManagement.CreateAgesMatrix(ranges, system).create()