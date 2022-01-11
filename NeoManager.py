from neo4j import GraphDatabase, Driver, Query


class NeoManager:
    __driver: Driver = None

    def __init__(self, uri, user, password):
        self.__driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        if self.__driver is not None:
            self.__driver.close()

    def _execute_write(self, tx, *args):
        with self.__driver.session() as session:
            session.write_transaction(tx, *args)
