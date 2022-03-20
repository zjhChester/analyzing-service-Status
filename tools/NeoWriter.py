from typing import List



class NeoWriter(NeoManager):
    def exec(self, statement):
        self._execute_write(self._exec, statement)

    def clear_database(self):
        self._execute_write(self._clear_all)

    def create_dynamic_arch_relationships(self, relationships: List[Relationship]):
        self.clear_database()
        for index, relationship in enumerate(relationships):
            total = len(relationships)
            print(f'saving relationship: {index + 1} / {total}')
            self.create_single_dynamic_arch_relationship(relationship)

    def create_single_dynamic_arch_relationship(self, relationship: Relationship):
        self._execute_write(self._exec, relationship.from_node.get_neo_merge_node_statement())
        self._execute_write(self._exec, relationship.to_node.get_neo_merge_node_statement())
        self._execute_write(self._exec, relationship.get_neo_merge_relationship_statement())

    def create_calling_relationship(self, from_node_name, to_node_name, times):
        self._execute_write(self._create_calling_relationship, from_node_name, to_node_name, times)

    def set_degrees(self, node_name):
        self._execute_write(self._set_node_degrees, node_name)

    def remove_all_calling_relationships(self):
        self._execute_write(self._remove_all_calling_relationships)

    @staticmethod
    def _create_calling_relationship(tx, from_node, to_node, times):
        tx.run("MATCH (from_node :SERVICE {name: $from_node}), (to_node :SERVICE {name: $to_node}) "
               "MERGE (from_node)-[:CALLING {times: $times}]->(to_node)",
               from_node=from_node, to_node=to_node, times=times)

    @staticmethod
    def _remove_all_calling_relationships(tx):
        tx.run("MATCH ()-[r:CALLING]-() DELETE r")

    @staticmethod
    def _set_node_degrees(tx, node_name):
        tx.run("MATCH (n {name: $node_name}) "
               "WITH size((n)-->()) as out, size((n)<--()) as in, n "
               "SET n.degree_in = in, n.degree_out = out", node_name=node_name)

    @staticmethod
    def _exec(tx, statement):
        tx.run(statement)

    @staticmethod
    def _clear_all(tx):
        tx.run("MATCH p=()-->() DELETE p")
        tx.run("MATCH p=() DELETE p")
