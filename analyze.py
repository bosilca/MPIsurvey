#!/usr/bin/env python3

## written by Atsushi Hori (ahori@riken.jp) at 
## Riken Center for Computational Science
## 2019 April
## George Bosilca 2019

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
import unicodedata
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.dates import date2num
import seaborn as sns
import argparse

DATE_FORMAT_MS = '%m/%d/%y' # mmddyy
DATE_FORMAT_JP = '%Y/%m/%d' # YYmmdd
DATE_FORMAT_US = '%m/%d/%Y' # mmddYY
DATE_FORMATS = [ DATE_FORMAT_JP, DATE_FORMAT_US, DATE_FORMAT_MS ]

CROSSTAB_THRESHOLD = 0.04 # crosstab rows and columns less than this are not shown
CROSSTAB_NCOLS   = 3
CROSSTAB_CLEGEND = CROSSTAB_NCOLS
CROSSTAB_COLOR = 'YlOrRd'
# possible color map names
## Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu,
## BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens,
## Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn,
## PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r,
## PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd,
## PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r,
## RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2,
## Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn,
## YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot,
## afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg,
## brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm,
## coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r,
## gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat,
## gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r,
## gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2,
## gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, icefire,
## icefire_r, inferno, inferno_r, jet, jet_r, magma, magma_r, mako,
## mako_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r,
## plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, rocket,
## rocket_r, seismic, seismic_r, spring, spring_r, summer, summer_r,
## tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r,
## terrain, terrain_r, twilight, twilight_r, twilight_shifted,
## twilight_shifted_r, viridis, viridis_r, vlag, vlag_r, winter, winter_r  

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

region_tab = { 'Argentina'		: 'Central and South America',
               'Australia' 		: 'Australia',
               'Austria' 		: 'Europe',
               'belgium' 		: 'Europe',
               'Belgium' 		: 'Europe',
               'Brazil' 		: 'Central and South America',
               'Canada' 		: 'North America',
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
               'Korea, South' 		: 'South Korea',
               'Luxembourg' 		: 'Europe',
               'Mexico' 		: 'Central and South America',
               'Netherlands' 		: 'Europe',
               'Norway'			: 'Europe',
               'Pakistan' 		: 'Asia',
               'Peru' 			: 'Central and South America',
               'Poland' 		: 'Europe',
               'Portugal' 		: 'Europe',
               'Russia' 		: 'Russia',
               'Saudi Arabia' 		: 'Asia',
               'Serbia' 		: 'Europe',
               'Singapore' 		: 'Asia',
               'Spain' 			: 'Europe',
               'Sweden' 		: 'Europe',
               'Switzerland' 		: 'Europe',
               'Taiwan'			: 'China',
               'Tunisia' 		: 'Africa',
               'Ukraine' 		: 'Europe',
               'UAE'			: 'Asia',
               'UK' 			: 'Europe',
               'USA'	 		: 'USA' 
               }

question_tab = { 'Q1'  : 'Occupation',
                 'Q2'  : 'Programming Skill',
                 'Q3'  : 'MPI Skill',
                 'Q4'  : 'Programming Language',
                 'Q5'  : 'Programming Experience',
                 'Q6'  : 'MPI Experience',
                 'Q7'  : 'Working Fields',
                 'Q8'  : 'Role',
                 'Q9'  : 'MPI Standard', 
                 'Q10' : 'Learning MPI',
                 'Q11' : 'MPI Book',
                 'Q12' : 'MPI Implementation',
                 'Q13' : 'Choosing MPI',
                 'Q14' : 'Checking MPI Spec.',
                 'Q15' : 'MPI Difficulty', 
                 'Q16' : 'Unknown MPI Features',
                 'Q17' : 'MPI Aspects',
                 'Q18' : 'MPI thread level',
                 'Q19' : 'MPI Obstacles', 
                 'Q20' : 'Error Checking',
                 'Q21' : 'Packing MPI calls', 
                 'Q22' : 'MPI+X',
                 'Q23' : 'Room for tuning',
                 'Q24' : 'Alternatives',
                 'Q25' : 'Missing Features',
                 'Q26' : 'Missing Semantics',
                 'Q27' : 'Unnecessary Features',
                 'Q28' : 'Backward Compatibility',
                 'Q29' : 'Performance and Portability'
              }

graph_scale = {
    'Q1'  : 0.75,
    'Q2'  : 0.83,
    'Q3'  : 0.83,
    'Q4'  : 0.81,
    'Q5'  : 0.83,
    'Q6'  : 0.83,
    'Q7'  : 0.7,
    'Q8'  : 0.7,
    'Q9' : 0.83,
    'Q10' : 0.68,
    'Q11' : 0.6,
    'Q12' : 0.74,
    'Q13' : 0.74,
    'Q14' : 0.7,
    'Q15' : 0.67,
    'Q16' : 0.7,
    'Q17' : 0.7,
    'Q18' : 0.7,
    'Q19' : 0.64,
    'Q20' : 0.78,
    'Q21' : 0.7,
    'Q22' : 0.8,
    'Q23' : 0.58,
    'Q24' : 0.65,
    'Q25' : 0.64,
    'Q26' : 0.65,
    'Q27' : 0.62,
    'Q28' : 0.62,
    'Q29' : 0.75
}

qval_tab = \
{ 'Q1' :
      { 'College/University' : 'Univ',
        'Governmental institute' : 'Gov',
        'Hardware vendor' : 'HW',
        'Software vendor' : 'SW',
        'Private research institute' : 'Priv',
        'Other' : 'other' },
  'Q2' :
      { '1' : 'Low', 
        '2' : '2', 
        '3' : '3', 
        '4' : '4', 
        '5' : '5', 
        '6' : 'High' },
  'Q3' :
      { '1' : 'Low', 
        '2' : '2', 
        '3' : '3', 
        '4' : '4', 
        '5' : '5', 
        '6' : 'High' },
  'Q4' :
      { 'C/C++' : 'C(++)',
        'Fortran 90 or newer' : '>=F90',
        'Python' : 'Py',
        'Fortran (older one than Fortran 90)' : '<F90',
        'Java' : 'Java',
        'Other' : 'other' } ,
  'Q5' :
      { 'more than 10 years' : '>10',
        'between 5 and 10 years' : '5-10',
        'between 2 and 5 years' : '2-5',
        'less than 2 years' : '<2' },
  'Q6' :
      { 'more than 10 years' : '>10',
        'between 5 and 10 years' : '5-10',
        'between 2 and 5 years' : '2-5',
        'less than 2 years' : '<2' },
  'Q7' :
      { 'System software development (OS, runtime library, communication library, etc.)' : 'OS/R',
        'Parallel language (incl. domain specific language)' : 'Lang',
        'Numerical application and/or library' : 'Num-Lib.',
        'AI (Deep Learning)' : 'AI',
        'Image processing' : 'Image',
        'Big data' : 'Big data',
        'Workflow and/or In-situ' : 'Worlflow',
        'Visualization' : 'Vis.',
        'Tool development (performance tuning, debugging, etc.)' : 'Tool',
        'Other' : 'other' },
  'Q8' :
      { 'Research and development of application(s)' : 'Apps',
        'Research and development software tool(s)' : 'Tools',
        'Parallelization of sequential program(s)' : 'Parralelize',
        'Performance tuning of MPI program(s)' : 'Tuning',
        'Debugging MPI programs' : 'Debug',
        'Research and development on system software (OS and/or runtime library)' : 'OS/R',
        'Other' : 'other'
        },
  'Q9' :
      { 'I read all.' : 'All',
        'I read most of it.' : 'Mostly',
        'I read only the chapters of interest for my work.' : 'Partly',
        'I have not read it, but I plan to.' : 'Wish',
        'No, and I will not read it.' : 'No' },
  'Q10' :
      { 'I read the MPI standard document.' : 'Standard',
        'I had lecture(s) at school.' : 'School Lectures',
        'I read articles found on Internet.' : 'Internet',
        'I read book(s).' : 'Books',
        'Other lectures or tutorials (workplace, conference).' : 'Other',
        'I have not learned MPI.' : 'Never learned',
        'Other' : 'other' },
  'Q11' :
      { 'Beginning MPI (An Introduction in C)' : 'Beginning MPI',
        'Parallel Programming with MPI' : 'Parallel Programming',
        'Using MPI' : 'Using MPI',
        'Parallel Programming in C with MPI and OpenMP' : 'Parallel Programming in C',
        'MPI: The Complete Reference' : 'MPI: complete Ref',
        'I have never read any MPI books' : '(no book)',
        'Other' : 'other' },
  'Q12' :
      { 'MPICH' : 'MPICH',
        'Open MPI' : 'OMPI',
        'Intel MPI' : 'Intel',
        'MVAPICH' : 'MVA',
        'Cray MPI' : 'Cray',
        'IBM MPI (BG/Q, PE, Spectrum)' : 'IBM',
        'HPE MPI' : 'HPE',
        'Tianhe MPI' : 'Tianhe',
        'Sunway MPI' : 'Sunway',
        'Fujistu MPI' : 'Fujistu',
        'NEC MPI' : 'NEC',
        'MS MPI' : 'MS',
        'MPC MPI' : 'MPC',
        'I do not know' : 'No idea',
        'Other' : 'other' },
  'Q13' :
      { 'I like to use it.' : 'I like',
        'I was said to use it.' : 'Said to use',
        'I could not have any choice (the one provided by a vendor).': 'No choice',
        'I am familiar with it.' : 'Familiar',
        'I have no special reason.' : 'No reason' },
  'Q14' :
      { 'I read the MPI Standard document (web/book).' : 'MPI standard',
        'I read online documents (such as man pages).' : 'Online docs',
        'I search the Internet (Google / Stack Overflow).' : 'Internet',
        'I ask colleagues.' : 'Colleagues',
        'I read book(s) (except the MPI standard).' : 'Books',
        'I know almost all MPI routines.' : 'I know all',
        'Other' : 'other' },
  'Q15' :
      { 'Algorithm design' : 'Algorithm',
        'Debugging' : 'Debugging',
        'Domain decomposition' : 'Decomposition',
        'Finding appropriate MPI routines' : 'Finding MPI routines',
        'Implementation issue workaround' : 'Workaround',
        'Performance tuning' : 'Tuning',
        'Other' : 'other' },
  'Q16' :
      { 'Point-to-point communications' : 'Pt2Pt',
        'Collective communications' : 'Coll',
        'Communicator operations (split, duplicate, and so on)' : 'Comm Ops',
        'MPI datatypes' : 'Datatypes',
        'One-sided communications' : 'One-sided',
        'Dynamic process creation' : 'Dynamic process',
        'Persistent communication' : 'Persistent',
        'PMPI interface' : 'PMPI',
        'MPI with OpenMP (or multithread)' : 'w/ OMP',
        'Other' : 'other'
        },
  'Q17' :
      { 'Point-to-point communications' : 'Pt2Pt',
        'Collective communications' : 'Coll',
        'Communicator operations (split, duplicate, and so on)' : 'Comm Ops',
        'MPI datatypes' : 'Datatypes',
        'One-sided communications' : 'One-sided',
        'Dynamic process creation' : 'Dynamic process',
        'Persistent communications' : 'Persistent',
        'MPI with OpenMP (or multithread)' : 'w/ OMP',
        'PMPI interface' : 'PMPI',
        'Other' : 'other' },
  'Q18' :
      { 'MPI_THREAD_SINGLE' : 'SINGLE',
        'MPI_THREAD_FUNNELED' : 'FUNNELED',
        'MPI_THREAD_SERIALIZED' : 'SERIALIZED',
        'MPI_THREAD_MULTIPLE' : 'MULTIPLE',
        'I have never called MPI_INIT_THREAD' : 'never used',
        'I do not know or I do not care.' : 'do not know/care',
        'Other' : 'other' },
  'Q19' :
      { 'I have no obstacles.' : 'No obstacles',
        'Too many routines.' : 'Too many routines',
        'No appropriate lecture / book / info.' : 'No appropriate one',
        'Too complicated and hard to understand.' : 'Complicated',
        'I have nobody to ask.' : 'Nobody to ask',
        'I do not like the API.' : 'Dislike API',
        'Other' : 'other' },
  'Q20' : 
  { 'I rely on the default ‘Errors abort’ error handling' : 'Default',
    'Always' : 'Always',
    'Mostly' : 'Mostly',
    'Sometimes' : 'Sometimes',
    'Never' : 'Never',
    'Other' : 'other' },
  'Q21' :
      { 'Yes, to minimize the changes of communication API.' : 'Yes',
        'Yes, but I have no special reason for doing that.' : 'Yes, but no reason',
        'No, my program is too small to do that.' : 'No, too small',
        'No, MPI calls are scattered in my programs.' : 'No, scattered',
        'Other' : 'other' },
  'Q22' :
      { 'OpenMP'  : 'OMP',
        'Pthread' : 'Pthread',
        'OpenACC' : 'OACC',
        'OpenCL'  : 'OCL',
        'CUDA'    : 'CUDA',
        'No'      : 'No',
        'Other'  : 'other' },
  'Q23' :
      { 'No, my MPI programs are well-tuned.' : 
        'Well-tuned',
        'Yes, I know there is room for tuning but I should re-write large part of my program to do that.' :
        'Hard to rewrie',
        'Yes, I know there is room for tuning but I do not have enough resources to do that.' :
        'No resource',
        'I think there is room but I do not know how to tune it.' :
        'No idea to tune',
        'I do not have (know) tools to find performance bottlenecks.' :
        'Not having the tools',
        'I have no chance to investigate.' :
        'No chance to investigate',
        'I do not know how to find bottlenecks.' :
        'Not idea to find bottlenecks',
        'I do not know if there is room for performance tuning.' :
        'No idea to improve',
        'Other' : 'other' },
  'Q24' :
      { 'A framework or library using MPI.' : 'Framework',
        'A PGAS language (UPC, Coarray Fortran, OpenSHMEM, XcalableMP, ...).' : 'PGAS',
        'A Domain Specific Language (DSL).' : 'DSL',
        'Low-level communication layer provided by vendor (Verbs, DCMF, ...).' : 'LL comm',
        'I am not investigating any alternatives.' : 'No investigation',
        'Other' : 'other' },
  'Q25' :
      { 'Latency' : 'Latency',
        'Message injection rate' : 'Inj. rate',
        'Bandwidth' : 'Bandwidth',
        'Additional optimization opportunities in terms of communication (network topology awareness, etc.)' : 'Additional comm. opt.',
        'Optimization opportunities except communication (architecture awareness, dynamic processing, accelerator support, etc.)' : 'Other opt',
        'Multi-threading support' : 'Multi-thread',
        'Asynchronous progress' : 'Asynch progress',
        'MPI provides all semantics I need' : 'Satisfied',
        'Other' : 'other' },
  'Q26' :
      { 'Latency hiding (including asynchronous completion)' : 'Latency hiding',
        'Endpoints (multi-thread, sessions)' : 'End-points',
        'Resilience (fault tolerance)' : 'Resilience',
        'Additional optimization opportunities in terms of communication (topology awareness, locality, etc.)' : 'Additional opt',
        'Another API which is easier and/or simpler to use' : 'Another API',
        'MPI is providing all the communication semantics required by my application' : 'MPI provides all',
        'Other' : 'other' },
  'Q27' :
      { 'One-sided communication' : 'One-sided',
        'Datatypes' : 'Datatypes',
        'Communicator and group management' : 'Communicator',
        'Collective operations' : 'Collectives',
        'Process topologies' : 'Topologies',
        'Dynamic process creation' : 'Dynamic process',
        'Error handlers' : 'Error',
        'There are no unnecessary features' : 'No unnecessary feature',
        'Other' : 'other' },
  'Q28' :
      { 'Yes, compatibility is very important for me.' : 'Very important',
        'API should be clearly versioned.' : 'Versioned API',
        'I prefer to have new API for better performance.' : 'New API for performance',
        'I prefer to have new API which is simpler and/or easier-to-use.' : 'New API for easier-to-use',
        'I do not know or I do not care.' : 'Do not know/care',
        'Other' : 'other'
        },
  'Q29' :
      { '1' : 'Portability',
        '2' : '2',
        '3' : '3',
        '4' : '4',
        '5' : 'Performance' },
}

multi_answer = [ 'Q4', 'Q7', 'Q8', 'Q10', 'Q11', 'Q12', 'Q14', 
                 'Q16', 'Q17', 'Q18', 'Q19', 'Q22', 'Q24', 
                 'Q26', 'Q27' ]

sort_answer = [ 'Q1', 'Q4', 'Q7', 'Q8', 'Q11', 'Q12', 'Q13', 'Q14', 
                'Q15', 'Q16', 'Q17', 'Q19', 'Q22', 'Q23', 'Q24', 'Q25', 
                'Q26', 'Q27', 'Q28' ]

print_other = [ 'Q4', 'Q7', 'Q8', 'Q10', 'Q11', 'Q12', 'Q14', 'Q17', 'Q19',
                'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28' ]

color_list =  [ 'r', 'b', 'g', 'c', 'm', 'y', 'k' ]

country_abbrv = { 'Multi-Answer' :	'mans',
                  'overall' : 		'overall',
                  'Europe:France' : 	'FR', 
                  'Europe:Germany' : 	'GR',
                  'Europe:Italy' : 	'IT',
                  'Europe:UK' : 	'UK',
                  'Europe:others' : 	'eu',
                  'Japan' : 		'JP',
                  'Russia' : 		'RU',
                  'USA' : 		'US'
                  }

mpi_cat = { 'MPICH' : 'OSS',
            'Open MPI' : 'OSS',
            'MVAPICH' : 'OSS',
            'MPC MPI' : 'OSS',
            'Intel MPI' : 'Vendor',
            'Cray MPI' : 'Vendor',
            'IBM MPI (BG/Q, PE, Spectrum)' : 'Vendor',
            'HPE MPI' : 'Vendor',
            'Tianhe MPI' : 'OSS',
            'Sunway MPI' : 'Vendor',
            'Fujistu MPI' : 'Vendor',
            'NEC MPI' : 'Vendor',
            'MS MPI' : 'Vendor',
            'I do not know' : 'No idea',
            'Other' : 'other' },


first_question   = 'What is your main occupation?'
country_question = 'Select main country or region of your workplace in past 5 years. [among the countries in Top500 list as of Nov. 2018. If you cannot find your country or region, please specify.]'

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode('utf-8')
    return str(text)

def conv_date ( dt ) :
    #print( "conv_date:'", dt, "'" )
    for ds in dt.split() :
        for format in DATE_FORMATS :
            try :
                return datetime.datetime.strptime( ds, format ).date()
            except :
                continue
    print( 'Unknown date format:', ds )
    exit( 1 )

def unique ( list ) :
    """
    Return a list of unique elements of the original list in the order in which they first
    appear in the original list.

    :param list: The input list
    :return: the list of unique elements maintaining the original order
    """
    unique_list = []
    for elm in list :
        if elm not in unique_list :
            unique_list.append( elm )
    return unique_list

def tex_conv( str ) :
    s = copy.copy( str )
    s = s.replace( '#', '\\#' )
    s = s.replace( '_', '\\_' )
    s = s.replace( '&', '\\&' )
    s = s.replace( '^', '\\^' )
    s = s.replace( '<', '\\verb!<!' )
    s = s.replace( '>', '\\verb!>!' )
    return( s )

def get_long_ans_tex( qno, sans ) :
    for key, value in qval_tab[qno].items():
        if value == sans :
            if len( key ) > 45 :
                key = '{\small ' + key[:40] + '$\\cdots$}'
            elif len( key ) > 40 :
                key = '{\small ' + key + '}'
            return( key )
    return( '' )


qlist = [ 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9',
          'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19',
          'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28', 'Q29'
          ]

qlist_all = qlist + [ 'all' ]

file_formats = [ 'eps', 'pdf', 'png' ]

parser = argparse.ArgumentParser( description="Survey Analysis" )
parser.add_argument( '-t', '--timeseries',
                     action='store_true',
                     help='Draw time series graph' )
parser.add_argument( '-e', '--event',
                     action='store_true',
                     help='Show events in the time series graph' )
parser.add_argument( '-s', '--simple',
                     nargs='?',
                     action='append',
                     choices=qlist_all,
                     help="Question (Qn) to output graph(s) for particular questions. " \
                         "Or, 'all' graphs of all questions" )
parser.add_argument( '-c', '--cross', 
                     nargs='?',
                     action='append',
                     help="A pair of questions (Qn,Qm) " \
                         "to output cross-tab graph(s). " \
                         "Or, 'all' to draw graphs of all possible" \
                         "combinations." )
parser.add_argument( '-m', '--major_region', type=int, default=50,
                     help="Threshold to be a major region (50)" )
parser.add_argument( '-f', '--format', type=str, default='',
                     choices=file_formats,
                     help="File format. Default is 'pdf'" )
parser.add_argument( '-o', '--outdir', type=str, default='',
                     help="Prepend to all generated graph files" )
#parser.add_argument( '--dry-run', action='store_true', default=False,
# AH: I have no idea what to do with dry-run
#                     help="Don't execute any outside visible " \
#                        "actions (such as generating pdfs)." )
#parser.add_argument( '-D', '--log', dest='DEBUG', action='store_true', 
#                     default=False,
#                     help="Log all steps of the operations (verbose)." )
# We automatically open the files in read mode, 
# so if they dont exists an exception
# will be raised by the parsec. Protect if necessary.
parser.add_argument( '-x', '--tex', action='store_true', help='Output TeX' )
parser.add_argument( '-O', '--tex-outdir', type=str, default='',
                     help="Prepend to all generated TeX files" )
parser.add_argument( '-V', '--csvout', type=str, default='', 
                     help="Output CSV files used to draw all graphs" )
parser.add_argument( '-D', '--DEBUG', action='store_true', help='for debug' )
parser.add_argument( 'csv_in', 
                     nargs=argparse.REMAINDER, 
                     type=argparse.FileType('r'),
                     help='CSV file name containing the survey data ' +
                        "(Google Form or Microsoft Forms). " +
			"Multiple files can be provided." )

def normalize_df( df ) :
    if 'ID' in df.columns :
        del df['ID']
    if 'Start time' in df.columns :
        del df['Start time']
    if 'Completion time' in df.columns :
        df = df.rename(columns={'Completion time':'Timestamp'})
    if 'Email' in df.columns :
        del df['Email']
    if 'Name' in df.columns :
        del df['Name']
    return df

args = parser.parse_args()

flag_timeseries = False
flag_show_event = False
if args.timeseries :
    flag_timeseries = True
if args.event :
    flag_show_event = True

list_simple = []
if args.simple is not None :
    if 'all' in args.simple :
        list_simple = qlist
    else :
        list_simple = args.simple

list_cross = []
if args.cross is not None :
    if 'all' in args.cross :
        i = 0
        for q0 in qlist :
            i += 1
            for q1 in qlist[i:] :
                if q0 in multi_answer and q1 in multi_answer :
                    # we cannot cross-tab on multi-answer questions 
                    continue
                list_cross.append( [q0,q1] )
    else  :
        for item in args.cross :
            pair = item.split( ',' )
            if len( pair ) != 2 :
#                print( 'ERR0' )
                parser.print_help()
                exit( 1 )
            elif pair[0] == pair[1] :
#                print( 'ERR1' )
                parser.print_help()
                exit( 1 )
            elif pair[0] == 'all' and pair[1] in qlist :
                q1 = pair[1]
                for q0 in qlist :
                    if q0 == q1 :
                        continue;
                    if q0 in multi_answer and q1 in multi_answer :
                        # we cannot cross-tab on multi-answer questions 
                        continue
                    list_cross.append( [q0,q1] )
            elif pair[1] == 'all' and pair[0] in qlist :
                q0 = pair[0]
                for q1 in qlist :
                    if q0 == q1 :
                        continue;
                    if q0 in multi_answer and q1 in multi_answer :
                        # we cannot cross-tab on multi-answer questions 
                        continue
                    list_cross.append( [q0,q1] )
            elif pair[0] not in qlist and pair[1] not in qlist :
#                print( 'ERR2' )
                parser.print_help()
                exit( 1 )
            else :
                list_cross.append( pair )

major_region = args.major_region

if args.csv_in is None :
    print( 'At least one input CSV file must be specified' )
    exit( 1 )
csv_in = args.csv_in

DEBUG = False
if args.DEBUG :
    DEBUG = True
    FILE_TYPE = ''
    flag_timeseries = True
    flag_show_event = True
    list_simple = [ 'Q1', 'Q2', 'Q11' ]
    list_cross  = [ ['Q2','Q3'], ['Q3','Q4'], ['Q27','Q29'] ]

flag_tex = args.tex
tex_outdir = args.tex_outdir + '/'
csv_outdir = args.csvout + '/'

if not flag_timeseries and  not flag_tex and \
        list_simple == [] and list_cross  == [] :
    flag_timeseries = True
    list_simple = qlist
    i = 0
    j = 0
    flag_break = False
    for q0 in qlist :
        if flag_break :
            break
        i += 1
        for q1 in qlist[i:] :
            if q0 in multi_answer and q1 in multi_answer :
                break;
            j += 1
            if DEBUG and j > 4 :
                flag_break = True
                break

csv_in = args.csv_in.pop(0)
df = pd.read_csv( csv_in, sep=',', dtype=str, keep_default_na=False )
df = normalize_df( df )

dirname = ''
format = args.format
if args.outdir != '' :
    dirname = args.outdir + '/'

if args.csv_in is not [] :
    for csv_in in args.csv_in :
        dfn = pd.read_csv( csv_in, sep=',', dtype=str, keep_default_na=False )
        dfn = normalize_df( dfn )
        df = pd.concat( [df, dfn], sort=False )
        df = df.reset_index(drop=True)

# shorten long (and wrong?) country names
df.replace( [ 'United Kingdom', 
              'United States', 
              'belgium', 
              'United arab Emirates ' ], # he/she put a space at the end
            [ 'UK',
              'USA',
              'Belgium',
              'UAE' ],
            inplace=True )
dict_orgq = {}
for i in range(1,10) :
#    print( df.columns[i] )
    if df.columns[i] == first_question :
        break;

#print( df.columns[i:] )
j = 1;
for column_name in df.columns[i:] :
    q = 'Q' + str(j)
    if( column_name == country_question ) :
        df.rename( columns={column_name: 'country'}, inplace=True )
    else :
        dict_orgq.setdefault( q, column_name )
        df.rename( columns={column_name: q}, inplace=True )
        j += 1

for column_name in df :
#    print( column_name )
    countries = df[ 'country' ]
    err = False
    # checking for unknown countries and remove accents from all countries name
    for country in countries :
        stripped = strip_accents(country)
        if stripped != country :
            print( "Convert %s to %s" % (country, stripped) )
            df.replace( country, stripped, inplace=True )
            country = stripped

        region = region_tab[ stripped ]
        if None == region :
            print( '????? Unknown Country: ' + stripped )
            exit( 1 )

# As we modified tha panda table to remove accents 
# we need to update the list of countries
countries = df[ 'country' ]

# adding another Region column
region_list = []
rename_list = []
if major_region <= 1 :
    for country in countries :
        region = region_tab[ country ]
        region_list.append( region )
else :
    for country in countries :
        region = region_tab[ country ]
        if len( df[df['country'] == country] ) >= major_region and \
                region != country :
            region_list.append( region + ':' + country )
            rename_list.append( region )
        else :
            region_list.append( region )
# adding Region column
df_whole = df.assign( Region = region_list )
if rename_list != [] :
    for rename in unique( rename_list ) :
        df_whole.replace( rename, rename+':others', inplace=True )

regions = df_whole['Region']
region_list = regions.values.tolist()
#print( 'Region_list:', region_list[:3] )
unique_regions = unique(region_list)
#print( 'Unique_regions:', unique_regions )

# creating region list having more than 'major_region' threshold
regions_major = []
for reg in unique_regions :
    df_reg = df_whole.query( 'Region=='+'"'+reg+'"' ) 
    if len( df_reg ) >= major_region :
        regions_major.append( reg )
regions_major.sort()
#print( regions_major )

regions_minor = []
for reg in unique_regions :
    if reg not in regions_major :
        regions_minor.append( reg )

whole = 'overall'
dict_qno    = {}
dict_others = {}
for qno in qval_tab.keys() :
    list_sum = []
    dict_tmp = {}
    legend = qval_tab[qno]

# decompose answers if this is a multiple-answer question and
# convert to percent numbers on whole data 
    dict_ans = { 'other' : 0 }
    for ans in legend.values() :
        dict_ans.setdefault( str(ans), 0 )
    tmp = df_whole[qno]

#    print( 'tmp\n', tmp )
    if qno in multi_answer :
        for mans in tmp :
            list_ans = mans.split( ';' )
            for ans in list_ans :
                if ans in legend.keys() :
                    dict_ans[legend[ans]] += 1
                elif len( ans ) > 0 :
                    dict_ans['other'] += 1
    else :
        for ans in tmp :
            if isinstance( ans, str ) :
                if ans in legend.keys() :
                    dict_ans[legend[ans]] += 1
                elif len( ans ) > 0 :
                    dict_ans['other'] += 1

#    print( 'dict_ans\n', dict_ans )
    ser = pd.Series( data=dict_ans, dtype=float )
    sum = ser.sum()
    list_sum.append( sum )
    for i in range( ser.size ) :
        ser.iat[i] = ser.iat[i] / float(sum) * 100.0
    dfq = pd.DataFrame( { whole : ser } )

    if flag_tex :
        tex_list = []
        tex_list.append( '\\begin{table}[htb]%\n' )
        tex_list.append( '\\begin{center}%\n' )
        tex_list.append( '\\caption{' + qno + ': ' + dict_orgq[qno] + '}%\n' )
        tex_list.append( '\\label{tab:' + qno + '-ans}%\n' )
        tex_list.append( '\\begin{tabular}{l|l|r}%\n' )
        tex_list.append( '\\hline%\n' )
        tex_list.append( 'Choice & Abbrv. & \# Answers \\\\%\n' )
        tex_list.append( '\\hline%\n' )
        sum = 0
        for k, v in dict_ans.items() :
            sum = sum + v
        flag_other = False
        if qno in sort_answer :
            for k, v in sorted( dict_ans.items(), key=lambda x: -x[1] ) :
                if k == 'other' :
                    flag_other = True
                    continue
                valstr = str( v )
                skeystr = tex_conv( k )
                lkeystr = tex_conv( get_long_ans_tex( qno, k ) )
                percent = str( round( ((v*100*100)/sum)/100, 1 ) )
                tex_list.append( lkeystr + ' & ' + skeystr + ' & ' + \
                                     valstr + ' (' + percent + '\%)' + \
                                     ' \\\\%\n')
        else :
            for k, v in dict_ans.items() :
                if k == 'other' :
                    flag_other = True
                    continue
                valstr = str( v )
                skeystr = tex_conv( k )
                lkeystr = tex_conv( get_long_ans_tex( qno, k ) )
                percent = str( round( ((v*100*100)/sum)/100, 1 ) )
                tex_list.append( lkeystr + ' & ' + skeystr + ' & ' + \
                                     valstr + ' (' + percent + '\%)' + \
                                     ' \\\\%\n')
        if flag_other :
            key = 'other'
            if dict_ans[key] > 0 :
                v = dict_ans[key]
                valstr = str( v )
                percent = str( round( ((v*100*100)/sum)/100, 1 ) )
                tex_list.append( key + ' & - & ' + valstr + \
                                     ' (' + percent + '\%)' + \
                                     ' \\\\%\n')
        tex_list.append( '\\hline%\n' )
        tex_list.append( '\multicolumn{2}{c}{total} & ' + str( sum ) + \
                             ' \\\\%\n' )
        tex_list.append( '\\hline%\n' )
        tex_list.append( '\\end{tabular}%\n' )
        tex_list.append( '\\end{center}%\n' )
        tex_list.append( '\\end{table}%\n' )
        with open( tex_outdir + qno + '-ans.tex', mode='w' ) as f :
            f.writelines( tex_list )

# convert to percent numbers for each region
    list_others = []
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
                        list_others.append( reg + ': ' + ans )
        else :
            for ans in tmp :
                if ans in legend.keys() :
                    dict_ans[legend[ans]] += 1
                elif len( ans ) > 0 :
                    dict_ans['other'] += 1
                    list_others.append( reg + ': ' + ans )
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
        dfq = dfq.sort_values( whole, ascending=False )

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
        dict_others.setdefault( qno, sorted( list_others ) )
    if flag_tex :
        if len( list_others ) == 0 :
            tex_list = [ '\item (no other answer)\n' ]
        else :
            tex_list = []
            for ans in sorted( list_others ) :
                texstr = tex_conv( ans )
                tex_list.append( '\item ' + texstr + '\n' )
        with open( tex_outdir + qno + '-other.tex', mode='w' ) as f :
            f.writelines( tex_list )

# finally append to the dict_qno
    dict_qno.setdefault( qno, dfq )

#print( dict_qno )

def graph_time_series( df ) :
    # adding 'Date' column
    dt_list = []
    date_dict = {}

    for dt in df['Timestamp'] :
        dt_list.append( conv_date( dt ) )

    df = df.assign( Date=dt_list )
    for dt in unique( dt_list ) :
        ondate = df[df['Date']==dt]
        regc = ondate['Region'].value_counts( sort=False )
        date_dict.setdefault( dt, regc )
    dc = pd.DataFrame( date_dict ).T
    dc.fillna( 0.0, inplace=True )
    dc = dc.sort_index( axis=0, ascending=True )
#    print( 'DC:\n', dc )
    # accumulate
    for i in range( 1, len(dc) ) :
        for j in range( 0, len(unique_regions) ) :
            dc.iat[i,j] += dc.iat[i-1,j]

# drop regions having less number of answers
    dc_etc = dc.assign( etc = dc[region_list[0]] )
    for i in range( 0, len(dc) ) :
        dc_etc['etc'].iat[i] = 0
    for reg in unique_regions :
        if dc_etc[reg].iat[-1] < major_region :
            for i in range( 0, len(dc) ) :
                dc_etc['etc'].iat[i] += dc_etc[reg].iat[i]
            dc_etc = dc_etc.drop( [reg], axis=1 )
#    print( 'dc_etc\n', dc_etc )
    
# now we can draw a time series graph
    fig = plt.figure( num=1, figsize=(8,6) )
    ax = fig.add_subplot( 1, 1, 1 )
#    dc_etc.plot.area( ax=ax, stacked=True, legend='reverse',
#    color=color_list )
    dc_etc.plot.area( ax=ax, stacked=True, legend='reverse', color=color_list )

    if csv_outdir != '' :
        dc_etc.to_csv( csv_outdir + 'timeline.csv' )

    ax.xaxis.set_major_locator( mdates.DayLocator(interval=10) )
    ax.xaxis.set_major_formatter( mdates.DateFormatter("%d") )
    ax.tick_params( axis="x", which="major", labelsize=11 )
    
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b"))
    ax.tick_params( axis="x", which="minor", labelsize=10, length=15, width=1 )

    ax.set_xlabel( "Date", size = 11 )
    ax.set_ylabel( "# Answers", size = 11 )

    #plt.subplots_adjust( right=0.68 )
    plt.legend( loc="upper left" )

    if flag_show_event :
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

    if format == '' and not flag_tex :
        plt.show()
    else :
        fn = dirname + 'TimeSeries.' + format
        print( '\nFilename:', fn )
        if flag_tex :
            plt.savefig( fn, transparent=False )
        else :
            plt.savefig( fn, transparent=True )
    plt.close( 'all' )
    return

def simple_analysis( dict, others, qno ) :
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
        for ans in others[qno] :
            print( '[' + str(i) + '] ' + ans )
            i += 1
    print( '\n', df_tmp )       # print data

# eventually draw a graph (stacked bar in percentage)
    trans = df_tmp.T
    fig = plt.figure( num=1, figsize=(8,6) )
#    fig = plt.figure()
    ax = fig.add_subplot( 1, 1, 1 )
#    ax.plot( trans, kind='bar', stacked=True, legend='reverse',
#    color=color_list )

    if csv_outdir != '' :
        trans.to_csv( csv_outdir + qno + '-simple.csv' )

    trans.plot( ax=ax, kind='bar', stacked=True, \
                    legend='reverse', color=color_list )
    plt.subplots_adjust( right=scale, bottom=0.3 )
    plt.legend( df_tmp.index, bbox_to_anchor=(1,1) )
    plt.ylabel( 'Percentage' )
    if qno in multi_answer :
        plt.title( qno + '* : ' + question_tab[qno] )
    else :
        plt.title( qno + ' : ' + question_tab[qno] )
    if format == '' and not flag_tex :
        plt.show()
    else :
        fn = dirname + qno + '.' + format
        print( '\nFilename:', fn )
        if flag_tex :
            plt.savefig( fn, transparent=False )
        else :
            plt.savefig( fn, transparent=True )
    plt.close( 'all' )
    return

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

def table_and_graph_multi_ans( qno ) :
    world = df_whole[qno].value_counts( sort=True ).sort_values( ascending=False )
    dict_idx = {}
    for ma in world.index :
        ma_str = ''
        if ma not in dict_idx :
            for sa in ma.split(';') :
                if sa in qval_tab[qno] :
                    if ma_str == '' :
                        ma_str = qval_tab[qno][sa]
                    else :
                        ma_str += ', ' + qval_tab[qno][sa]
        if ma_str != '' :
            dict_idx.setdefault( ma, ma_str )
        elif ma not in qval_tab[qno] :
            world = world.drop( ma, axis='index' )
    world = world.rename( index=dict_idx )
    world = world.groupby( level=0 ).sum().sort_values( ascending=False )
    #print( world )

    df = pd.DataFrame( {whole:world} )
    #print( df )
    for reg in regions_major:
        tmp = df_whole[df_whole['Region']==reg][qno].value_counts( sort=True )
        for ma in tmp.index :
            ma_str = ''
            for sa in ma.split(';') :
                if sa in qval_tab[qno] :
                    if ma_str == '' :
                        ma_str = qval_tab[qno][sa]
                    else :
                        ma_str += ', ' + qval_tab[qno][sa]
            if ma_str == '' and ma not in qval_tab[qno] :
                tmp = tmp.drop( ma, axis='index' )
        tmp.rename( index=dict_idx, inplace=True )
        tmp = tmp.groupby( level=0 ).sum()
        tmp.name = reg
        df = pd.concat( [df,tmp], axis='columns', sort=False )
        #print( tmp )
        #print( df )
        #print()
    #print( df )

    df = df.groupby( level=0 ).sum().astype(np.int64)
    df.rename( columns=country_abbrv, inplace=True )
    df.sort_values( whole, ascending=False, inplace=True )
    #print( df )

    if flag_tex :
	## output TeX table
        cpos = 'r'
        for c in df.columns :
            cpos += '|c'

        thead = 'Multi-Answer'
        for clm in df.columns :
            thead += ' & ' +  tex_conv(clm)
        thead += ' \\\\\n'
        thead += ' \\hline%\n'

        clms = df.columns.tolist() + ['others']
        clms.pop()
        headsum = '(total)'
        for clm in clms :
            headsum += ' & ' + str( df[clm].sum() )
        headsum += ' \\\\%\n'

        csz = ''
        tex_list = []
        tex_list.append( '\\clearpage%\n' )
        tex_list.append( '{\\footnotesize\\begin{landscape}%\n' )
        tex_list.append( '\\begin{longtable}[htb]{' + cpos + '}%\n' )
        tex_list.append( '\\caption{' + qno + ': ' + dict_orgq[qno] + '}%\n' )
        tex_list.append( '\\label{tab:' + qno + '-mans} \\\\%\n' )
        # begin first head
        tex_list.append( '\\hline%\n' )
        tex_list.append( thead )
        tex_list.append( '\\endfirsthead%\n' )
        # begin head
        tex_list.append( '\\multicolumn{' + str(len(df.columns)+1) )
        tex_list.append( '}{r}{(continued from the previous page)}\\\\%\n' )
        tex_list.append( '\\hline%\n' )
        tex_list.append( thead )
        tex_list.append( '\\endhead%\n' )
        # end foot
        tex_list.append( '\\hline%\n' )
        tex_list.append( headsum );
        tex_list.append( '\\hline%\n' )
        tex_list.append( '\\multicolumn{' + str(len(df.columns)+1) )
        tex_list.append( '}{r}{(continue to the next page)}\\\\%\n' )
        tex_list.append( '\\endfoot%\n' )
        # end last foot
        tex_list.append( '\\hline%\n' )
        tex_list.append( headsum );
        tex_list.append( '\\hline%\n' )
        tex_list.append( '\\endlastfoot%\n' )
        # begin of table body
        tex_list.append( '\\hline%\n' )
        i = 0;
        for idx in df.index :
            tex_list.append( '{' + csz + tex_conv(idx) + '}' )
            j = 0;
            for clm in df.columns :
                tex_list.append( ' & ' + str(df.iat[i,j]) )
                j += 1
            tex_list.append( ' \\\\%\n' )
            i += 1
        tex_list.append( '\\hline%\n' )
        tex_list.append( '\\end{longtable}%\n' )
        tex_list.append( '\\end{landscape}}%\n' )
        tex_list.append( '\\clearpage%\n' )
        with open( tex_outdir + qno + '-mans.tex', mode='w' ) as f :
            f.writelines( tex_list )

# adding numbers to the tiltle
    gtotal = df['overall'].sum()
    dict_rename = {}
    for clm in df.columns :
        total = df[clm].sum()
        newc = clm + '\n(' + str( round(total) ) + \
        ' / ' + str( round(gtotal) ) + ')'
        dict_rename.setdefault( clm, newc )

    # convert to percent
    for clm in df.columns :
        df[clm] = df[clm] / df[clm].sum() * 100.0
    toosmall = []
    etc      = 0.0
    etclist  = []
    for idx in df.index :
        #print( idx )
        mans = df.at[ idx, 'overall' ]
        if mans < 3.0 :
            etc += mans
            toosmall.append( idx )
    etclist.append( etc )
    #print( toosmall )
    for reg in df.columns :
        etc  = 0.0
        if reg == 'overall' :
            continue
        others = 0.0
        for idx in df.index :
            if idx in toosmall :
                etc += df.at[ idx, reg ]
        etclist.append( etc )
    df_tmp = df.drop( toosmall )
    #print( df_tmp )
    #print( etclist )
    df_tmp.loc['etc.'] = etclist

    df_tmp.rename( columns=dict_rename, inplace=True )

    trans = df_tmp.T

    if csv_outdir != '' :
        trans.to_csv( csv_outdir + qno + '-mans.csv' )

    fig = plt.figure( num=1, figsize=(8,6) )
    ax = fig.add_subplot( 1, 1, 1 )
    trans.plot( ax=ax, kind='bar', stacked=True, \
                    legend='reverse', color=color_list )
    plt.subplots_adjust( right=0.5, bottom=0.3 )
    plt.legend( df_tmp.index, bbox_to_anchor=(1,1) )
    plt.ylabel( 'Percentage' )

    if format == '' and not flag_tex :
        plt.show()
    else :
        fn = dirname + qno + '-mans.' + format
        #print( '\nFilename:', fn )
        if flag_tex :
            plt.savefig( fn, transparent=False )
        else :
            plt.savefig( fn, transparent=True )
    plt.close( 'all' )
    return

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
        dat = dat.reindex( index=qval_tab[qno0].values(), 
                           columns=qval_tab[qno1].values() )
        dat.fillna( 0.0, inplace=True )
        new_graphs.append( dat )

    # remove low-freq index
    dat_whole = new_graphs[0]
    for idx in dat_whole.index :
        flag = True
        for dat in new_graphs :
            if not flag :
                break
            for clm in dat.columns :
                if dat.at[idx,clm] > CROSSTAB_THRESHOLD :
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
                break
            for idx in dat.index :
                if dat.at[idx,clm] > CROSSTAB_THRESHOLD :
                    flag = False
                    break
        if flag :
            for dat in new_graphs :
                dat.drop( clm, axis=1, inplace=True )

    # find max in all data to have the same scale in heatmaps
    max = 0.0
    for dat in new_graphs :
        for idx in dat_whole.index :
            for clm in dat_whole.columns :
                if dat.at[idx,clm] > max :
                    max = dat.at[idx,clm]

    ncols = CROSSTAB_NCOLS
    nrows = int( math.ceil( ( nregs + CROSSTAB_CLEGEND ) / ncols ) )

    flag_enlarge = False
    len_max = 0
    for xlabel in new_graphs[0].columns :
        l = len( xlabel )
        if l > len_max :
            len_max = l
##    if len_max > 15 :
##        flag_enlarge = True
##        nrows += 1

    plt.rcParams["font.size"] = 7
    legend = copy.copy( new_graphs[0] )
    i = 0
    for dat in new_graphs :
        # rename index names to ''. this makes graphs larger
        tickl = {}
        for idx in dat.index :
            tickl.setdefault( idx, '' )
        ndat = dat.rename( mapper=tickl, axis='index' )
        # rename column names to ''
        tickl = {}
        for clm in dat.columns :
            tickl.setdefault( clm, '' )
        ndat = ndat.rename( mapper=tickl, axis='columns' )

        if csv_outdir != '' :
            sreg = list_regions[i].replace( 'Europe:', '' )
            if sreg == 'others' :
                sreg = 'EU-others'
            ndat.to_csv( csv_outdir + qno0 + '-' + qno1 + \
                             '-cross-' +  sreg + '.csv' )

        print( '\nRegion:', list_regions[i], '\n', dat )
#        print( nregs, nrows, ncols, int(i/ncols), int(i%ncols) )
        ax = plt.subplot2grid( ( nrows, ncols ), 
                               ( int(i/ncols), int(i%ncols) ) )
        ax.set_title( list_regions[i] )
        sns.heatmap( ndat, 
                     cmap=CROSSTAB_COLOR, 
                     cbar=False, 
                     annot=False, #square=True, 
#                     annot=True, #square=True, 
                     linewidths=0.5, linecolor='black', 
                     xticklabels=False, yticklabels=False,
#                     xticklabels=True, yticklabels=True,
                     vmin=0.0, vmax=max,
                     ax=ax )
        ax.set_xlabel( '' )
        ax.set_ylabel( '' )
        i += 1

    # LEGEND
 #    plt.subplots_adjust( bottom=0.8 )
    i = ( nrows * ncols ) - CROSSTAB_CLEGEND + 1
    if flag_enlarge :
        ax = plt.subplot2grid( ( nrows, ncols ), 
                               ( int(i/ncols), int(i%ncols) ),
                               colspan=CROSSTAB_CLEGEND-1 )
    else :
        ax = plt.subplot2grid( ( nrows, ncols ), 
                               ( int(i/ncols), int(i%ncols) ),
                               colspan=CROSSTAB_CLEGEND-1 )
    print( '\nLEGEND\n', legend )
    nrows, ncols = legend.shape
#    print( 'nrows=', nrows, 'ncols=', ncols )
    nn = nrows * ncols
    for i in range( 0, nrows ) :
        for j in range( 0, ncols ) :
# hatch
#            legend.iat[i,j] = ( ( ( (j+1) % 2 ) + ( i % 2 ) ) % 2 ) * 0.5
# 
#            legend.iat[i,j] = float( i + j ) / float( nn ) * max * 100
            legend.iat[i,j] = float( i * ncols + j ) / float( nn ) * max * 100
#    ax.set_title( 'Legend' )
    ax.set_autoscale_on( True )
    ax.set_ylim( 0.8 )

    sns.heatmap( legend, 
                 cmap=CROSSTAB_COLOR, 
                 cbar=False, 
                 annot=True, #square=True, 
                 linewidths=0.5, linecolor='black', 
                 xticklabels=True, yticklabels=True,
                 ax=ax )
 #   plt.subplots_adjust(hspace=0.4)

    if qno0 in multi_answer :
        ax.set_ylabel( qno0 + '*:' + question_tab[qno0] )
    else :
        ax.set_ylabel( qno0 + ':'  + question_tab[qno0] )
    if qno1 in multi_answer :
        ax.set_xlabel( qno1 + '*:' + question_tab[qno1] )
    else :
        ax.set_xlabel( qno1 + ':'  + question_tab[qno1] )

    if len_max > 10 :
        for label in ax.get_xmajorticklabels() :
            label.set_rotation( 15 )
            label.set_horizontalalignment( "right" )

    plt.tight_layout()
    if format == '' and not flag_tex :
        plt.show()
    else :
        fn = dirname + qno0 + '-' + qno1 + '.' + format
        print( '\nFilename:', fn )
        if flag_tex :
            plt.savefig( fn, transparent=False )
        else :
            plt.savefig( fn, transparent=True )
    plt.close( 'all' )

    if flag_tex :
        tex_list = []
        tex_list.append( '\\begin{description}%\n' )
        tex_list.append( '\\item{' + qno0 + '} ' + dict_orgq[qno0] + '%\n' )
        tex_list.append( '\\item{' + qno1 + '} ' + dict_orgq[qno1] + '%\n' )
        tex_list.append( '\\end{description}%\n' )
        fn = tex_outdir + qno0 + '-' + qno1 + '-questions.tex'
        with open( fn, mode='w' ) as f :
            f.writelines( tex_list )
    return

def summary () :
    ##print( '** Whole Data **' )
    ##print( df_whole )
    print( '\n\n** SUMMARY **' )
    cs = df_whole['country'].value_counts( sort=True )
    print( cs )
    print( '' ) # newline
    nc = len(cs)
    print( '# Countries:\t' + str( nc ) )
    nans = len( df_whole.index )
    print( '# Answers:\t' + str( nans ) )
    if flag_tex :
        tex_list = []
        tex_list.append( '\\begin{table}[htb]%\n' )
        tex_list.append( '\\begin{center}%\n' )
        tex_list.append( '\\caption{Country}\\label{tab:countries}%\n' )
        tex_list.append( '\\begin{tabular}{l|c|l|r}%\n' )
        tex_list.append( '\\hline%\n' )
        tex_list.append( 'Country & Abbrv. & Region & \# Answers \\\\%\n' )
        tex_list.append( '\\hline%\n' )
        prev = cs[0]
        for i in range( 0, len(cs) ) :
            if prev >= major_region and cs[i] < major_region :
                tex_list.append( '\\hline%\n' )
            country = cs.index[i]
            if country in country_abbrv :
                abbrv = country_abbrv[country]
            elif 'Europe:' + country in country_abbrv :
                abbrv = country_abbrv['Europe:'+country]
            else :
                abbrv = ''
            prev   = cs[i]
            region = region_tab[country]
            tex_list.append( country + '&' + \
                                 abbrv  + '&' + \
                                 region + '&' + \
                                 str( cs[i] ) + '\\\\%\n' )
        tex_list.append( '\\hline%\n' )
        tex_list.append( str( nc ) + ' countries & & & ' + \
                             str( nans ) + ' answers \\\\%\n' )
        tex_list.append( '\\hline%\n' )
        tex_list.append( '\\end{tabular}%\n' )
        tex_list.append( '\\end{center}%\n' )
        tex_list.append( '\\end{table}%\n' )
        with open( tex_outdir + 'countries.tex', mode='w' ) as f :
            f.writelines( tex_list )
    return

def response_rate() :
    nregs = len(regions_major)
    if flag_tex :
        tex_list = []
        tabs = '|c|'
        cols = 'Q'
        for reg in regions_major :
            tabs += 'c|'
            cols += ' & {\\footnotesize ' + reg.replace('Europe','EU') + '}'
        cols += '\\\\%\n'
        tex_list.append( '\\begin{table}[htb]%\n' )
        tex_list.append( '\\begin{center}\\small%\n' )
        tex_list.append( '\\caption{Number of Abstains (percent in paranthesis)}' )
        tex_list.append( '\\label{tab:abstain}%\n' )
        tex_list.append( '\\begin{tabular}{' + tabs + '}%\n' )
        tex_list.append( '\\hline%\n' )
        tex_list.append( cols )
        tex_list.append( '\\hline%\n' )
        numans = '\#Ans'
        for reg in regions_major :
            df_rq = df_whole[df_whole['Region']==reg]['Q1']
            tans  = len( df_rq.index )
            numans += ' & ' + str( tans )
        tex_list.append( numans )
        tex_list.append( ' \\\\%\n' )
        tex_list.append( '\\hline%\n' )
        for q in range(1,30) :
            qno = 'Q' + str(q)
            tex_list.append( '\\hline%\n' )
            tex_list.append( qno )
            for reg in regions_major :
                df_rq = df_whole[df_whole['Region']==reg][qno]
                nnull = df_rq == ''
                noans = nnull.sum()
                tans  = len( df_rq.index )
                if noans > 0 :
                    regrr = str(noans) + ' (' + str( round(noans/tans*100,1) ) + ')'
                else :
                    regrr = '0'
                tex_list.append( ' & ' + regrr )
            tex_list.append( ' \\\\%\n' )
        tex_list.append( '\\hline%\n' )
        tex_list.append( '\\end{tabular}%\n' )
        tex_list.append( '\\end{center}%\n' )
        tex_list.append( '\\end{table}%\n' )
        with open( tex_outdir + 'response-rate.tex', mode='w' ) as f :
            f.writelines( tex_list )
    return

if flag_timeseries : 
    graph_time_series( df_whole )

response_rate()

for qno in list_simple :
    simple_analysis( dict_qno, dict_others, qno )

for qno in multi_answer :
    table_and_graph_multi_ans( qno )

for cross in list_cross :
    cross_tab( cross[0], cross[1] )

summary()

##if __name__ == '__main__':
##    main()

exit( 0 )
