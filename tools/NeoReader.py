from typing import List



class NeoReader(NeoManager):
    def query_all_service_names(self):
        return self._execute_read(self._query_all_service_names)

    def query_calling_times(self, from_node, to_node):
        return self._execute_read(self._query_calling_times, from_node, to_node)

    def query_amount_of_chains(self):
        return self._execute_read(self._query_amount_of_chains)

    def get_high_frequency_path(self, limit):
        return self._execute_read(self._get_high_frequency_chain_path, limit)

    def get_low_frequency_path(self, limit):
        return self._execute_read(self._get_low_frequency_chain_path, limit)

    def get_chain_infos(self):
        return self._execute_read(self._get_chain_infos)

    def get_chain_start_node_names(self, chain_id):
        return self._execute_read(self._get_chain_start_node_names, chain_id)

    def get_chain_end_node_names(self, chain_id):
        return self._execute_read(self._get_chain_end_node_names, chain_id)

    def get_chain_all_shortest_paths(self, chain_id, start_node_name, end_node_name):
        return self._execute_read(self._get_all_shortest_paths_of_chains, chain_id, start_node_name, end_node_name)

    @staticmethod
    def _query_all_service_names(tx):
        result = tx.run("MATCH (n: SERVICE) return n.name")
        return [row['n.name'] for row in result]

    @staticmethod
    def _query_calling_times(tx, from_node, to_node):
        result = tx.run("MATCH (from_node {name: $from_node}), (to_node {name: $to_node}) "
                        "RETURN size((from_node)-->(to_node)) as times", from_node=from_node, to_node=to_node)
        return result.data()[0]['times']

    @staticmethod
    def _query_amount_of_chains(tx):
        query = "MATCH ()-[r:CHAINS]-() RETURN COUNT(DISTINCT(r.chain_id)) as total_size"
        return tx.run(query).data()[0]['total_size']

    @staticmethod
    def _get_high_frequency_chain_path(tx, limit: int):
        query = f"MATCH ()-[r:CHAINS]-() \
                RETURN distinct(r.chain_id) as chains_id, r.times as times ORDER BY times DESC LIMIT {limit}"
        return tx.run(query).data()

    @staticmethod
    def _get_low_frequency_chain_path(tx, limit: int):
        query = f"MATCH ()-[r:CHAINS]-() \
                RETURN distinct(r.chain_id) as chains_id, r.times as times ORDER BY times ASC LIMIT {limit}"
        return tx.run(query).data()

    @staticmethod
    def _get_chain_infos(tx) -> List[ChainInfo]:
        query = "MATCH p=()-[r:CHAINS]-() \
                WITH DISTINCT(r.chain_id) AS chain_id \
                CALL{ \
                    WITH chain_id \
                    MATCH (a)-[:CHAINS {chain_id: chain_id}]-() \
                    RETURN COLLECT(DISTINCT(a.name)) AS node_names \
                } \
                RETURN chain_id, node_names"
        query_result = tx.run(query).data()
        result: List[ChainInfo] = []
        for item in query_result:
            info = ChainInfo(item['chain_id'], item['node_names'])
            result.append(info)
        return result

    @staticmethod
    def _get_chain_start_node_names(tx, chain_id) -> List[str]:
        query = "MATCH (n)-[:CHAINS {chain_id: $chain_id}]-() \
                WITH n, size((n)<-[:CHAINS {chain_id: $chain_id}]-()) as in \
                WHERE in = 0 \
                RETURN DISTINCT(n.name) as name"
        return list(map(lambda n: n['name'], tx.run(query, chain_id=chain_id).data()))

    @staticmethod
    def _get_chain_end_node_names(tx, chain_id) -> List[str]:
        query = "MATCH (n)-[:CHAINS {chain_id: $chain_id}]-() \
                WITH n, size((n)-[:CHAINS {chain_id: $chain_id}]->()) as out \
                WHERE out = 0 \
                RETURN DISTINCT(n.name) as name"
        return list(map(lambda n: n['name'], tx.run(query, chain_id=chain_id).data()))

    @staticmethod
    def _get_all_shortest_paths_of_chains(tx, chain_id, start_node_name, end_node_name) -> List[str]:
        query = "MATCH p=ALLSHORTESTPATHS(({name: $start_node_name})-[r:CHAINS *]->({name: $end_node_name})) \
                WHERE ALL(r in relationships(p) WHERE r.chain_id = $chain_id) \
                RETURN nodes(p) as path_nodes"
        query_result = tx.run(query, chain_id=chain_id, start_node_name=start_node_name, end_node_name=end_node_name) \
            .data()
        result = []
        for item in query_result:
            string = [n['name'] for n in item['path_nodes']]
            string = ','.join(string)
            result.append(string)
        return result
