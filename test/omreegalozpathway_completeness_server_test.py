# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from omreegalozpathway_completeness.omreegalozpathway_completenessImpl import omreegalozpathway_completeness
from omreegalozpathway_completeness.omreegalozpathway_completenessServer import MethodContext
from omreegalozpathway_completeness.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class omreegalozpathway_completenessTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('omreegalozpathway_completeness'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'omreegalozpathway_completeness',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = omreegalozpathway_completeness(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    #def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        #ret = self.serviceImpl.run_omreegalozpathway_completeness(self.ctx, {'workspace_name': self.wsName,'main_input_ref': '32176/3/2'})


        """
    def test_kbase_genome(self):
        #enter name of existing reference, from Lauren's assembly 
        #The type of this data is: "KBaseGenomes.Genome‑10.0"

        ref = "321"
        ret = self.serviceImpl.run_omreegalozpathway_completeness(self.ctx, {
            'workspace_name': self.wsName,
            'main_input_ref': ref,
        })

        """


    """
    def test_FBA_Model(self):
        
        #This is an example FBAModel called SHW_Metabolic_Model
        ref = "32176/11/1"

        ret = self.serviceImpl.run_omreegalozpathway_completeness(self.ctx, {
            'workspace_name': self.wsName,
            'main_input_ref': ref,
        })

    """
    def test_Domain_Annotation(self):
        

        #This is an example TIGRFam Domain Annotation structure
        ref = "32176/26/1"

        ret = self.serviceImpl.run_omreegalozpathway_completeness(self.ctx, {
            'workspace_name': self.wsName,
            'main_input_ref': ref,
        })




