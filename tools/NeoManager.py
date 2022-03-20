from neo4j import GraphDatabase, Driver



class NeoManager:
    __driver: Driver = None
    __uri: str = None
    __user_name: str = None
    __password: str = None

    instance = None

    def __init__(self):
        if self.__driver is None:
            self.__uri = get_arg('NEO4J_HOST')
            self.__user_name = get_arg('NEO4J_USER_NAME')
            self.__password = get_arg('NEO4J_PASSWORD')
            if self.__uri is None:
                self.__uri = config_read('neo4j', 'uri')
                self.__user_name = config_read('neo4j', 'user')
                self.__password = config_read('neo4j', 'password')
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user_name, self.__password))
            self.instance = self

    def __del__(self):
        if self.__driver is not None:
            self.__driver.close()

    def _execute_write(self, tx, *args):
        with self.__driver.session() as session:
            session.write_transaction(tx, *args)

    def _execute_read(self, tx, *args):
        with self.__driver.session() as session:
            return session.read_transaction(tx, *args)
