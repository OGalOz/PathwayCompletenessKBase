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

        #Preparing report client
        report_client = KBaseReport(self.callback_url)

        #Original report info
        report_info = report_client.create({'report': {'objects_created':[],
                                                'text_message': params['main_input_ref']},
                                                'workspace_name': params['workspace_name']})

        token = os.environ.get('KB_AUTH_TOKEN', None)


        #Checking the input params
        if "main_input_ref" in params:
            main_input_ref = params['main_input_ref']
        else:
            logging.info('the reference number is not in the params, program must end.')
            raise Exception("main_input_ref not in params")

        #Creating the workspace client object
        ws = Workspace(self.ws_url, token=token)

        #Getting information about the main input ref
        obj_info = ws.get_object_info3({'objects': [{'ref': main_input_ref}]})


        #Catching errors: 
        if "infos" in obj_info:
            #Getting information from object reference number
            object_name = obj_info["infos"][0][1]
            object_type = obj_info["infos"][0][2]
            ws_name = obj_info["infos"][0][7]

            #Logging:
            logging.debug("Object Type: " + object_type)
            logging.debug("Object Name: " + object_name)   
            logging.debug("Workspace Name: " + ws_name)
        else:
            logging.info("The function ws.get_object_info3 failed to download the right information. The program must abort.")
            raise Exception("Could not find infos in obj_info")
        
        #We create the output file name and add information to it later.
        output_file_name = 'pathways_measurements'

        #This part is a hack, need to check type of data more accurately.
        if object_type[:17] == 'KBaseFBA.FBAModel':
            logging.info("Succesfully recognized type as FBA Model")

            #Preparing the output file name which we return to the user
            output_file_name += '_fba_model'

            #Creating an fba tools object
            fba_t = fba_tools(self.callback_url)

            # Getting the TSV file from the object
            X = fba_t.export_model_as_tsv_file({"input_ref": main_input_ref })

            # Logging
            logging.info("the object output from fba tools export model as tsv file:")
            logging.info(X)

            #Locating where the reactions tsv was placed (Not well done- replace this with a robust form)
            reactions_file_path = os.path.join(self.shared_folder, object_name + '/' + object_name + '-reactions.tsv')

            #Preparing an output path for a future function
            output_path = os.path.join(self.shared_folder, output_file_name + '.tsv')

            #This function performs the percentage calculation work for FBAModel Object Types.
            html_path = reactions_file_to_pathway_reactions_and_percentages(reactions_file_path, output_path, object_name)            
        
        # Using KBase Gene Families- Domain Annotation
        elif object_type[:34] == "KBaseGeneFamilies.DomainAnnotation":
            logging.info("Succesfully recognized type as Domain Annotation")
            output_file_name += '_domain_annotation'

            #We get the object using workspace's get_objects2 function
            obj = ws.get_objects2({'objects': [{'ref': main_input_ref}]})
        
            #Within the way the object dictionary is given, what we are looking for is in the location as follows:
            Y = obj['data'][0]['data']['data']

            #Preparing our own output_file_path with Domain Annotation instead of FBAModel (why?)
            output_file_path = os.path.join(self.shared_folder, output_file_name + '.tsv')

            #This function (written for the module) finds percentages of pathway completeness.
            html_path = TIGRFAM_file_to_pathway_reactions_and_percentages(Y, output_file_path, object_name)
            
        else:
            logging.info("Object type unknown")
            raise Exception("Could not recognize ref to object- Check if object is FBA Model or Domain Annotation type. If so, the error is in the program, not the input - contact ogaloz@lbl.gov.")
       



        html_dict = [{"path" : html_path, "name" : 'Completeness_Table'}]


        #Preparing final report:
        report = report_client.create_extended_report({

        'direct_html_link_index': 0,
        'message' : 'Here are the pathway completeness results',
        'workspace_name' : ws_name,
        'html_links' : html_dict

        })


        output = {
            'report_name': report['name'],
            'report_ref': report['ref'],
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
