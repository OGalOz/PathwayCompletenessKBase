# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os


#from installed_clients.AssemblyUtilClient import AssemblyUtil
#from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.KBaseReportClient import KBaseReport
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
    GIT_COMMIT_HASH = "521bbaee75d8737ab820c97bd45a2c2ccafb2ccd"

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
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['main_input_ref']},
                                                'workspace_name': params['workspace_name']})

        report_info_string = str(report_info)


        #TEST FOR Genome type: KBaseGenomes.Genome???10.0
        #We want to download the file
        ref_num = params['main_input_ref']


        genome_dict = self.gfu.genome_to_gff({'genome_ref': ref_num})
        logging.info('what is the genome file: ' + str(type(genome_dict)))

        logging.info("the keys:")
        for k in genome_dict.keys():
            logging.info(str(k))
        


        f_path = genome_dict['file_path']

        #removing slashes from reference number
        ref_wo_slash = ref_num.replace('/','')


        #This is how you write to a file.
        test_local_log_file = os.path.join(self.shared_folder, ref_wo_slash)
        f=open(test_local_log_file, 'w')
        f.write(str(str(genome_dict)))
        f.close()


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
