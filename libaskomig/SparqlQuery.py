import random
from SPARQLWrapper import SPARQLWrapper, JSON

class SparqlQuery():

    def __init__(self, endpoint, user_graph, prefix):

        self.endpoint = endpoint
        self.user_graph = user_graph
        self.prefix = prefix

    def sparql_query(self, query):

        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()["results"]["bindings"]

        res_list = []
        seen = set()
        for result in results:
            res_dict = {}
            for key in result:
                res_dict[key] = result[key]['value']
            res_list.append(res_dict)
        return res_list

    def get_rdf_users(self):

        query_user = '''
        PREFIX : <%s>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?URIusername ?username ?email ?admin ?blocked ?password ?salt ?apikey ?Gurl ?Gkey
        WHERE {
                GRAPH <%s> {
                    ?URIusername rdf:type foaf:Person .
                    ?URIusername foaf:name ?username .
                    ?URIusername foaf:mbox ?email .
                    ?URIusername :isadmin ?admin .
                    ?URIusername :isblocked ?blocked .
                    ?URIusername :password ?password .
                    ?URIusername :randomsalt ?salt .
                    OPTIONAL {
                        ?URIusername :keyid ?URIkeyid .
                        ?URIkeyid rdfs:label ?keyname .
                        ?URIkeyid :key ?apikey .
                    }
                    OPTIONAL {
                        ?URIusername :galaxy_instance ?Ginstance .
                        ?Ginstance rdf:type :galaxy .
                        ?Ginstance :galaxy_url ?Gurl .
                        ?Ginstance :galaxy_key ?Gkey .
                    }
                }
        }
        ''' % (self.prefix, self.user_graph)

        rdf_users = self.sparql_query(query_user)

        seen = set()
        uniq_rdf_users = []
        for user in rdf_users:
            uri = user['URIusername']
            user['admin'] = True if user['admin'] == '1' else False
            user['blocked'] = True if user['blocked'] == '1' else False
            user['email'] = user['email'].replace('mailto:', '')
            if 'apikey' not in user:
                user['apikey'] = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(20))
            if uri not in seen:
                seen.add(uri)
                uniq_rdf_users.append(user)

        return uniq_rdf_users
