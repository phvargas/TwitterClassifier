def dictionaryByValue(obj):
    return [(key, obj[key]) for key in sorted(obj, key=obj.get, reverse=True)]
