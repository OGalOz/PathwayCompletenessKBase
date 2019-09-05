/*
A KBase module: omreegalozpathway_completeness
*/

module omreegalozpathway_completeness {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_omreegalozpathway_completeness(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
