# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from Bio import SeqIO


#from installed_clients.AssemblyUtilClient import AssemblyUtil
#from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.fba_toolsClient import fba_tools
from installed_clients.DomainAnnotationClient import DomainAnnotation
from biokbase.workspace.client import Workspace
from my_other_module.main_functions import reactions_file_to_pathway_reactions_and_percentages, TIGRFAM_file_to_pathway_reactions_and_percentages


#END_HEADER


class omreegalozpathway_completeness:
    '''
    Module Name:
    omreegalozpathway_completeness

    Module Description:
    A KBase module: omreegalozpathway_completeness
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/OGalOz/PathwayCompletenessKBase.git"
    GIT_COMMIT_HASH = "405a957e4d408fa9556927eaffcdf3bbbe36b12b"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        #self.dfu = DataFileUtil(self.callback_url)
        self.gfu = GenomeFileUtil(self.callback_url)
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.ws_url = config['workspace-url']

        #END_CONSTRUCTOR
        pass


    def run_omreegalozpathway_completeness(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_omreegalozpathway_completeness
        report_client = KBaseReport(self.callback_url)

        #"""
        report_info = report_client.create({'report': {'objects_created':[],
                                                'text_message': params['main_input_ref']},
                                                'workspace_name': params['workspace_name']})

        #end """

        #report_info_string = str(report_info)


        token = os.environ.get('KB_AUTH_TOKEN', None)
        upa = params['main_input_ref']

        ws = Workspace(self.ws_url, token=token)
        obj_info = ws.get_object_info3({'objects': [{'ref': upa}]})
        
        #logging.info(obj)
        #logging.info(obj['data'])


        object_name = obj_info["infos"][0][1]
        object_type = obj_info["infos"][0][2]
        logging.info("Object Type: " + object_type)
        ws_name = obj_info["infos"][0][7]
        logging.info("Object Info")
        logging.info(obj_info)     
        logging.info("Object Name: " + object_name)   
        logging.info("Workspace Name: " + ws_name)

        #This part is a hack, need to check type of data more accurately.
        if object_type[:17] == 'KBaseFBA.FBAModel':
            logging.info("Object type is FBA Model")
            fba_t = fba_tools(self.callback_url)
            X = fba_t.export_model_as_tsv_file({"input_ref": upa })
            reactions_file_path = os.path.join(self.shared_folder, object_name + '/' + object_name + '-reactions.tsv')
            output_path = os.path.join(self.shared_folder, 'check_path_complete.tsv')
            bug_filepath = reactions_file_path
            reactions_file_to_pathway_reactions_and_percentages(bug_filepath, output_path)            
        elif object_type[:34] == "KBaseGeneFamilies.DomainAnnotation":
            logging.info("Succesfully recognized type as Domain Annotation")
            da = DomainAnnotation(self.callback_url)
            obj = ws.get_objects2({'objects': [{'ref': upa}]})
            Y = obj['data'][0]['data']['data']
            output_file_path = os.path.join(self.shared_folder,'test-data-2.tsv')
            TIGRFAM_file_to_pathway_reactions_and_percentages(Y, output_file_path)
            
        else:
            logging.info("Object type unknown")
       

        html_path = os.path.join(self.shared_folder, 'check_path_complete.html')

        html_dict = [{"path" : html_path, "name" : 'Completeness_Table'}]

          
        """Start Comment

        #If type is TIGRFAM domain annotations, type_id = 0###
        if type_id == 0 :
            TIGRFAM_file_to_pathway_reactions_and_percentages(bug_filepath, output_path)

        #If type is Prokka domain annotations###
        elif type_id == 2 :
            logging.info("Prokka incomplete")
        else :
            logging.info("Could not get type of data")

        Stop Comment"""


        #genome_gff_dict = self.gfu.genome_to_gff({'genome_ref': ref_num})
        #logging.info('what is the genome file: ' + str(type(genome_dict)))


        #Getting genbank info
        #genome_genbank = self.gfu.genome_to_genbank({'genome_ref': ref_num})

        #converting the genbank file into readable format using BioPython: unclear if this will work.
        #record = SeqIO.read(genome_genbank, "genbank")


        


        #test_local_log_file = os.path.join(self.shared_folder, ref_wo_slash)
        #f=open(test_local_log_file, 'w')
        #f.write(str(str(genome_dict)))
        #f.close()


        """
        #Testing New Material Sept 10th:
        #TIGRFAM DOMAIN ANNOTATION FILE!
        bug_filepath = '/kb/module/data/HL1H-Tigrfam-Domain-Annot.csv'
        output_path = os.path.join(self.shared_folder, 'tfam_to_pathways.tsv')
        TIGRFAM_file_to_pathway_reactions_and_percentages(bug_filepath, output_path)       
        """
        #Testing New Material Sept 11th:
        #Downloading TSV file from FBA Model given reference number
        #ref_num = params['main_input_ref']
        #bug_filepath = '/kb/module/data/kb|g.220339.fbamdl0-reactions.tsv'
        #output_path = os.path.join(self.shared_folder, 'check_path_complete.tsv')
        #reactions_file_to_pathway_reactions_and_percentages(bug_filepath, output_path)

 
        """
        report = report_client.create_extended_report({

        'direct_html_link_index': 0,
        'message' : 'Here are the pathway completeness results',
        'workspace_name' : ws_name,
        'html_links' : html_dict

        })
        """


        #later change report_info to report
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_omreegalozpathway_completeness

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_omreegalozpathway_completeness return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
