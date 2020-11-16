import json
import sys

AMMOUNT_OUTSTANDING = 'amount_outstanding'
TYPE = 'type'
ID = 'id'
YIELD = 'yield'
TENOR = 'tenor'
CORPORATE = 'corporate'
GOVERNMENT = 'government'
CORPORATE_BOND_ID = 'corporate_bond_id'
GOVERNMENT_BOND_ID = 'government_bond_id'
SPREAD_TO_BENCHMARK = 'spread_to_benchmark'
DATA = 'data'


def isolate_data(input_data, debug=False):
    ''' (list of dicts) -> (dict, dict)
    Returns two dictionaries isolating the corporate and government data alongisde validating each entry
    Each entry in both dictionaries will be in the format:
    
    {id:
    {   AMMOUNT_OUTSTANDING:amount_outstanding,
        YIELD:yield, 
        TENOR:tenor
    }}
    '''
    corporates = {}
    goverments = {}
    for entry in input_data:
        # validate if each entry in the json file is in the correct format and not missing any data
        amount_outstanding_exist = AMMOUNT_OUTSTANDING in entry and entry[AMMOUNT_OUTSTANDING]
        type_exist = TYPE in entry and entry[TYPE]
        id_exist = ID in entry and entry[ID]
        yeild_exist = YIELD in entry and entry[YIELD]
        tenor_exist = TENOR in entry and entry[TENOR]
        if not (amount_outstanding_exist and tenor_exist and id_exist and yeild_exist and tenor_exist):
            continue
        yield_entry = float(yeild_exist.strip('%'))
        tenor_entry = float(tenor_exist.split()[0])
        dict_entry = {AMMOUNT_OUTSTANDING: amount_outstanding_exist,
                      YIELD: yield_entry, TENOR: tenor_entry}
        if type_exist == CORPORATE:
            corporates[str(id_exist)] = dict_entry
        elif type_exist == GOVERNMENT:
            goverments[str(id_exist)] = dict_entry
    return corporates, goverments


def spread_data(corporates, goverments, debug=False):
    ''' (dict, dict) -> list of dicts
    Returns list of dictionaries matching and each corporate bond to nearest government bond
    Each element in the list will be in the format:
    {
       CORPORATE_BOND_ID:corporate_id 
       GOVERNMENT_BOND_ID:government_id 
       SPREAD_TO_BENCHMARK: bps
    }
    '''
    outData = []
    for ck, cv in corporates.items():
        min_gk = None
        min_tenor = float('inf')
        if goverments == {}:
            continue
        for gk, gv in goverments.items():
            if debug:
                print('gk:',gk,'gv:',gv,'ck:',ck,'cv:',cv,'min_gk:',min_gk,'min_tenor:',min_tenor)
            tenor = round(abs(cv[TENOR] - gv[TENOR]),5)
            gt_tenor = min_tenor > tenor
            eql_tenor = (min_tenor == tenor and min_tenor != None and 
                gv[AMMOUNT_OUTSTANDING] > min_gk[AMMOUNT_OUTSTANDING])
            no_min_tenor = min_gk == None
            if debug:
                print('tenor:',tenor, 'gt_tenor:', gt_tenor, 'eql_tenor:', eql_tenor, 'no_min_tenor:',no_min_tenor)
            if no_min_tenor or gt_tenor or eql_tenor:
                min_tenor = round(tenor, 5)
                min_gk = gk
        if debug:
            print('ck:',ck,'cv:',cv,'min_gk:',min_gk,'min_tenor:',min_tenor)
        bps = round((cv[YIELD] - goverments[min_gk][YIELD]) * 100)
        bps_str = str(bps).split('.')[0]
        outentry = {CORPORATE_BOND_ID: ck, GOVERNMENT_BOND_ID: min_gk,
                    SPREAD_TO_BENCHMARK: bps_str + ' bps'}
        outData.append(outentry)
    return outData

def main(argv, debug=False):
    # defines how to use this script
    def usage():
        print('Usage: python common.py inputFile.json, outputFile.json')
        return
    # check if the script has correct arguments
    if len(argv) != 3:
        usage()
        return 1
    # get the arguments passed in the file
    inputFile = argv[1]
    outputFile = argv[2]
    # open the input json file
    with open(inputFile) as f:
        data = json.loads(f.read())
    if not data:
        usage()
        return 1
    # loop over each entry isolating the goverment bonds and corporate bonds
    corporates, goverments = isolate_data(data[DATA], debug=debug)
    # "Spread" the data
    out_data = spread_data(corporates, goverments, debug=debug)
    # Output the data to a new file
    outJson = json.dumps({DATA: out_data})
    with open(outputFile, 'w') as f:
        f.write(outJson)
    return 0


if __name__ == "__main__":
    exit_code = main(sys.argv)
    # exit(exit_code)