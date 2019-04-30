#!/usr/local/bin/python3

## written by Atsushi Hori (ahori@riken.jp) at 
## Riken Center for Computational Science
## 2019 April

# Preparation
# python3
# and Python modules listed below

import copy
import os
import sys
import datetime
import math
import pandas as pd
from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.dates import date2num
import seaborn as sns

PREPROCESS = '' 	# if specified, then the csv file is preprocessed
DATE_FORMAT = '%Y/%m/%d' # YYmmDD
REGION_COUNTRY = True 	# if True, major countries will also appear
FILE_TYPE = 'pdf' 	# if specified, then graphs are saved in this format
EVENT_SHOW = False 	# if True, events are wshown in TimeSeries graph
CROSSTAB_THRESHOLD = 0.01 # crosstabe values less than this will be removed
CROSSTAB_NCOLS = 3
DEBUG = False

event_list = [ # [ year, month, day, event-name, text-height ]
    [ 2019, 2, 18, 'hpc-announce[1]', 120 ],
    [ 2019, 2, 21, 'Atsushi@Riken[1]', 140 ],
    [ 2019, 2, 26, 'Sanjay@UIUC', 160 ],
    [ 2019, 2, 26, 'Emmanuel@Inria', 180 ],
    [ 2019, 2, 22, 'Artem@Mellanox', 200 ],
    [ 2019, 2, 27, 'Atsushi@Riken[2]', 220 ],
    [ 2019, 3,  1, 'hpc-announce[2]', 110 ],
    [ 2019, 3, 19, 'hpc-announce[3]', 130 ],
    [ 2019, 4,  1, 'Rolf@HLRS', 150 ]
    ]

region_tab = { 'Argentina'		: 'CentralandSouthAmerica',
               'Australia' 		: 'Australia',
               'Austria' 		: 'Europe',
               'belgium' 		: 'Europe',
               'Belgium' 		: 'Europe',
               'Brazil' 		: 'CentralandSouthAmerica',
               'Canada' 		: 'NorthAmerica',
               'China' 			: 'China',
               'Croatia' 		: 'Europe',
               'Czech Republic' 	: 'Europe',
               'Denmark' 		: 'Europe',
               'Denmark, Austria' 	: 'Europe',
               'Egypt' 			: 'Africa',
               'Estonia'		: 'Europe',
               'Finland' 		: 'Europe',
               'France' 		: 'Europe',
               'Germany' 		: 'Europe',
               'Greece' 		: 'Europe',
               'India' 			: 'India',
               'Italy' 			: 'Europe',
               'Japan' 			: 'Japan',
               'Korea, South' 		: 'SouthKorea',
               'Luxembourg' 		: 'Europe',
               'Mexico' 		: 'CentralandSouthAmerica',
               'Netherlands' 		: 'Europe',
               'Norway'			: 'Europe',
               'Pakistan' 		: 'Asia',
               'Peru' 			: 'CentralandSouthAmerica',
               'Poland' 		: 'Europe',
               'Portugal' 		: 'Europe',
               'Russia' 		: 'Russia',
               'Saudi Arabia' 		: 'Asia',
               'Serbia' 		: 'Europe',
               'Singapore' 		: 'Asia',
               'Spain' 			: 'Europe',
               'Sweden' 		: 'Europe',
               'Switzerland' 		: 'Europe',
               'Tunisia' 		: 'Africa',
               'Ukraine' 		: 'Europe',
               'UAE'			: 'Asia',
               'UK' 			: 'Europe',
               'USA'	 		: 'USA' 
               }

question_tab = { 'Q1'  : 'Occupation',
                 'Q2'  : 'Country/Region',
                 'Q3'  : 'Programming Skill',
                 'Q4'  : 'MPI Skill',
                 'Q5'  : 'Programming Language',
                 'Q6'  : 'Programming Experience',
                 'Q7'  : 'MPI Experience',
                 'Q8'  : 'Working Fields',
                 'Q9'  : 'Role',
                 'Q10' : 'MPI Standard', 
                 'Q11' : 'Learning MPI',
                 'Q12' : 'MPI Book',
                 'Q13' : 'MPI Implementation',
                 'Q14' : 'Reasons to choose MPI',
                 'Q15' : 'How to check MPI Spec.',
                 'Q16' : 'MPI Difficulty', 
                 'Q17' : 'Known MPI Fetures',
                 'Q18' : 'MPI Aspects',
                 'Q19' : 'MPI thread level',
                 'Q20' : 'MPI Obstacles', 
                 'Q21' : 'Error Checking',
                 'Q22' : 'Packing MPI calls', 
                 'Q23' : 'MPI+X',
                 'Q24' : 'Room for tuning',
                 'Q25' : 'Alternatives',
                 'Q26' : 'Missing Fetures',
                 'Q27' : 'Missing Semantics',
                 'Q28' : 'Unnecessary Features',
                 'Q29' : 'Backward Compatibility',
                 'Q30' : 'Performance and Portability'
              }

graph_scale = {
    'Q1'  : 0.75,
    'Q3'  : 0.83,
    'Q4'  : 0.83,
    'Q5'  : 0.81,
    'Q6'  : 0.83,
    'Q7'  : 0.83,
    'Q8'  : 0.7,
    'Q9'  : 0.7,
    'Q10' : 0.83,
    'Q11' : 0.68,
    'Q12' : 0.6,
    'Q13' : 0.74,
    'Q14' : 0.74,
    'Q15' : 0.7,
    'Q16' : 0.67,
    'Q17' : 0.7,
    'Q18' : 0.7,
    'Q19' : 0.7,
    'Q20' : 0.64,
    'Q21' : 0.78,
    'Q22' : 0.7,
    'Q23' : 0.8,
    'Q24' : 0.58,
    'Q25' : 0.65,
    'Q26' : 0.64,
    'Q27' : 0.65,
    'Q28' : 0.62,
    'Q29' : 0.62,
    'Q30' : 0.75
}

qval_tab = \
{ 'Q1' :
      { 'College/University' : 'University',
        'Governmental institute' : 'Government',
        'Hardware vendor' : 'HW vendor',
        'Software vendor' : 'SW vendor',
        'Private research institute' : 'Private',
        'Other' : 'other' },
  'Q3' :
      { '1' : 'Low', 
        '2' : '2', 
        '3' : '3', 
        '4' : '4', 
        '5' : '5', 
        '6' : 'High' },
  'Q4' :
      { '1' : 'Low', 
        '2' : '2', 
        '3' : '3', 
        '4' : '4', 
        '5' : '5', 
        '6' : 'High' },
  'Q5' :
      { 'C/C++' : 'C/C++',
        'Fortran 90 or newer' : '>= F90',
        'Fortran (older one than Fortran 90)' : '< F90',
        'Python' : 'Python',
        'Java' : 'Java',
        'Other' : 'other' } ,
  'Q6' :
      { 'more than 10 years' : '>10',
        'between 5 and 10 years' : '5-10',
        'between 2 and 5 years' : '2-5',
        'less than 2 years' : '<2' },
  'Q7' :
      { 'more than 10 years' : '>10',
        'between 5 and 10 years' : '5-10',
        'between 2 and 5 years' : '2-5',
        'less than 2 years' : '<2' },
  'Q8' :
      { 'System software development (OS, runtime library, communication library, etc.)' : 'OS/Runtime',
        'Parallel language (incl. domain specific language)' : 'Parallel language',
        'Numerical application and/or library' : 'Numerical Lib.',
        'AI (Deep Learning)' : 'AI',
        'Image processing' : 'Image',
        'Big data' : 'Big data',
        'Workflow and/or In-situ' : 'Worlflow',
        'Visualization' : 'Visualization',
        'Tool development (performance tuning, debugging, etc.)' : 'Tool',
        'Other' : 'other' },
  'Q9' :
      { 'Research and development of application(s)' : 'R&D Apps',
        'Research and development on system software (OS and/or runtime library)' : 'R&D OS/Runtime',
        'Research and development software tool(s)' : 'R&D Tools',
        'Parallelization of sequential program(s)' : 'Parralelization',
        'Performance tuning of MPI program(s)' : 'MPI Tuning',
        'Debugging MPI programs' : 'Debugging',
        'Other' : 'other'
        },
  'Q10' :
      { 'I read all.' : 'All',
        'I read most of it.' : 'Mostly',
        'I read only the chapters of interest for my work.' : 'Partly',
        'I have not read it, but I plan to.' : 'Wish',
        'No, and I will not read it.' : 'No' },
  'Q11' :
      { 'I read the MPI standard document.' : 'Read MPI standard',
        'I read book(s).' : 'MPI Book(s)',
        'I had lecture(s) at school.' : 'School Lecture(s)',
        'Other lectures or tutorials (workplace, conference).' : 'Other lecture(s)',
        'I read articles found on Internet.' : 'Internet',
        'I have not learned MPI.' : 'Not learned',
        'Other' : 'other' },
  'Q12' :
      { 'Beginning MPI (An Introduction in C)' : 'Beginning MPI',
        'Parallel Programming with MPI' : 'Parallel Programming\nwith MPI',
        'Using MPI' : 'Using MPI',
        'Parallel Programming in C with MPI and OpenMP' : 'Parallel Programming\nin C with MPI and OpenMP',
        'MPI: The Complete Reference' : 'MPI: the complete\nReference',
        'I have never read any MPI books' : '(never read)',
        'Other' : 'other' },
  'Q13' :
      { 'MPICH' : 'MPICH',
        'Open MPI' : 'Open MPI',
        'MVAPICH' : 'MVAPICH',
        'Intel MPI' : 'Intel MPI',
        'Cray MPI' : 'Cray MPI',
        'IBM MPI (BG/Q, PE, Spectrum)' : 'IBM MPI',
        'HPE MPI' : 'HPE MPI',
        'Tianhe MPI' : 'Tianhe MPI',
        'Sunway MPI' : 'Sunway MPI',
        'Fujistu MPI' : 'Fujistu MPI',
        'NEC MPI' : 'NEC MPI',
        'MS MPI' : 'MS MPI',
        'MPC MPI' : 'MPC MPI',
        'I do not know' : 'I do not know',
        'Other' : 'other' },
  'Q14' :
      { 'I like to use it.' : 'I like',
        'I was said to use it.' : 'Said to use',
        'I could not have any choice (the one provided by a vendor).': 'No choice',
        'I am familiar with it.' : 'I am familiar',
        'I have no special reason.' : 'No reason' },
  'Q15' :
      { 'I read the MPI Standard document (web/book).' : 'MPI standard',
        'I read book(s) (except the MPI standard).' : 'Book',
        'I read online documents (such as man pages).' : 'Online docs',
        'I ask colleagues.' : 'Asking colleagues',
        'I search the Internet (Google / Stack Overflow).' : 'Internet',
        'I know almost all MPI routines.' : 'I know all',
        'Other' : 'other' },
  'Q16' :
      { 'Algorithm design' : 'Algorithm',
        'Debugging' : 'Debugging',
        'Domain decomposition' : 'Decomposition',
        'Finding appropriate MPI routines' : 'Finding MPI routines',
        'Implementation issue workaround' : 'Workaround',
        'Performance tuning' : 'Tuning',
        'Other' : 'other' },
  'Q17' :
      { 'Point-to-point communications' : 'Pt2Pt',
        'Collective communications' : 'Collectives',
        'Communicator operations (split, duplicate, and so on)' : 'Communicators',
        'MPI datatypes' : 'MPI datatypes',
        'One-sided communications' : 'One-sided',
        'Dynamic process creation' : 'Dynamic process',
        'Persistent communication' : 'Persistent',
        'MPI with OpenMP (or multithread)' : 'MPI with OpenMP',
        'PMPI interface' : 'PMPI',
        'Other' : 'other'
        },
  'Q18' :
      { 'Point-to-point communications' : 'Pt2Pt',
        'Collective communications' : 'Collectives',
        'Communicator operations (split, duplicate, and so on)' : 'Communicators',
        'MPI datatypes' : 'MPI datatypes',
        'One-sided communications' : 'One-sided',
        'Dynamic process creation' : 'Dynamic process',
        'Persistent communications' : 'Persistent',
        'MPI with OpenMP (or multithread)' : 'MPI with OpenMP',
        'PMPI interface' : 'PMPI',
        'Other' : 'other' },
  'Q19' :
      { 'MPI_THREAD_SINGLE' : 'SINGLE',
        'MPI_THREAD_FUNNELED' : 'FUNNELED',
        'MPI_THREAD_SERIALIZED' : 'SERIALIZED',
        'MPI_THREAD_MULTIPLE' : 'MULTIPLE',
        'I have never called MPI_INIT_THREAD' : 'Never used',
        'I do not know or I do not care.' : 'Do not know/care',
        'Other' : 'other' },
  'Q20' :
      { 'I have no obstacles.' : 'No obstacles',
        'Too many routines.' : 'Too many routines.',
        'No appropriate lecture / book / info.' : 'No appropriate lecture',
        'Too complicated and hard to understand.' : 'Too much complicated',
        'I have nobody to ask.' : 'I have nobody to ask.',
        'I do not like the API.' : 'I do not like the API.',
        'Other' : 'other' },
  'Q21' : 
  { 'I rely on the default ‘Errors abort’ error handling' : 'Default',
    'Always' : 'Always',
    'Mostly' : 'Mostly',
    'Sometimes' : 'Sometimes',
    'Never' : 'Never',
    'Other' : 'other' },
  'Q22' :
      { 'Yes, to minimize the changes of communication API.' : 'Yes',
        'Yes, but I have no special reason for doing that.' : 'Yes, but no reason',
        'No, my program is too small to do that.' : 'No, too small',
        'No, MPI calls are scattered in my programs.' : 'No, scattered',
        'Other' : 'other' },
  'Q23' :
      { 'OpenMP'  : 'OpenMP',
        'Pthread' : 'Pthread',
        'OpenACC' : 'OpenACC',
        'OpenCL'  : 'OpenCL',
        'CUDA'    : 'CUDA',
        'No'      : 'No',
        'Other'  : 'other' },
  'Q24' :
      { 'No, my MPI programs are well-tuned.' : 
        'Well-tuned',
        'I think there is room but I do not know how to tune it.' : 
        'No tknowing how to do',
        'Yes, I know there is room for tuning but I do not have enough resources to do that.' : 
        'No resource',
        'Yes, I know there is room for tuning but I should re-write large part of my program to do that.' : 
        'Rewrintg is hard',
        'I think there is room but I do not know how to tune it.' : 
        'Not knowing how to tune',
        'I have no chance to investigate.' : 
        'No chance to investigate',
        'I do not know how to find bottlenecks.' : 
        'Not knowing how to find',
        'I do not know if there is more to improve' : 
        'Not knowing how to improve',
        'Other' : 'other' },
  'Q25' :
      { 'A framework or library using MPI.' : 'Framework',
        'A PGAS language (UPC, Coarray Fortran, OpenSHMEM, XcalableMP, ...).' : 'PGAS',
        'A Domain Specific Language (DSL).' : 'DSL',
        'Low-level communication layer provided by vendor (Verbs, DCMF, ...).' : 'Low-level comm. layer',
        'I am not investigating any alternatives.' : 'No investigation',
        'Other' : 'other' },
  'Q26' :
      { 'Latency' : 'Latency',
        'Message injection rate' : 'Injection rate',
        'Bandwidth' : 'Bandwidth',
        'Additional optimization opportunities in terms of communication (topology awareness, locality, etc.)' : 'Additional comm. opt.',
        'Optimization opportunities except communication (architecture awareness, dynamic processing, accelerator support, etc.)' : 'Other optimization',
        'Multi-threading support' : 'Multi-threading\nsupport',
        'Asynchronous progress' : 'Asynchronous progress',
        'MPI provides all semantics I need' : 'Satisfied',
        'Other' : 'other' },
  'Q27' :
      { 'Latency hiding (including asynchronous completion)' : 'Latency hiding',
        'Endpoints (multi-thread, sessions)' : 'End-points',
        'Resilience (fault tolerance)' : 'Resilience',
        'Additional optimization opportunities in terms of communication (topology awareness, locality, etc.)' : 'Additional optimization',
        'Another API which is easier and/or simpler to use' : 'Another API',
        'MPI is providing all the communication semantics required by my application' : 'MPI provides all',
        'Other' : 'other' },
  'Q28' :
      { 'One-sided communication' : 'One-sided',
        'Datatypes' : 'Datatypes',
        'Communicator and group management' : 'Communicator',
        'Collective operations' : 'Collectives',
        'Process topologies' : 'Process topologies',
        'Dynamic process creation' : 'Dynamic process',
        'Error handlers' : 'Error handlers',
        'There are no unnecessary features' : 'No unnecessary features',
        'Other' : 'other' },
  'Q29' :
      { 'Yes, compatibility is very important for me.' : 'Very important',
        'API should be clearly versioned.' : 'Versioned API',
        'I prefer to have new API for better performance.' : 'New API for performance',
        'I prefer to have new API which is simpler and/or easier-to-use.' : 'New API for easier-to-use',
        'I do not know or I do not care.' : 'Do not know/care',
        'Other' : 'other'
        },
  'Q30' :
      { '1' : 'Portability',
        '2' : '2',
        '3' : '3',
        '4' : '4',
        '5' : 'Performance' },
}

multi_answer = [ 'Q5', 'Q8', 'Q9', 'Q11', 'Q12', 'Q13', 'Q15', 
                 'Q17', 'Q18', 'Q19', 'Q20', 'Q23', 'Q25', 
                 'Q27', 'Q28' ]

sort_answer = [ 'Q1', 'Q5', 'Q8', 'Q9', 'Q12', 'Q13', 'Q14', 'Q15', 
                'Q16', 'Q17', 'Q18', 'Q20', 'Q23', 'Q24', 'Q25', 'Q26', 
                'Q27', 'Q28', 'Q29' ]

print_other = [ 'Q5', 'Q8', 'Q9', 'Q11', 'Q12', 'Q13', 'Q15', 'Q18', 'Q20',
                'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28', 'Q29' ]

color_list =  [ "r", "g", "b", "c", "m", "y" ]

def conv_date ( q0_str ) :
    ymd = q0_str.split().pop(0)
    return datetime.datetime.strptime( ymd, DATE_FORMAT ).date()

def unique ( list ) :
    unique_list = []
    for elm in list :
        if elm not in unique_list :
            unique_list.append( elm )
    return unique_list


argv_idx = 1
argc = len( sys.argv )
if argc < 2 :
    print( 'Input CSV file must be specified' )
    exit( 1 )
if argc > 2 :
    if sys.argv[argv_idx] == 'debug' :
        argv_idx += 1
        DEBUG = True
    elif sys.argv[argv_idx] =='show' :
        FILE_TYPE = ''
        argv_idx += 1
csv_in = sys.argv[argv_idx]
if not os.path.isfile( csv_in ) :
    print( csv_in + ' not found' )
    exit( 1 )

argv_idx += 1
question0 = ''
question1 = ''
if argv_idx < argc :
    question0 = sys.argv[argv_idx]
    argv_idx += 1
    if argv_idx < argc :
        question1 = sys.argv[argv_idx]

if DEBUG :
    FILE_TYPE = ''
    EVENT_SHOW = True

if PREPROCESS != '' :
    tmpfile = csv_in + '.pre'
    os.system( PREPROCESS + ' "' + csv_in + '" > "' + tmpfile + '"' )
    df = pd.read_csv( tmpfile, sep=',' )
    os.remove( tmpfile )
else :
    df = pd.read_csv( csv_in, sep=',', dtype=str, keep_default_na=False )
basename = os.path.splitext( os.path.basename( csv_in ) )[0].replace(' ','')

# shorten long country names
df = df.replace( 'United Kingdom', 	'UK'  )
df = df.replace( 'United States', 	'USA' )
df = df.replace( 'belgium',		'Belgium' )
df = df.replace( 'United arab Emirates ', 'UAE' )
total_answers = len( df )

#print( df.dtypes )
#print( df.columns )
i = 0;
for column_name in df :
    q = 'Q' + str(i)
    i += 1
    df.rename(columns={column_name: q}, inplace=True)
num_columns = i + 1

countries = df[ 'Q2' ]
#print( countries )

err = False
# checking unknown cournties
for country in countries :
    region = region_tab[ country ]
    if region == None :
        err = True
        print( '????? Unknown Country: ' + country )
if err :
    exit( 1 )

# adding another Region column
region_list = []
rename_list = []
if REGION_COUNTRY == 'Region' :
    # adding Region column
    for country in countries :
        region = region_tab[ country ]
        region_list.append( region )
else :
    for country in countries :
        region = region_tab[ country ]
        if len( df[df['Q2']==country] ) > 30 and \
                region != country :
            region_tab.setdefault( region, country )
            region_list.append( region + ':' + country )
            rename_list.append( region )
        else :
            region_list.append( region )
df_whole = df.assign( Region = region_list )
for rename in unique( rename_list ) :
    df_whole.replace( rename, rename+':others', inplace=True )

regions = df_whole['Region']
region_list = regions.values.tolist()
#print( region_list )
unique_regions = unique(region_list)
#print( unique_regions )
#print( df_whole )

# creating region list having more than 30 answers
regions_major = []
for reg in unique_regions :
    df_reg = df_whole.query( 'Region=='+'"'+reg+'"' ) 
    if len( df_reg ) > 30 :
        regions_major.append( reg )
regions_major.sort()

whole = 'whole'
dict_qno    = {}
dict_others = {}
for qno in qval_tab.keys() :
    list_sum = []
    dict_tmp = {}
    list_others = []
    legend = qval_tab[qno]

# decompose answers if this is a multiple-answer question and
# convert to percent numbers on whole data 
    dict_ans = { 'other' : 0 }
    for ans in legend.values() :
        dict_ans.setdefault( str(ans), 0 )
    tmp = df_whole[qno]

#    print( tmp )
    if qno in multi_answer :
        for mans in tmp :
            list_ans = mans.split( ';' )
            for ans in list_ans :
                if ans in legend.keys() :
                    dict_ans[legend[ans]] += 1
                elif len( ans ) > 0 :
                    dict_ans['other'] += 1
                    list_others.append( ans )
    else :
        for ans in tmp :
            if ans in legend.keys() :
                dict_ans[legend[ans]] += 1
            elif len( ans ) > 0 :
                dict_ans['other'] += 1
                list_others.append( ans )
#    print( list_others )
    ser = pd.Series( data=dict_ans, dtype=float )
    sum = ser.sum()
    list_sum.append( sum )
    for i in range( ser.size ) :
        ser.iat[i] = ser.iat[i] / float(sum) * 100.0
    dfq = pd.DataFrame( { 'whole' : ser } )
#    print( 'whole', dfq )

# convert to percent numbers for each region
    for reg in regions_major :
        dict_ans = { 'other' : 0 }
        for ans in legend.values() :
            dict_ans.setdefault( str(ans), 0 )
        tmp = df_whole[df_whole['Region']==reg][qno]
#        print( tmp )
        if qno in multi_answer :
            for mans in tmp :
                list_ans = mans.split( ';' )
                for ans in list_ans :
                    if ans in legend.keys() :
                        dict_ans[legend[ans]] += 1
                    elif len( ans ) > 0 :
                        dict_ans['other'] += 1
                        list_others.append( ans )
        else :
            for ans in tmp :
                if ans in legend.keys() :
                    dict_ans[legend[ans]] += 1
                elif len( ans ) > 0 :
                    dict_ans['other'] += 1
                    list_others.append( ans )
        ser = pd.Series( data=dict_ans, dtype=float )
        sum = ser.sum()
        list_sum.append( sum )
        for i in range( ser.size ) :
            ser.iat[i] = ser.iat[i] / float(sum) * 100.0
        dfq[reg] = ser
    dfq.fillna( 0.0, inplace=True )

## rename index with short ones
#    legend = qval_tab[qno]
#    idxs = dfq.index
#    for idx_name in idxs :
#        if idx_name in legend.keys() :
#            dfq.rename( index={idx_name: legend[idx_name]}, inplace=True )

# remove all zero rows
    for idx in dfq.index :
        flag = True
        for clm in dfq.columns :
            if dfq.loc[ idx, clm ] > 0 :
                flag = False
        if flag :
            dfq.drop( idx, inplace=True )

# sort, if desired
    if qno in sort_answer :
        dfq = dfq.sort_values( 'whole', ascending=False )

# move 'other' to the last
    if 'other' in dfq.index :
        idx = dfq.index.tolist()
        idx.remove( 'other' )
        idx.append( 'other')
        dfq = dfq.loc[idx,:]
#    print( dfq )

# adding number of answer row
#    print( list_sum )
    dfq = dfq.append( pd.Series( data=list_sum, 
                                 index=[whole]+regions_major, 
                                 name='_NumAns_',
                                 dtype=int ) )
    
# print data
#    print( dfq )                # print data
# print others
    if qno in print_other :
        dict_others.setdefault( qno, list_others )

# finally append to the dict_qno
    dict_qno.setdefault( qno, dfq )

#print( dict_qno )

def graph_time_series( df, regions ) :
    # adding 'Date' column
    dt_list = []
    date_dict = {}
    for dt in df['Q0'] :
        dt_list.append( conv_date( dt ) )
    df = df.assign( Date=dt_list )
#    print( df )
##    dateF = conv_date( df['Q0'].iat[0] )
##    ondate = df[df['Date']==dateF]
#    print( unique( dt_list ) )
    for dt in unique( dt_list ) :
        ondate = df[df['Date']==dt]
        regc = ondate['Region'].value_counts( sort=False )
        date_dict.setdefault( dt, regc )
    dc = pd.DataFrame( date_dict ).T
    dc.fillna( 0.0, inplace=True )
    for i in range( 1, len(dc) ) :
        for j in range( 0, len(unique_regions) ) :
            dc.iat[i,j] += dc.iat[i-1,j]

# drop regions having less number of answers
    dc_etc = dc.assign( etc = dc[region_list.pop(0)] )
#    print( dc_etc )
    for i in range( 0, len(dc) ) :
        dc_etc['etc'].iat[i] = 0
    for reg in unique_regions :
        if dc_etc[reg].iat[-1] < 30 :
            for i in range( 0, len(dc) ) :
                dc_etc['etc'].iat[i] += dc_etc[reg].iat[i]
    for reg in unique_regions :
        if dc_etc[reg].iat[-1] < 30 :
            dc_etc = dc_etc.drop( [reg], axis=1 )
    
# now we can draw a time series graph
    fig = plt.figure()
    ax = fig.add_subplot(111)
    dc_etc.plot.area( ax=ax, stacked=True, legend='reverse', color=color_list )

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
    ax.tick_params(axis="x", which="major", labelsize=10)
    
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b"))
    ax.tick_params(axis="x", which="minor", labelsize=10, length=15, width=1)

    plt.subplots_adjust( right=0.68 )
    plt.legend( dc_etc, bbox_to_anchor=(1, 1) )

    if EVENT_SHOW :
        for event in event_list :
            year  = event.pop(0)
            month = event.pop(0)
            day   = event.pop(0)
            what  = event.pop(0)
            where = event.pop(0)
            x = date2num( datetime.date(year,month,day) )
            ax.annotate( what, 
                         xy=(x, 0), 
                         xycoords='data',
                         xytext=(0, where), 
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle="->")
                         )

    if FILE_TYPE == '' :
        plt.show()
    else :
        plt.savefig(basename+'-TimeSeries.'+FILE_TYPE, transparent=True)
    plt.close('all')
    return

def graph_percentage( dict, others, qno ) :
    df     = dict[qno]
    scale  = graph_scale[qno]
    legend = qval_tab[qno]

# adding numbers to the tiltle
    df_tmp = df[:-1]          # sub-DF excepting '_NumAns_'
    list_numans   = df.tail(1).values.tolist()[0]
    total_answers = list_numans[0]
#    print( total_answers, list_numans )
    for clm in dfq.columns :
        newc = clm + '\n(' + str( round( list_numans.pop(0)) ) + \
        ' / ' + str( round(total_answers) ) + ')'
        df_tmp.rename( columns={clm: newc}, inplace=True )

# print data 
    print( '\n**** ' + qno + ': ' + question_tab[qno] + ' ****')
    if qno in print_other :
        i = 0
        for ans in set( others[qno] ) :
            print( '[' + str(i) + '] ' + ans )
            i += 1
    print( '\n', df_tmp )       # print data

# eventually draw a graph (stacked bar in percentage)
    trans = df_tmp.T
    trans.plot( kind='bar', stacked=True, legend='reverse', color=color_list )
    plt.subplots_adjust( right=scale, bottom=0.3 )
    plt.legend( df_tmp.index, bbox_to_anchor=(1, 1) )
    plt.ylabel( 'Percentage' )
    if qno in multi_answer :
        plt.title( qno + '* : ' + question_tab[qno] )
    else :
        plt.title( qno + ' : ' + question_tab[qno] )
    plt.ylabel( 'Percentage' )
    if FILE_TYPE == '' :
        plt.show()
    else :
        plt.savefig(basename+'-'+qno+'.'+FILE_TYPE, transparent=True)
    return

### graph_time_series( df_whole, region_list )

if question0 != '' and question1 == '' :
    graph_percentage( dict_qno, dict_others, question0 )
elif question0 == '' and question1 == '' :
    graph_percentage( dict_qno, dict_others, 'Q1' )
    graph_percentage( dict_qno, dict_others, 'Q3' )
    graph_percentage( dict_qno, dict_others, 'Q4' )

    if not DEBUG :
        graph_percentage( dict_qno, dict_others, 'Q5' )
        graph_percentage( dict_qno, dict_others, 'Q6' )
        graph_percentage( dict_qno, dict_others, 'Q7' )
        graph_percentage( dict_qno, dict_others, 'Q8' )
        graph_percentage( dict_qno, dict_others, 'Q9' )
        graph_percentage( dict_qno, dict_others, 'Q10' )
        graph_percentage( dict_qno, dict_others, 'Q11' )
        graph_percentage( dict_qno, dict_others, 'Q12' )
        graph_percentage( dict_qno, dict_others, 'Q13' )
        graph_percentage( dict_qno, dict_others, 'Q14' )
        graph_percentage( dict_qno, dict_others, 'Q15' )
        graph_percentage( dict_qno, dict_others, 'Q16' )
        graph_percentage( dict_qno, dict_others, 'Q17' )
        graph_percentage( dict_qno, dict_others, 'Q18' )
        graph_percentage( dict_qno, dict_others, 'Q19' )
        graph_percentage( dict_qno, dict_others, 'Q20' )
        graph_percentage( dict_qno, dict_others, 'Q21' )
        graph_percentage( dict_qno, dict_others, 'Q22' )
        graph_percentage( dict_qno, dict_others, 'Q23' )
        graph_percentage( dict_qno, dict_others, 'Q24' )
        graph_percentage( dict_qno, dict_others, 'Q25' )
        graph_percentage( dict_qno, dict_others, 'Q26' )
        graph_percentage( dict_qno, dict_others, 'Q27' )
        graph_percentage( dict_qno, dict_others, 'Q28' )
        graph_percentage( dict_qno, dict_others, 'Q29' )
        graph_percentage( dict_qno, dict_others, 'Q30' )

def expand_multians( qno, df ) :
    list_expand = []
    for idx, row in df.iterrows():
        mans = row[qno]
        for ans in mans.split(';') :
            rec = copy.copy( row )
            if ans in qval_tab[qno] :
                rec[qno] = ans
            else :
                rec[qno] = 'Other'
            list_expand.append( rec )
    new_df = pd.DataFrame( list_expand, columns=df.columns )
    new_df.fillna( 0.0, inplace=True )
    return new_df

def cross_tab( qno0, qno1 ) :
    if qno0 in multi_answer and qno1 in multi_answer :
        print( 'Unable cross multiple answer quenstions' )
        return

    list_regions = [whole] + regions_major
    nregs        = len( list_regions )
    list_graphs  = []
    list_numasn  = []

    cross = df_whole.loc[:,[qno0,qno1]]
    # remove not-answered
    cross = cross[cross[qno0]!='']
    cross = cross[cross[qno1]!='']

    if qno0 in multi_answer :
        cross = expand_multians( qno0, cross )
    elif qno1 in multi_answer :
        cross = expand_multians( qno1, cross )
    ct = pd.crosstab( cross[qno0], cross[qno1], normalize=True, dropna=False )
    ct.fillna( 0.0, inplace=True )
#    print( '\nCT\n', ct )

    list_graphs.append( ct )
#    print( '\nwhole\n', ct )

    for reg in regions_major :
        df_reg = df_whole[df_whole['Region']==reg]
        cross = df_reg.loc[:,[qno0,qno1]]
        # remove not-answered
        cross = cross[cross[qno0]!='']
        cross = cross[cross[qno1]!='']

        if qno0 in multi_answer :
            cross = expand_multians( qno0, cross )
        elif qno1 in multi_answer :
            cross = expand_multians( qno1, cross )
#        print( '\nCROSS\n', cross )
        ct = pd.crosstab( cross[qno0], cross[qno1], 
                          normalize=True, dropna=False )
        ct.fillna( 0.0, inplace=True )
        list_regions.append( reg )
        list_graphs.append( ct )

    # make tick titles short
    # reorder index and columns
    new_graphs = []
    for dat in list_graphs :
        dat = dat.rename( mapper=qval_tab[qno0], axis='index' )
        dat = dat.rename( mapper=qval_tab[qno1], axis='columns' )
        dat.fillna( 0.0, inplace=True )
#        print( dat )
        dat = dat.reindex( index=qval_tab[qno0].values(), 
                           columns=qval_tab[qno1].values() )
        dat.fillna( 0.0, inplace=True )
#        print( dat )
        new_graphs.append( dat )

    # remove low-freq index 
    dat_whole = new_graphs[0]
    for idx in dat_whole.index :
        flag = True
        for dat in new_graphs :
            if not flag :
                break;
            for clm in dat_whole.columns :
                if clm in dat.columns and \
                   idx in dat.index   and \
                   dat.at[idx,clm] > 0.03 :
                    flag = False
                    break
        if flag :
            for dat in new_graphs :
                dat.drop( idx, axis=0, inplace=True )

    # remove low-freq columns
    for clm in dat_whole.columns :
        flag = True
        for dat in new_graphs :
            if not flag :
                break;
            for idx in dat_whole.index :
                if idx in dat.index   and \
                   clm in dat.columns and \
                   dat.at[idx,clm] > 0.03 :
                    flag = False
                    break
        if flag :
            for dat in new_graphs :
                dat.drop( clm, axis=1, inplace=True )

    ncols = CROSSTAB_NCOLS
    nrows = int( math.ceil( ( nregs + 2 ) / ncols ) )

    plt.figure( figsize=(ncols*2,nrows*2) )
    plt.rcParams["font.size"] = 8
    plt.tight_layout()
    i = 0
    for dat in new_graphs :
        print( '\nRegion:', list_regions[i], '\n', dat )
#        print( nregs, nrows, ncols, int(i/ncols), int(i%ncols) )
        ax = plt.subplot2grid( ( nrows, ncols ), 
                               ( int(i/ncols), int(i%ncols) ) )
        ax.set_title( list_regions[i] )
        sns.heatmap( dat, 
                     cmap='Greys', cbar=False, 
                     annot=False, #square=True, 
                     linewidths=0.5, linecolor='black', 
                     xticklabels=False, yticklabels=False,
#                     xticklabels=True, yticklabels=True,
                     ax=ax )
        ax.set_xlabel( '' )
        ax.set_ylabel( '' )
        i += 1

    i+= 1 # make space for tick titles
    ax = plt.subplot2grid( ( nrows, ncols ), 
                           ( int(i/ncols), int(i%ncols) ),
                           colspan=((nrows*ncols)-2) )

    # LEGEND
    legend = copy.copy( new_graphs[0] )
    print( '\nLEGEND\n', legend )
    nrows, ncols = legend.shape
#    print( 'nrows=', nrows, 'ncols=', ncols )
    for i in range( 0, nrows ) :
        for j in range( 0, ncols ) :
            legend.iat[i,j] = ( ( ( (j+1) % 2 ) + ( i % 2 ) ) % 2 ) * 0.5
#    ax.set_title( 'Legend' )
    ax.set_autoscale_on( True )

    sns.heatmap( legend, 
                 cmap='Greys', cbar=False, 
                 annot=False, square=True, 
                 linewidths=0.5, linecolor='black', 
                 xticklabels=True, yticklabels=True,
                 ax=ax )
    plt.subplots_adjust(hspace=0.4)

    if qno0 in multi_answer :
        ax.set_ylabel( qno0 + '*:' + question_tab[qno0] )
    else :
        ax.set_ylabel( qno0 + ':' + question_tab[qno0] )
    if qno1 in multi_answer :
        ax.set_xlabel( qno1 + '*:' + question_tab[qno1] )
    else :
        ax.set_xlabel( qno1 + ':' + question_tab[qno1] )

    len_max = 0
    for xlabel in dat.columns :
        if len( xlabel ) > len_max :
            len_max = len( xlabel )
    if len_max > 10 :
        for label in ax.get_xmajorticklabels() :
            label.set_rotation( 30 )
            label.set_horizontalalignment( "right" )
    
    if FILE_TYPE == '' :
        plt.show()
    else :
        plt.savefig(basename+'-'+qno0+'-'+qno1+'.'+FILE_TYPE, transparent=True)
    plt.close( 'all' )
    return

def summary () :
    ##print( '** Whole Data **' )
    ##print( df_whole )
    print( '\n\n** SUMMARY **' )
    cs = df_whole['Q2'].value_counts( sort=True )
    print( cs )
    print( '' ) # newline
    print( '# Countries:\t' + str( len(cs) ) )
    print( '# Answers:\t' + str(total_answers) )
    return


if question0 != '' and question1 != '' :
    cross_tab( question0, question1 )
elif question0 == '' and question1 == '' :
    qlist = [ 'Q1', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 
              'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 
              'Q17', 'Q18', 'Q19',
              'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 
              'Q27', 'Q28', 'Q29',
              'Q30' ]
    i = 0
    j = 0
    for q0 in qlist :
        i += 1
        for q1 in qlist[i:] :
            j += 1
            if DEBUG and j > 4 :
                summary()
                exit( 0 )
            cross_tab( q0, q1 )

####summary()

##if __name__ == '__main__':
##    main()

exit( 0 )

