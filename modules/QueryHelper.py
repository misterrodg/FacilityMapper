def translateWildcard(wildcardString: str) -> str:
    return wildcardString.replace("#", "%")


def segmentQuery(queryResult: list, dictId: str) -> list[dict]:
    lastId = ""
    segment = []
    result = []
    for record in queryResult:
        recordDict = dict(record)
        currentId = recordDict.get(dictId)
        if currentId != lastId and lastId != "":
            result.append(segment)
            segment = []
        segment.append(recordDict)
        lastId = currentId
    if len(segment) > 0:
        result.append(segment)
    return result
