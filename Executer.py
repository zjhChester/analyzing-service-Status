import os

import javalang

import analysis.CollectionsAnalysis as collectionsAnalysis
import analysis.ObjectsAnalysis as objectsAnalysis

javaFiles = []
errorParseJavaFiles = []


def dir_walk(dirname):
    for i in os.listdir(dirname):
        filename = os.path.join(dirname, i)

        if os.path.isfile(filename) and filename.endswith(".java") and filename.__contains__("Test") == False:
            open_file(filename)

        if os.path.isdir(filename):
            dir_walk(filename)


def open_file(file_name):
    with open(file_name, encoding='utf8') as f:
        java_file_content = ""
        for line in f.readlines():
            java_file_content += line

    try:
        java_file = javalang.parse.parse(java_file_content)
        javaFiles.append(java_file)
    except:
        errorParseJavaFiles.append(file_name)


if __name__ == '__main__':
    # dirPath = r'/Users/jiahao.zhang/Documents/coding/on_boarding/ysg'  # r是转义，要不就用双斜杠
    dirPath = r'/Users/jiahao.zhang/Documents/coding/open-source/analyzing-service-status/javaFile'  # r是转义，要不就用双斜杠
    dir_walk(dirPath)
    collectionsAnalysis.analysis(javaFiles)
    objectsAnalysis.analysis(javaFiles)
    print("hello world")
