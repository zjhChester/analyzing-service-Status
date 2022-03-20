singeTonAnnotations = [
    'Service', 'Controller', 'Repository', 'Configuration', 'Component'
]
getterAnnotations = [
    'Data', 'Getter'
]
collectionTypes = [
    'Map', 'List', 'Set', 'Vector', 'HashTable'
]
usedMethods = [
    "remove", "add", "push", "put", "pop", "clear", "removeAll", "insert"
]

collectionsVariables = []
collectionsVariablesWithOnlyClassName = []
absoluteHasStatusVariables = []


def getFieldsAccessible(javaClass):
    names = []
    for item in javaClass.types[0].annotations:
        if getterAnnotations.__contains__(item.name):
            return True
    return False


def getCollectionVariables(javaClass):
    variablesNames = []
    for item in javaClass.types[0].fields:
        if collectionTypes.__contains__(item.type.name) and (getFieldsAccessible(javaClass) or str(item.modifiers).__contains__("public")):
            itemObj = {
                'nameOrigin': item.declarators[0].name,
                'name': 'get' + item.declarators[0].name.title(),
                'itemType': item.type.name,
                'package': javaClass.package.name,
                'className': javaClass.types[0].name
            }
            variablesNames.append(itemObj)
    return variablesNames


def getSingleTonClass(javaClass):
    names = []
    for item in javaClass.types[0].annotations:
        if singeTonAnnotations.__contains__(item.name):
            return True
    return False


def isContainsImports(javaClass, variable):
    for item in javaClass.imports:
        if item.path == variable:
            return True

    return False


def checkIsUsed(sources):
    for javaClass in sources:
        if javaClass.types.__len__() != 0:
            for field in javaClass.types[0].fields:
                # 判断变量内有没有 待选的类
                if collectionsVariablesWithOnlyClassName.__contains__(field.type.name):
                    for arrayVariable in collectionsVariables:
                        variableWithPackagePath = arrayVariable['package'] + '.' + arrayVariable['className']
                        # 这里就是判断当前变量是否是待选包里的类 「与当前类包一致 or  类+ 包名」
                        if arrayVariable['package'] == javaClass.package.name or isContainsImports(javaClass,
                                                                                                   variableWithPackagePath):
                            # 判断是否被调用 variable.put/add/insert/push  javaClass.types[0].methods[0].body[0].expression.qualifier  member  children[3][0].member
                            for method in javaClass.types[0].methods:
                                for body in method.body:
                                    try:
                                        if usedMethods.__contains__(body.expression.children[3][0].member) \
                                                and body.expression.qualifier[0:1].title()+body.expression.qualifier[1:] == arrayVariable['className'] \
                                                and body.expression.member == arrayVariable['name']:
                                            absoluteHasStatusVariables.append(arrayVariable)
                                    except:
                                        if str(body).__contains__(arrayVariable['className']+'.'+arrayVariable['nameOrigin']):
                                            absoluteHasStatusVariables.append(arrayVariable)
                                        else:
                                            print(javaClass.types[0].name+' method line is blank or no operation coding')


def analysis(sources):
    for item in sources:
        if item.types.__len__() != 0:
            isSingleTonClass = getSingleTonClass(item)
            if isSingleTonClass:
                for var in getCollectionVariables(item):
                    collectionsVariables.append(var)
                    collectionsVariablesWithOnlyClassName.append(var['className'])

    checkIsUsed(sources)
    print(absoluteHasStatusVariables)
