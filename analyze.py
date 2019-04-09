#!/usr/local/bin/python3

## written by Atsushi Hori (ahori@riken.jp) at 
## Riken Center for Computational Science
## 2019 April

# Preparation
# python3
# and Python modules listed below

import os
import sys
import datetime
import pandas as pd
from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.dates import date2num

PREPROCESS = '' # if specified, then the csv file is preprocessed
REGION_COUNTRY = True # if True, major countries will also be appear
FILE_TYPE = 'pdf' # if specified, then graphs are saved in this format
#FILE_TYPE = '' # if file type is not specified, then graphs will be shown
EVENT_SHOW = True # if True, events are wshown in TimeSeries graph

event_list = [ # [ year, month, day, event-name, text-height ]
    [ 2019, 2, 18, 'hpc-announce [1]', 20 ],
    [ 2019, 2, 21, 'swopp (Japan) [1]', 40 ],
    [ 2019, 2, 27, 'Sanjay@UIUC', 60 ],
    [ 2019, 2, 27, 'Artem@Mellanox', 80 ],
    [ 2019, 2, 27, 'swopp (Japan) [2]', 100 ],
    [ 2019, 3,  1, 'hpc-announce [2]', 10 ],
    [ 2019, 3, 19, 'hpc-announce [3]', 30 ],
    [ 2019, 4,  1, 'Rolf@HLRS', 50 ]
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
               'United arab Emirates '	: 'Asia',
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
                 'Q15' : 'How to check MPI Spec.?',
                 'Q16' : 'MPI Difficulty', 
                 'Q17' : 'Known MPI Fetures',
                 'Q18' : 'MPI Aspects',
                 'Q19' : 'MPI Thread Level',
                 'Q20' : 'MPI Obstacles', 
                 'Q21' : 'Error Checking',
                 'Q22' : 'Packing MPI calls', 
                 'Q23' : 'MPI+X',
                 'Q24' : 'Room for Tuning',
                 'Q25' : 'Alternatives',
                 'Q26' : 'Missing Fetures',
                 'Q27' : 'Missing semantics',
                 'Q28' : 'Unnecessary Features',
                 'Q29' : 'Backward Compatibility',
                 'Q30' : 'Tradeoff between performance and portability'
              }

multi_answer = [ 'Q5', 'Q8', 'Q9', 'Q11', 'Q12', 'Q13', 'Q15', 
                 'Q17', 'Q18', 'Q19', 'Q20', 'Q22', 'Q23', 'Q24', 'Q25', 
                 'Q26', 'Q27', 'Q28', 'Q29' ]

print_other = [ 'Q5', 'Q8', 'Q9', 'Q11', 'Q12', 'Q13', 'Q15', 'Q18', 'Q20',
                'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28', 'Q29' ]

color_list =  ["r", "g", "b", "c", "m", "y"]

def conv_date ( q0_str ) :
    ymd = q0_str.split().pop(0)
    return datetime.datetime.strptime( ymd, '%Y/%m/%d' ).date()

def unique ( list ) :
    unique_list = []
    for elm in list :
        if elm not in unique_list :
            unique_list.append( elm )
    return unique_list

if len( sys.argv ) < 2 :
    print( 'Input CSV file must be specified' )
    exit( 1 )
csv_in = sys.argv[1]

if PREPROCESS != '' :
    tmpfile = csv_in + '.ascii'
    os.system( 'nkf ' + '"' + csv_in + '" > "' + tmpfile + '"' )
    df = pd.read_csv( tmpfile, sep=',')
    os.remove( tmpfile )
else :
    df = pd.read_csv( csv_in, sep=',')
basename = os.path.splitext( os.path.basename( csv_in ) )[0].replace(' ','')

# shorten long country names
df = df.replace( 'United Kingdom', 	'UK'  )
df = df.replace( 'United States', 	'USA' )

total_answers = len( df )
print( total_answers )

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

if REGION_COUNTRY == 'Region' :
    # adding Region column
    region_list = []
    for country in countries :
        region = region_tab[ country ]
        region_list.append( region )
else :
    # adding another Region column
    region_list = []
    for country in countries :
        region = region_tab[ country ]
        if len( df[df['Q2']==country] ) > 30 and \
                region != country :
            region_tab.setdefault( region, country )
            region_list.append( region + ':' + country )
        else :
            region_list.append( region )
df_whole = df.assign( Region = region_list )
print( df_whole )

def graph_time_series( df ) :
    # adding 'Date' column
    dt_list = []
    date_dict = {}
    for dt in df['Q0'] :
        dt_list.append( conv_date( dt ) )
    df = df.assign( Date = dt_list )
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
        for j in range( 0, len(unique(region_list)) ) :
            dc.iat[i,j] += dc.iat[i-1,j]

# drop regions having less number of answers
    dc_etc = dc.assign( ETC = dc[region_list.pop(0)] )
#    print( dc_etc )
    for i in range( 0, len(dc) ) :
        dc_etc['ETC'].iat[i] = 0
    for reg in unique(region_list) :
        if dc_etc[reg].iat[-1] < 30 :
            for i in range( 0, len(dc) ) :
                dc_etc['ETC'].iat[i] += dc_etc[reg].iat[i]
    for reg in unique(region_list) :
        if dc_etc[reg].iat[-1] < 30 :
            dc_etc = dc_etc.drop( [reg], axis=1 )
    
# now we can draw a time series graph
    fig = plt.figure()
    ax = fig.add_subplot(111)
    dc_etc.plot.area(ax=ax, stacked=True, color=color_list)

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
    ax.tick_params(axis="x", which="major", labelsize=10)
    
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b"))
    ax.tick_params(axis="x", which="minor", labelsize=10, length=15, width=1)

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
        plt.savefig(basename+'-TimeSeries.'+FILE_TYPE)
    return

def graph_percentage( all, qno, legend, last='', 
                      order='', legend_reverse=False,
                      scale=0.8) :
    print( '\n**** ' + qno + ': ' + question_tab[qno] + ' ****')
    dict_tmp  = {}
    list_sum  = []
    whole     = 'whole'
    list_regs = [ whole ]

# creating region list
    regions = []
#    print( unique( region_tab.values() ) )
    for reg in unique( region_list ) :
        df_reg = all.query( 'Region=='+'"'+reg+'"' ) 
        if len( df_reg ) > 30 :
            regions.append( reg )
    regions.sort()
#    print( regions )


# list all the 'other' answers
    list_others = []
    if qno in print_other :
        if qno in multi_answer :
            for mans in all[qno] :
                if mans == mans :
                    for ans in mans.split( ';' ) :
                        if not ans in legend.keys() :
                            list_others.append( ans )
        else :
            for ans in all[qno] :
                if ans == ans and not ans in legend.keys() :
                    list_others.append( ans )

# convert to percent numbers on whole data
# decompose answer if this is a multiple-answer question
    if qno in multi_answer :
        dict_mans = {}
        for sans in legend.keys() :
            dict_mans.setdefault( sans, 0 )
        tmp = all[qno]
        for mans in pd.Series( data=tmp, dtype=str ) :
            list_ans = mans.split( ';' )
            for ans in list_ans :
                if ans in legend.keys() :
                    dict_mans[ans] += 1
                else :
                    dict_mans['Other'] += 1
        tmp = pd.Series( dict_mans, dtype=float )
#        print( tmp )
    else :
        tmp = all[qno].value_counts( sort=False )
    ser = pd.Series( data=tmp, dtype=float )
    sum = int(0)
    for elm in ser :
        sum += int( elm + 0.001 )
    list_sum.append( sum )
    for i in range( ser.size ) :
        ser.iat[i] = ser.iat[i] / float(sum) * 100.0
    dict_tmp.setdefault( whole, ser )
    dfq = pd.DataFrame( data=dict_tmp )
#    print( dfq )

# convert to percent numbers for each region
    for reg in regions :
        if qno in multi_answer :
            dict_mans = {}
            for sans in legend.keys() :
                dict_mans.setdefault( sans, 0 )
#            print( dict_mans )
            tmp = all[all['Region']==reg][qno]
            for mans in pd.Series( data=tmp, dtype=str ) :
                list_ans = mans.split( ';' )
                for ans in list_ans :
                    if ans in legend.keys() :
                        dict_mans[ans] += 1
                    else :
                        dict_mans['Other'] += 1
            ser = pd.Series( dict_mans, dtype=float )
#            print( ser )
        else :
            tmp = all[all['Region']==reg][qno].value_counts(sort=False)
            ser = pd.Series( data=tmp, dtype=float )
        sum = int(0)
        for elm in ser :
            sum += int( elm + 0.001 )
        list_sum.append( sum )
        for i in range( ser.size ) :
            ser.iat[i] = ser.iat[i] / float(sum) * 100.0
        dict_tmp.setdefault( reg, ser )
        perc = pd.DataFrame( data=dict_tmp )
        dfq = pd.concat( [ perc ], axis=1, sort=False )
    dfq.fillna( 0.0, inplace=True )

#    print( dfq )

# setup legend
    if legend != '' :
        idxs = dfq.index
        for idx_name in idxs :
            dfq.rename(index={idx_name: legend[idx_name]}, inplace=True)

#    print( dfq )

# move the specified line to the last (if specified)
    idxs = dfq.index
    if idxs.contains( last ) :
        idxl = idxs.drop( last ).tolist()
        idxl.append( last )
        dfq = dfq.reindex( index=idxl )

# reorder index (if specified)
    if order == 'sort' :
        dfq = dfq.sort_values( whole, ascending=False )

    elif order == 'reverse' :
        dfq = dfq.reindex( index=dfq.index[::-1] )

    elif type( order ) is list :
        dfq = dfq.reindex( index=order )
        dfq_idx = dfq.value_counts
        if len(list) < len( dfq_idx ) :
            diff = list( set(dfq_idx) - set(list) )
            list_idx = dfq.index.tolist()
            list_etc = []
            for reg in regions :
                sum = 0.0
                for e in diff :
                    sum += dfq.loc[e,reg]
                list_etc.append( sum )
            dfq = dfq.drop( diff )
            etc = pd.Series( list_etc, 
                             index=[ whole ] + regions, 
                             name='(etc.)' )
            dfq.loc['(etc.)'] = etc
            
    elif type(order) is int :
        top = order
        nidx = len( dfq.index )
        if top > 0 and nidx > top :
            dfq = dfq.sort_values( whole, ascending=False )
            list_idx = dfq.index.tolist()
            list_etc = []
            for i in range( 0, len( regions ) + 1 ) :
                sum = 0.0
                for j in range( top, nidx ) :
                    sum += dfq.iat[j,i]
                list_etc.append( sum )
            for i in range( 0, top ) :
                list_idx.pop(0)
            dfq = dfq.drop( list_idx )
            etc = pd.Series( list_etc, 
                             index=[ whole ] + regions, 
                             name='(etc.)' )
            dfq.loc['(etc.)'] = etc

# adding numbers to the tiltle
    for column_name in dfq :
        newc = column_name + '\n(' + str(list_sum.pop(0)) + \
        ' / ' + str(total_answers) + ')'
        dfq.rename( columns={column_name: newc}, inplace=True )

# print data 
    if qno in print_other :
        i = 0
        for ans in set( list_others ) :
            print( '[' + str(i) + '] ' + ans )
            i += 1
        print( '' )             # new line
    print( dfq )                # print data

# eventually draw a graph (stacked bar in percentage)
    trans = dfq.T
    trans.plot.bar( stacked=True, color=color_list )
    if legend_reverse :
        plt.legend( labelspacing=-2.5, frameon=True )
    plt.subplots_adjust( right=scale, bottom=0.3 )
    plt.legend( dfq.index, bbox_to_anchor=(1, 1), )
    plt.ylabel( 'Percentage' )
    if qno in multi_answer :
        plt.title( qno + '* : ' + question_tab[qno] )
    else :
        plt.title( qno + ' : ' + question_tab[qno] )
    plt.ylabel( 'Percentage' )
    if FILE_TYPE == '' :
        plt.show()
    else :
        plt.savefig(basename+'-'+qno+'.'+FILE_TYPE)
    return

graph_time_series( df_whole )

graph_percentage( df_whole,
                  'Q1',
                  { 'College/University' : 'University',
                    'Governmental institute' : 'Government',
                    'Hardware vendor' : 'HW',
                    'Software vendor' : 'SW',
                    'Private research institute' : 'Private',
                    'Other' : 'other' },
                  last = 'Other',
                  scale = 0.75
                  )

graph_percentage( df_whole,
                  'Q3',
                  { 1 : 'Low',
                    2 : '2',
                    3 : '3',
                    4 : '4',
                    5 : '5',
                    6 : 'High' },
                  order = 'reverse' )

graph_percentage( df_whole,
                  'Q4',
                  { 1 : 'Low',
                    2 : '2',
                    3 : '3',
                    4 : '4',
                    5 : '5',
                    6 : 'High' },
                  order = 'reverse' )

graph_percentage( df_whole,
                  'Q5',
                  { 'C/C++' : 'C/C++',
                    'Fortran 90 or newer' : '>F90',
                    'Fortran (older one than Fortran 90)' : '<F90',
                    'Python' : 'Python',
                    'Java' : 'Java',
                    'Other' : 'other' } 
                  )
graph_percentage( df_whole,
                  'Q6',
                  { 'more than 10 years' : '>10',
                    'between 5 and 10 years' : '5-10',
                    'between 2 and 5 years' : '2-5',
                    'less than 2 years' : '<2' },
                  order = 'reverse')

graph_percentage( df_whole,
                  'Q7',
                  { 'more than 10 years' : '>10',
                    'between 5 and 10 years' : '5-10',
                    'between 2 and 5 years' : '2-5',
                    'less than 2 years' : '<2' } )

graph_percentage( df_whole,
                  'Q8',
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
                  scale = 0.68
                  )

graph_percentage( df_whole,
                  'Q9',
                  { 'Research and development of application(s)' : 'R&D Apps',
                    'Research and development on system software (OS and/or runtime library)' : 'R&D OS/Runtime',
                    'Research and development software tool(s)' : 'R&D Tools',
                    'Parallelization of sequential program(s)' : 'Parralelization',
                    'Performance tuning of MPI program(s)' : 'MPI Tuning',
                    'Debugging MPI programs' : 'Debugging',
                    'Other' : 'other'
                    },
                  scale = 0.68
                  )

graph_percentage( df_whole,
                  'Q10',
                  { 'I read all.' : 'All',
                    'I read most of it.' : 'Mostly',
                    'I read only the chapters of interest for my work.' : 'Partly',
                    'I have not read it, but I plan to.' : 'Wish',
                    'No, and I will not read it.' : 'No' } )

graph_percentage( df_whole,
                  'Q11',
                  { 'I read the MPI standard document.' : 'Read MPI standard',
                    'I read book(s).' : 'MPI Book(s)',
                    'I had lecture(s) at school.' : 'School Lecture(s)',
                    'Other lectures or tutorials (workplace, conference).' : 'Other lecture(s)',
                    'I read articles found on Internet.' : 'Internet',
                    'I have not learned MPI.' : 'No learning',
                    'Other' : 'other'
                    },
                  scale = 0.68
                  )

graph_percentage( df_whole,
                  'Q12',
                  { 'Beginning MPI (An Introduction in C)' : 'Beginning MPI',
                    'Parallel Programming with MPI' : 'Parallel Programming\nwith MPI',
                    'Using MPI' : 'Using MPI',
                    'Parallel Programming in C with MPI and OpenMP' : 'Parallel Programming\nin C with MPI and OpenMP',
                    'MPI: The Complete Reference' : 'MPI: the complete\nReference',
                    'I have never read any MPI books' : '(never read)',
                    'Other' : 'other'
                    },
                  scale=0.6
                  )

graph_percentage( df_whole,
                  'Q13',
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
                    'Other' : 'other'
                    },
                  order=6
                  )

graph_percentage( df_whole,
                  'Q14',
                  { 'I like to use it.' : 'I like',
                    'I was said to use it.' : 'Said to use',
                    'I could not have any choice (the one provided by a vendor).' : 'No choice',
                    'I am familiar with it.' : 'I am familiar',
                    'I have no special reason.' : 'No reason' },
                  scale = 0.73
                  )

graph_percentage( df_whole,
                  'Q15',
                  { 'I read the MPI Standard document (web/book).' : 'MPI standard',
                    'I read book(s) (except the MPI standard).' : 'Book',
                    'I read online documents (such as man pages).' : 'Online docs',
                    'I ask colleagues.' : 'I ask colleagues.',
                    'I search the Internet (Google / Stack Overflow).' : 'Internet',
                    'I know almost all MPI routines.' : 'I know all',
                    'Other' : 'other'
                    },
                  scale = 0.7
                  )

graph_percentage( df_whole,
                  'Q16',
                  { 'Algorithm design' : 'Algorithm',
                    'Debugging' : 'Debugging',
                    'Domain decomposition' : 'Decomposition',
                    'Finding appropriate MPI routines' : 'Finding MPI routines',
                    'Implementation issue workaround' : 'Workaround',
                    'Performance tuning' : 'Tuning',
                    'Other' : 'other' },
                  last = 'Other',
                  scale = 0.67
                  )

graph_percentage( df_whole,
                  'Q17',
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
                  scale = 0.7
                  )

graph_percentage( df_whole,
                  'Q18',
                  { 'Point-to-point communications' : 'Pt2Pt',
                    'Collective communications' : 'Collectives',
                    'Communicator operations (split, duplicate, and so on)' : 'Communicators',
                    'MPI datatypes' : 'MPI datatypes',
                    'One-sided communications' : 'One-sided',
                    'Dynamic process creation' : 'Dynamic process',
                    'Persistent communications' : 'Persistent',
                    'MPI with OpenMP (or multithread)' : 'MPI with OpenMP',
                    'PMPI interface' : 'PMPI',
                    'Other' : 'other',
                    },
                  scale = 0.7
                  )

graph_percentage( df_whole,
                  'Q19',
                  { 'MPI_THREAD_SINGLE' : 'SINGLE',
                    'MPI_THREAD_FUNNELED' : 'FUNNELED',
                    'MPI_THREAD_SERIALIZED' : 'SERIALIZED',
                    'MPI_THREAD_MULTIPLE' : 'MULTIPLE',
                    'I have never called MPI_INIT_THREAD' : 'Never used',
                    'I do not know or I do not care.' : 'Do not know/care',
                    'Other' : 'other'
                    },
                  scale = 0.7
                  )

graph_percentage( df_whole,
                  'Q20',
                  { 'I have no obstacles.' : 'No obstacles',
                    'Too many routines.' : 'Too many routines.',
                    'No appropriate lecture / book / info.' : 'No appropriate lecture',
                    'Too complicated and hard to understand.' : 'Too much complicated',
                    'I have nobody to ask.' : 'I have nobody to ask.',
                    'I do not like the API.' : 'I do not like the API.',
                    'Other' : 'other'
                    },
                  scale = 0.64
                  )

graph_percentage( df_whole,
                  'Q21',
                  { 'I rely on the default ‘Errors abort’ error handling' : 'Default',
                    'Always' : 'Always',
                    'Mostly' : 'Mostly',
                    'Sometimes' : 'Sometimes',
                    'Never' : 'Never',
                    'Other' : 'other' 
                    },
                  scale = 0.76
                  )

graph_percentage( df_whole,
                  'Q22',
                  { 'Yes, to minimize the changes of communication API.' : 'Yes',
                    'Yes, but I have no special reason for doing that.' : 'Yes, but no reason',
                    'No, my program is too small to do that.' : 'No, too small',
                    'No, MPI calls are scattered in my programs.' : 'No, scattered',
                    'Other' : 'other'
                    },
                  scale = 0.7
                   )

graph_percentage( df_whole,
                  'Q23',
                  { 'OpenMP' : 'OpenMP',
                    'Pthread' : 'Pthread',
                    'OpenACC' : 'OpenACC',
                    'OpenCL' : 'OpenCL',
                    'CUDA' : 'CUDA',
                    'No' : 'No',
                    'Other' : 'other'
                    }
                  )

graph_percentage( df_whole,
                  'Q24',
                  { 'No, my MPI programs are well-tuned.' : 'Well-tuned',
                    'I think there is room but I do not know how to tune it.' : 'No tknowing how to do',
                    'Yes, I know there is room for tuning but I do not have enough resources to do that.' : 'No resource',
                    'Yes, I know there is room for tuning but I should re-write large part of my program to do that.' : 'Rewrintg is hard',
                    'I think there is room but I do not know how to tune it.' : 'Not knowing how to tune',
                    'I have no chance to investigate.' : 'No chance to investigate',
                    'I do not know how to find bottlenecks.' : 'Not knowing how to find',
                    'I do not know if there is more to improve' : 'Not knowing how to improve',
                    'Other' : 'other'
                    },
                  scale = 0.58
                  )

graph_percentage( df_whole,
                  'Q25',
                  { 'A framework or library using MPI.' : 'Framework',
                    'A PGAS language (UPC, Coarray Fortran, OpenSHMEM, XcalableMP, ...).' : 'PGAS',
                    'A Domain Specific Language (DSL).' : 'DSL',
                    'Low-level communication layer provided by vendor (Verbs, DCMF, ...).' : 'Low-level comm. layer',
                    'I am not investigating any alternatives.' : 'No investigation',
                    'Other' : 'other'
                    },
                  scale = 0.65
                  )

graph_percentage( df_whole,
                  'Q26',
                  { 'Latency' : 'Latency',
                    'Message injection rate' : 'Injection rate',
                    'Bandwidth' : 'Bandwidth',
                    'Additional optimization opportunities in terms of communication (topology awareness, locality, etc.)' : 'Additional comm. opt.',
                    'Optimization opportunities except communication (architecture awareness, dynamic processing, accelerator support, etc.)' : 'Other optimization',
                    'Multi-threading support' : 'Multi-threading\nsupport',
                    'Asynchronous progress' : 'Asynchronous progress',
                    'MPI provides all semantics I need' : 'Satisfied',
                    'Other' : 'other'
                    },
                  scale = 0.65
                  )

graph_percentage( df_whole,
                  'Q27',
                  { 'Latency hiding (including asynchronous completion)' : 'Latency hiding',
                    'Endpoints (multi-thread, sessions)' : 'End-points',
                    'Resilience (fault tolerance)' : 'Resilience',
                    'Additional optimization opportunities in terms of communication (topology awareness, locality, etc.)' : 'Additional optimization',
                    'Another API which is easier and/or simpler to use' : 'Another API',
                    'MPI is providing all the communication semantics required by my application' : 'MPI provides all',
                    'Other' : 'other'
                    },
                  scale = 0.62
                  )

graph_percentage( df_whole,
                  'Q28',
                  { 'One-sided communication' : 'One-sided',
                    'Datatypes' : 'Datatypes',
                    'Communicator and group management' : 'Communicator',
                    'Collective operations' : 'Collectives',
                    'Process topologies' : 'Process topologies',
                    'Dynamic process creation' : 'Dynamic process',
                    'Error handlers' : 'Error handlers',
                    'There are no unnecessary features' : 'No unnecessary features',
                    'Other' : 'other'
                    },
                  scale = 0.6
                  )

graph_percentage( df_whole,
                  'Q29',
                  { 'Yes, compatibility is very important for me.' : 'Very important',
                    'API should be clearly versioned.' : 'Versioned API',
                    'I prefer to have new API for better performance.' : 'New API for performance',
                    'I prefer to have new API which is simpler and/or easier-to-use.' : 'New API for easier-to-use',
                    'I do not know or I do not care.' : 'Do not know/care',
                    'Other' : 'other'
                    },
                  scale = 0.6
)

graph_percentage( df_whole,
                  'Q30',
                  { 1 : 'Portability',
                    2 : '2',
                    3 : '3',
                    4 : '4',
                    5 : 'Performance' },
                  scale = 0.75)

plt.close('all')


#if __name__ == '__main__':
#    main()
