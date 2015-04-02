# -*- coding: utf-8 -*-

import pytest
import sys
import cPickle as pickle
import time
from test_base_class import TestBaseClass

try:
    import aerospike
except:
    print "Please install aerospike python client."
    sys.exit(1)

class TestInfo(object):

    def setup_class(cls):

        """
        Setup class.
        """
        hostlist, user, password = TestBaseClass.get_hosts()
        config = {
                'hosts': hostlist
                }
        if user == None and password == None:
            TestInfo.client = aerospike.client(config).connect()
        else:
            TestInfo.client = aerospike.client(config).connect(user, password)

    def teardown_class(cls):

        """
        Teardoen class.
        """

        TestInfo.client.close()

    def test_info_for_statistics(self):

        request = "statistics"

        nodes_info = TestInfo.client.info(request, [('127.0.0.1', 3000)])

        assert nodes_info != None

        assert type(nodes_info) == dict

    def test_info_positive_for_namespace(self):
        """
        Test info positive for namespace
        """
        key = ('test', 'demo', 'list_key')

        rec = {
                'names': ['John', 'Marlen', 'Steve']
            }

        TestInfo.client.put(key, rec)
        response = TestInfo.client.info('namespaces', [('127.0.0.1', 3000)])
        TestInfo.client.remove(key)
        flag = 0
        for keys in response.keys():
            for value in response[keys]:
                if value != None:
                    if 'test' in value:
                        flag = 1
        if flag:
            assert True == True
        else:
            assert True == False

    def test_info_positive_for_sets(self):
        """
        Test info positive for sets
        """
        key = ('test', 'demo', 'list_key')

        rec = {
                'names': ['John', 'Marlen', 'Steve']
            }

        TestInfo.client.put(key, rec)
        response = TestInfo.client.info('sets', [('127.0.0.1', 3000)])
        TestInfo.client.remove(key)
        flag = 0
        for keys in response.keys():
            for value in response[keys]:
                if value != None:
                    if 'demo' in value:
                        flag = 1
        if flag:
            assert True == True
        else:
            assert True == False

    def test_info_positive_for_bins(self):
        """
        Test info positive for bins
        """
        key = ('test', 'demo', 'list_key')

        rec = {
                'names': ['John', 'Marlen', 'Steve']
            }

        TestInfo.client.put(key, rec)
        response = TestInfo.client.info('bins', [('127.0.0.1', 3000)])
        TestInfo.client.remove(key)
        flag = 0
        for keys in response.keys():
            for value in response[keys]:
                if value != None:
                    if 'names' in value:
                        flag = 1
        if flag:
            assert True == True
        else:
            assert True == False

    def test_info_positive_for_sindex_creation(self):
        """
        Test info for secondary index creation
        """
        key = ('test', 'demo', 'list_key')

        rec = {
                'names': ['John', 'Marlen', 'Steve']
            }
        policy = {}
        TestInfo.client.put(key, rec)
        response = TestInfo.client.info('sindex-create:ns=test;set=demo;indexname=names_test_index;indexdata=names,string', [('127.0.0.1', 3000)])
        time.sleep(2)
        TestInfo.client.remove(key)
        response = TestInfo.client.info('sindex', [('127.0.0.1', 3000)])
        TestInfo.client.info('sindex-delete:ns=test;indexname=names_test_index', [('127.0.0.1', 3000)])

        flag = 0
        for keys in response.keys():
            for value in response[keys]:
                if value != None:
                    if 'demo' in value:
                        flag = 1
        if flag:
            assert True == True
        else:
            assert True == False

    def test_info_with_config_for_statistics(self):

        request = u"statistics"

        config = [(127, 3000)]

        with pytest.raises(Exception) as exception:
            TestInfo.client.info(request, config)

        assert exception.value[0] == -2
        assert exception.value[1] == "Host address is of type incorrect"

    def test_info_with_config_for_statistics_and_policy(self):

        request = "statistics"

        config = [('127.0.0.1', 3000)]

        policy = {
                'timeout': 1000
        }
        nodes_info = TestInfo.client.info(request, config, policy)

        assert nodes_info != None

        assert type(nodes_info) == dict

    def test_info_for_invalid_request(self):

        request = "no_info"

        nodes_info = TestInfo.client.info(request, [('127.0.0.1', 3000)])

        assert type(nodes_info) == dict

        assert nodes_info.values() != None

    def test_info_with_none_request(self):

        request = None

        with pytest.raises(Exception) as exception:
            TestInfo.client.info(request, [('127.0.0.1', 3000)])

        assert exception.value[0] == -2L
        assert exception.value[1] == "Request must be a string"

    def test_info_without_parameters(self):

        with pytest.raises(TypeError) as typeError:
            nodes_info = TestInfo.client.info()

        assert "Required argument 'command' (pos 1) not found" in typeError.value

    def test_info_positive_for_sets_without_connection(self):
        """
        Test info positive for sets without connection
        """
        config = {
                'hosts': [('127.0.0.1', 3000)]
                }
        
        client1 = aerospike.client(config)
        with pytest.raises(Exception) as exception:
            response = client1.info('sets', [('127.0.0.1', 3000)])

        assert exception.value[0] == 11L
        assert exception.value[1] == 'No connection to aerospike cluster'
