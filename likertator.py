#coding: UTF-8

#########################################
# likertator.py                         #
# Author: Matthew A. Tucker             #
# NYUAD Language, Mind, and Brain Lab   #
# Email: matt.tucker@nyu.edu            #
# Revision 1.0/ 12 August 2014          #
#########################################

import os
import sys
import random
import subprocess
import math

def parse_config():
    """Parse the config file for this likert task, assumed to be in inputs/config.txt"""
    
    # begin parsing config file
    print "Parsing configuration File..."
    try:
        config_f = open("config.txt", "r")
    except IOError as e:
        print "Could not open configuration file; please make sure inputs/config.txt exists and can be read by python."
        sys.exit()
    
    ret_val = {}
    
    # allocate each config param to a dictionary
    for l in config_f:
        line = l.strip().split()
        ret_val[line[0]] = line[1]
    
    config_f.close()
    
    return ret_val
        
    
def parse_stimuli(stim_file = None, no_conds = 0):
    """Parse the stimuli for this likert task, assumed to be in the file specified as stim_file. We assume the number of conditions to be no_conds."""
    if no_conds <= 1:
        print "There must be at least two conditions. Please specify more conditions in config.txt"
        sys.exit()
        
    try:
        stim_f = open(stim_file, 'r')
    except IOError as e:
        print "Could not open the stimuli file %s. Please make sure it exists, is openable, and is in the inputs/ directory." % stim_file
        
    print "Parsing stimuli file..."
        
    item_ctr = 1
    item_count = 1
    ret_val = []
    this_item = {}
    
    for l in stim_f:
        if item_ctr > no_conds:
            if not len(this_item) == no_conds:
                print "Something is wrong with one of the items. There is an mismatch between item number %i and the number of conditions, which is specified as %i." (item_count, no_conds)
                sys.exit()
                
            ret_val.append((item_count, this_item))
            this_item = {}
            item_ctr = 1
            item_count += 1
            continue
        else:
            this_item[item_ctr] = l.strip()
            item_ctr += 1
    
    # put the last item in
    if not len(this_item) == no_conds:
        print "Something is wrong with one of the items. There is an mismatch between item number %i and the number of conditions, which is specified as %i." (item_count, no_conds)
        sys.exit()
        
    ret_val.append((item_count, this_item))
    item_count += 1
    
    stim_f.close()
            
    return (item_count - 1, ret_val)
    
    
def parse_fillers(fill_file = None):
    """Parse the fillers for this likert task, assumed to be in the file specified as fill_file."""
    try:
        stim_f = open(fill_file, 'r')
    except IOError as e:
        print "Could not open the stimuli file %s. Please make sure it exists, is openable, and is in the inputs/ directory." % fill_file
        
    print "Parsing fillers file..."
        
    ret_val = []
    fill_count = 1
    
    for l in stim_f:
        ret_val.append((fill_count, l.strip()))
        fill_count += 1
        
    stim_f.close()
        
    return (fill_count - 1, ret_val)
    
def check_ratio(ratio = "1:1", fillers_count = None, items_count = None):
    """Check to make sure the fillers and items counts match the filler to item ratio that is specified in the config.txt file."""
    f_ratio = ratio.split(':')
    
    if not (math.floor(fillers_count / items_count) == math.floor(int(f_ratio[0]) / int(f_ratio[1]))):
        print "Fillers (%i) and items (%i) counts do not match the filler:item ratio specified in config.txt. You should check to make sure everything is correct in this regard." % (int(f_ratio[0]), int(f_ratio[1]))
        sys.exit()
        
def get_list_items(items = None, list_no = 0, no_lists = 0):
    """Get just the conditions from items which appear in list number list_no in the Latin Square, along with their item numbers/conditions."""

    if list_no < 1 or list_no > no_lists:
        print "This list number (%i) is invalid. It must be between 1 and %i, the number of lists specified in config.txt" % (list_no, no_lists)
        sys.exit()
        
    ret_val = []
        
    for item in items:
        # here's steve's hack to latin square
        this_cond = item[0] % no_lists + 1
        this_cond = this_cond - (list_no - 1)
        
        if this_cond <= 0:
            this_cond += no_lists
        
        ret_val.append((str(item[0]) + '-' + str(this_cond),item[1][this_cond]))
        
    return ret_val
    
def exify_item(item = None):
    """Takes an item and inserts it into a line template in latex. """
    return "\\begin{flushright}\n\\textarabic{%s}\n\\end{flushright}\n\n" % item
    
def write_likert_document(items = None, list_no = 0, exp_name = None, template = None):
    """Write out a XeLaTeX document for compilation containing an Arabic Likert task with items as Latin Square list number list_no."""
    
    write_val = template
    ret_val = []
    
    # construct the items
    items_list = ""
    for item in items:
        # save the item identifer so we know what's in this list and in what order
        ret_val.append(item[0])
        
        this_item = exify_item(item[1])
        
        # add the likert scale
        this_item += """\\begin{center}
        \\hfill\\textarabic{٧}\\hfill\\textarabic{٦}\\hfill\\textarabic{٥}\\hfill\\textarabic{٤}\\hfill\\textarabic{٣}\\hfill\\textarabic{٢}\\hfill\\textarabic{١}
        \\end{center}\n\n\n\\vspace{0.5\\baselineskip}"""
        
        items_list += this_item
        
    context = {
        "listno" : str(list_no),
        "expname" : exp_name,
        "items" : items_list
    }
    
    # do the replacement
    f_name = exp_name + "-List-" + str(list_no) + ".tex"
    
    try:
        with open(f_name, 'w') as out_f:
            out_f.write(template.format(**context))
            out_f.close()
    except IOError as e:
        print "There was a problem opening or writing to the output file for List no. %i. Please ensure permissions, etc. are correct." % list_no
#    except KeyError as e:
#        print e.args[0]

    return ret_val
        
    
def parse_template(tex_template = None):
    """Parse the template file given by tex_template into a string for use later in writing to individual lists."""
    
    try:
        with open(tex_template, 'r') as tex_f:
            ret_val = tex_f.read()
            return ret_val
    except IOError as e:
        print "There was no template file %s, or it was not openable. Please ensure it exists." % tex_template
        sys.exit()
    
def main():
    """Main entry point for likerator."""
    
    # ensure inputs directory exists and change to it.
    if not os.path.isdir(os.path.join(os.getcwd(), "inputs/")):
        print "An inputs folder containing config.txt and other necessary files must exist."
        sys.exit()
    else:
        os.chdir(os.path.join(os.getcwd(), "inputs/"))
        
    # parse the configuration file    
    config = parse_config()    
  
    # parse the fillers
    try:
        fillers_count, fillers = parse_fillers(fill_file = config['fillers'])
    except KeyError as e:
        print "There was no fillers file specified in config.txt. Please specify the fillers as \"fillers\"."
        sys.exit()
        
    # parse the items
    try:
        items_count, items = parse_stimuli(stim_file = config['stimuli'], no_conds = int(config['no_conds']))
    except KeyError as e:
        print "There was no stimuli file specified in config.txt. Please specify the fillers as \"stimuli\"."
        sys.exit()
        
    # parse the template for the experiment
    template = parse_template(tex_template = config['template'])
        
    # check to make sure everything's okay with the counts
    check_ratio(config['filler_ratio'], fillers_count, items_count)
    
    # begin to work on output files
    os.chdir("..")
    
    if not os.path.isdir(os.path.join(os.getcwd(), "outputs/")):
        os.makedirs(os.path.join(os.getcwd(), "outputs/"))
        
    os.chdir(os.path.join(os.getcwd(), "outputs/"))
    
    for curr_list in range(1, int(config['no_lists']) + 1):
        print "Creating List %i..." % curr_list
        
        if not os.path.isdir(os.path.join(os.getcwd(), "List-" + str(curr_list) + "/")):
            os.makedirs(os.path.join(os.getcwd(), "List-" + str(curr_list) + "/"))
            
        os.chdir(os.path.join(os.getcwd(), "List-" + str(curr_list) + "/"))
        
        # get the items to be used in this list
        this_list_items = get_list_items(items = items, list_no = curr_list, no_lists = int(config['no_lists']))
        
        # get all the items and fillers, randomized
        this_all_items = this_list_items + fillers
        random.shuffle(this_all_items)
        
        # actually write the items to the document
        list_order = write_likert_document(items = this_all_items, list_no = curr_list, exp_name = config['ex_name'], template = template)
        
        f_prefix = config['ex_name'] + "-List-" + str(curr_list)
        
        try:
            with open(f_prefix + "-Order.txt", 'w') as order_f:
                for item in list_order:
                    order_f.write(str(item) + "\n")
                order_f.close()
        except IOError as e:
            print "The output file for writing list order could not be opened. Please ensure permissions are correct."
        
        
        # compile the list
        print "Compiling TeX for List %i..." % curr_list
        
       # FNULL = open(os.devnull, 'w')
        for i in range(1,4):
            subprocess.call(["xelatex", f_prefix + ".tex"], shell = False)#, stdout = FNULL, stderr = subprocess.STDOUT)
        
        os.chdir("..")
        #end of main list loop
    
    print "Done."

if __name__ == '__main__':
    main()