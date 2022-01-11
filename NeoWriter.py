from static_arch.neo_manage.NeoManager import NeoManager


class NeoWriter(NeoManager):
    def create_service(self, name):
        self._execute_write(self._create_service_node_with_name, name)

    def create_service_domain(self, name):
        self._execute_write(self._create_service_domain_node_with_name, name)

    def create_service_to_service_domain_relationship(self, src_node_name, dest_node_name, times):
        self._execute_write(self._create_calling_relationship_with_times_prop, src_node_name, dest_node_name, times)

    def clear_database(self):
        self._execute_write(self._clear_all)

    # def create_project_name(self, name):
    #     self._execute_write(self._create_project_name_with_name, name)
    #
    # def create_keyword(self, name):
    #     self._execute_write(self._create_keyword_with_name, name)

    def create(self, key, name):
        self._execute_write(self._create_with_name, key, name)

    # def create_package(self, name):
    #     self._execute_write(self._create_package_with_name, name)
    #
    # def create_keyword_relationship(self, name1, name2):
    #     self._execute_write(self._create_keyword_relationship, name1, name2)
    #
    # def create_package_relationship(self, name1, name2):
    #     self._execute_write(self._create_package_relationship, name1, name2)

    def create_relationship(self, key1, name1, key2, name2, linked_text):
        self._execute_write(self._create_relationship, key1, name1, key2, name2, linked_text)

    def create_property(self, node_name, property_name, property_value):
        self._execute_write(self._create_property, node_name, property_name, property_value)

    def check_exist_project_name(self, name):
        self._execute_write(self._check_project_name_exist, name)

    @staticmethod
    def _check_project_name_exist(tx, name):
        return tx.run("MATCH (a:projectName) where a.name=$name return a", name=name)

    @staticmethod
    def _create_with_name(tx, key, name):
        return tx.run("CREATE (a:" + key + ") SET a.name = $name", name=name)

    @staticmethod
    def _create_property(tx, node_name, property_name, property_value):
        return tx.run("MATCH (n { name: '" + node_name + "' })SET n." + property_name + " = '" + property_value + "'")

    # @staticmethod
    # def _create_project_name_with_name(tx, name):
    #     tx.run("CREATE (a:ProjectName) SET a.name = $name", name=name)
    #
    # @staticmethod
    # def _create_keyword_with_name(tx, name):
    #     tx.run("CREATE (b:Keyword) SET b.name = $name", name=name)
    #
    # @staticmethod
    # def _create_package_with_name(tx, name):
    #     tx.run("CREATE (c:Package) SET c.name = $name", name=name)
    #
    # @staticmethod
    # def _create_keyword_relationship(tx, name1, name2):
    #     tx.run("MATCH(a:ProjectName),(b:Keyword) where a.name = $name1 and b.name = $name2  CREATE (a)-["
    #            "r1:linked]->(b)", name1=name1, name2=name2)

    @staticmethod
    def _create_relationship(tx, key1, name1, key2, name2, linked_text):
        tx.run("MATCH(a:" + key1 + "),(b:" + key2 + ") where a.name = $name1 and b.name = $name2  CREATE (a)-["
                                                    "r1: "+linked_text+"]->(b)", name1=name1, name2=name2)

    @staticmethod
    def _create_package_relationship(tx, name1, name2):
        tx.run("MATCH(a:Keyword),(b:Package) where a.name = $name1 and b.name = $name2  CREATE (a)-["
               "r1:linked]->(b)", name1=name1, name2=name2)

    @staticmethod
    def _create_service_node_with_name(tx, name):
        tx.run("CREATE (a:Service) SET a.name = $name", name=name)

    @staticmethod
    def _create_service_domain_node_with_name(tx, name):
        tx.run("CREATE (a:ServiceDomain) SET a.name = $name", name=name)

    @staticmethod
    def _clear_all(tx):
        tx.run("MATCH p=()-->() DELETE p")
        tx.run("MATCH p=() DELETE p")

    @staticmethod
    def _create_calling_relationship_with_times_prop(tx, src_node_name, dest_node_name, times):
        tx.run("CREATE r=(:Service {name:$src_node_name})"
               " -[:has {times:$times}]-> "
               "(:ServiceDomain {name:$dest_node_name})",
               src_node_name=src_node_name, dest_node_name=dest_node_name, times=times)
