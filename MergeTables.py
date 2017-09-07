#!/usr/bin/env python2.7

# @Name
# @Copyright Bruno Costa ITQB 2016
# @Description This is a program to merge files based on common columns must like in sql tabels
# @Description if nao key is found no value will be appended. This assumes that keys are unique. If not unique ------


#input1 - path(str) "Key value pairs						Required
#input2 - path(str) "File with keys 						Required
#output - path(str) "File with values appended to input2 	Required
#sep1 	- str "Seperator cac" 								Optional
#sep2 	- str "Seperator caracter" 							Optional
#column_key_input1	int										Required
#column_key_input2											Required
#column_value_input2 										Optional

import argparse
import operator, functools

parser = argparse.ArgumentParser(description='This is used to parse the blast result')

## blast result, output, cutoff,
#parser.add_argument('--flag', type=str, nargs=1, metavar='', dest='', required=True, help='')
parser.add_argument('--input1', type=str, metavar='input file', dest='input1', required=True, help='Path to the file with the keys and values')
parser.add_argument('--input2', type=str, metavar='input file', dest='input2', required=True, help='Path to the file with the key to which the values should be appended')
parser.add_argument('--output', type=str, metavar='output file', dest='output', required=True, help='Path where the file with the values appended should be stored')
parser.add_argument('--sep1', type=str, metavar='seperation string', dest='sep1', required=False, help='Set the seperation string for input 1. Default is \t')
parser.add_argument('--sep2', type=str, metavar='seperation string', dest='sep2', required=False, help='Set the seperation string for input 2. Default is \t')
parser.add_argument('--col_key_num_input1', type=int, metavar='column key number', dest='cKeyInput1', required=True, help='')
parser.add_argument('--col_key_num_input2', type=int, metavar='column key number', dest='cKeyInput2', required=True, help='')
parser.add_argument('--col_value_num_input2', type=int, metavar='column value number', dest='cValInput2', required=False, help='')
parser.add_argument('--log', type=int, metavar='log file', dest='log', required=False, help='Path where the log file should be stored with the information abount which keys wheren\'t found')
parser.add_argument('--append_result', type=bool , metavar='Result type', dest='result', required=False, help='')

args = parser.parse_args()

#Define variables
input1=args.input1
input2=args.input2
output=args.output
if(args.sep1==None):
	print("No input give will you tab as a seperator")
	sep1="\t"	
else:
	sep1=args.sep1
if(args.sep2==None):
	sep2="\t"
else:	
	sep2=args.sep2
if(args.result==None):
	result_format=False
else:
	result_format=True
col_key_input1=args.cKeyInput1
col_key_input2=args.cKeyInput2
col_val_input2=args.cValInput2
log=args.log

#Open files
key_value=open(input2,"r")
main_file=open(input1,"r")
writer=open(output,"w")
if(log!=None):
	logger=open(log,"w")
	log=True
else:
	log=False
#Process key_value
key_value=[line.strip().split(sep2) for line in key_value.readlines()]
#Save header
header_key_value=key_value[0]
#Delete header
del key_value[0]
dict_key_value={}
if(col_val_input2==None):
	header_key_value=header_key_value[0:col_key_input2]+header_key_value[(col_key_input2+1):len(header_key_value)]
	#If no column value number is given all column other then key are the value
	for line in key_value:
		try:
			#If the first element of this value is a string 
			#This is to create multiple lines in case the keys aren't unique
			if(type(dict_key_value[line[col_key_input2]][0])==str): 
				tmp=dict_key_value[line[col_key_input2]]
				dict_key_value[line[col_key_input2]]=[]
				dict_key_value[line[col_key_input2]].append(tmp)
				dict_key_value[line[col_key_input2]].append(line[0:col_key_input2] + line[(col_key_input2+1):len(line)])
			else:	
				dict_key_value[line[col_key_input2]].append(line[0:col_key_input2] + line[(col_key_input2+1):len(line)])
		except KeyError:
			dict_key_value[line[col_key_input2]]=line[0:col_key_input2] + line[(col_key_input2+1):len(line)]
else:
	header_key_value=[header_key_value[col_val_input2]]
	#Column with value is given one column is key the other is value other columns are discarted
	for line in key_value:
		try:
			if(type(dict_key_value[line[col_key_input2]])==str):
				#Transform to list if more keys are found
				tmp=dict_key_value[line[col_key_input2]]
				dict_key_value[line[col_key_input2]]=[]
				dict_key_value[line[col_key_input2]].append(tmp)
				dict_key_value[line[col_key_input2]].append(line[col_val_input2])
			else:
				#The first add as string
				dict_key_value[line[col_key_input2]].append(line[col_val_input2])
		except KeyError:
				dict_key_value[line[col_key_input2]]=line[col_val_input2]
			

#Start parsing main file
main_file=[line.strip().split(sep1) for line in main_file.readlines()]
header=main_file[0]
del main_file[0]
result_str=functools.reduce(lambda a, b :a+"\t"+b, header+header_key_value)
writer.write(result_str+"\n")
for line in main_file:
#for target in targets_results:
	try:
		#annotations=d[[]]
		values=dict_key_value[line[col_key_input1]]
		if(result_format):
			if(type(values)==str):
				result_str=functools.reduce(lambda a, b :a+"\t"+b, line+[values])
				writer.write(result_str+"\n")
			else:
				result_str=functools.reduce(lambda a, b :a+"\t"+b, line+values)#+"\t"+functools.reduce(lambda a, b :a+";"+b, values)
				writer.write(result_str+"\n")

		else:
			if(type(values)==str):
				print(type(line))
				print(type(values))
				result_str=functools.reduce(lambda a, b :a+"\t"+b, line+[values])
				writer.write(result_str+"\n")  		
			else:
				for value in values:
					result_str=functools.reduce(lambda a, b :a+"\t"+b, line+[value])
					writer.write(result_str+"\n")  		

	except (IndexError, KeyError), e:
		if(log):
			logger.write("Error - " + str(e))
		else:
			print("Error - " + str(e))
		if(type(dict_key_value[dict_key_value.keys()[0]][0])==str):	
			result_str=functools.reduce(lambda a, b :a+"\t"+b, line+["0"])#["-"]*len(dict_key_value[dict_key_value.keys()[0]]) )
		else:
			result_str=functools.reduce(lambda a, b :a+"\t"+b, line+["0"])#["-"]*len(dict_key_value[dict_key_value.keys()[0]][0]) )
		writer.write(result_str+"\n")  
	writer.flush()

writer.flush()
writer.close()
if(log):
	logger.flush()
	logger.close()	