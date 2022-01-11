import os

from py2neo import NodeMatcher, Graph

from static_arch.neo_manage.NeoWriter import NeoWriter

collection_keywords = [
    # 集合
    'Vector',
    'Stack',
    'HashSet',
    'TreeSet',
    'LinkedHashMap',
    'LinkedHashSet',
    'ArrayList',
    'LinkedList',
    'WeakHashMap',
    'Hashtable',
    'IdentityHashMap',
    'HashMap',
    'SortedMap',
    'Queue',
    'TreeMap',
    'ConcurrentHashMap',
    # 'Map',
    'CopyOnWriteArrayList',
    'LinkedList']
cache_keywords = [
    # 缓存框架
    # 'GuavaCacheManager',
    # 'CacheManager',
    # 'LoadingCache',
    # 'CacheLoader',
    'Cache',
    'Caffeine'
]
match_items = {}

resluts = []

counter = {

}
primary_key_counter = {
    'index': 1
}


def dir_walk(dirname):
    for i in os.listdir(dirname):
        filename = os.path.join(dirname, i)

        if os.path.isfile(filename) & filename.endswith(".java"):
            open_flie(filename)

        if os.path.isdir(filename):
            dir_walk(filename)


def open_flie(file_name):
    with open(file_name, encoding='utf8') as f:
        match_sentense = f.readlines()
        match_sentenses = [x.replace('\n', '').strip(' ') for x in match_sentense if 'import' not in x]
        for define in match_sentenses:
            if 'package' in define:
                temp_package = define
            for key in collection_keywords:
                if key in define:
                    if 'static' in define and '=' in define:
                        find_variable(define, f, file_name, key, match_sentenses, temp_package)
            for key in cache_keywords:
                if key in define:
                    if '.put' not in define and '.add' not in define and '.remove' not in define and '.pop' not \
                            in define and '.insert' not in define:
                        find_variable(define, f, file_name, key, match_sentenses, temp_package)

                    # resluts.push(match_items)


def find_variable(define, f, file_name, key, match_sentenses, temp_package):
    index_end = define.index('=', 0, len(define))
    if '>' in define and define.index('>') < index_end:
        index_start = define.index('>', 0, index_end) + 1
        if index_start != 1:
            variable_name = define[index_start: index_end].strip()
            primary_key_counter['index'] = primary_key_counter['index'] + 1
            build_model(define, f, file_name, key, match_sentenses, temp_package,
                        variable_name)


def build_model(define, f, file_name, key, match_sentenses, temp_package, variable_name):
    for impl in match_sentenses:
        if (variable_name + '.put') in impl or (
                variable_name + '.add') in impl or (
                variable_name + '.remove') in impl or (
                variable_name + '.pop') in impl or (
                variable_name + '.insert') in impl:
            strip = file_name[len(dirname) + 1:len(file_name)]
            project_name = strip[0:strip.index("/")]
            match_items['keyword'] = key
            match_items['project_name'] = project_name
            match_items['package'] = temp_package
            match_items['define'] = define
            match_items['impl'] = impl
            class_name = f.name[
                         len(f.name) - f.name[::-1].index('/'): len(
                             f.name)] + '  <' + project_name + '>'
            build_neo4j(class_name, define, f, impl, key, project_name, temp_package)
            # neo_manager.create_relationship('define', define, 'impl', impl)


def build_neo4j(class_name, define, f, impl, key, project_name, temp_package):
    project_name_key = 'project'
    keyword_key = 'keyword'
    package_key = 'package'
    class_name_key = 'class'
    defined_in_relation_ship = 'defined_in'
    contains_relation_ship = 'contains'
    if nodeMatcher.match(project_name_key).where(
            "_.name=~ '" + project_name + "'").first() is None:
        neo_manager.create(project_name_key, project_name)

    if nodeMatcher.match(keyword_key).where("_.name=~ '" + key + "'").first() is None:
        neo_manager.create(keyword_key, key)

    if nodeMatcher.match(package_key).where(
            "_.name=~ '" + temp_package + "'").first() is None:
        neo_manager.create(package_key, temp_package)
    absolute_define = define + str(primary_key_counter['index'])

    if nodeMatcher.match(class_name_key).where(
            "_.name=~ '" + class_name + "'").first() is None:
        neo_manager.create(class_name_key, class_name)
    # neo_manager.create('impl', impl)

    neo_manager.create_relationship(keyword_key, key, project_name_key, project_name,
                                    defined_in_relation_ship)
    neo_manager.create_relationship(project_name_key, project_name, package_key,
                                    temp_package, contains_relation_ship)
    neo_manager.create_relationship(package_key, temp_package, class_name_key,
                                    class_name,
                                    contains_relation_ship)
    if counter.__contains__(absolute_define):
        counter[absolute_define] = counter[absolute_define] + 1
    else:
        counter[absolute_define] = 1
    neo_manager.create_property(class_name, 'path', f.name)
    neo_manager.create_property(class_name,
                                'define', absolute_define)
    neo_manager.create_property(class_name,
                                'impl' + str(counter[absolute_define]), impl)


if __name__ == '__main__':
    uri = 'bolt://localhost:7687'
    user = 'neo4j'
    password = '123'
    neo_manager = NeoWriter(uri, user, password)
    neo_manager.clear_database()
    graph = Graph(uri, username=user, password=password)
    nodeMatcher = NodeMatcher(graph)
    dirname = r'/Users/jiahao.zhang/Documents/coding/on_boarding/wfc'  # r是转义，要不就用双斜杠
    # dirname = r'/Users/jiahao.zhang/Documents/coding/on_boarding/ysg'  # r是转义，要不就用双斜杠
    # dirname = r'/Users/jiahao.zhang/Documents/coding/open-source/service-status-module'  # r是转义，要不就用双斜杠
    dir_walk(dirname)
