# =======================
# Created by John M. Hunter on 15APR2015
# =======================
# Purpose - Create .TXT file for METVue
# Containing Lat/Long, Cumu Prec Total for Storm, Date, SHEF
# for all gages
# Parameters Definitions and Assignment
format_output = "%s,%s,%s,%s,%s,%s\n"
mm_inch_conversion = 0.00393700787401575
hundredthinch_inch_converstion = 0.01
Path_CSVFILES = r".\*.csv"
output_filename = "metvuetritin.txt"
log_filename = "flags_skipped.txt"
Indicator_Daily_Data = "Daily"
Initial_Line_Match = "Blank"
Blank_CSV_Cell = " "
Flag_A = "A"
Flag_P = "P"
Flag_T = "T"
# Imports Listing
import sys
import glob
import csv
# LIST .CSV Files in Directory 
path_list = glob.glob(Path_CSVFILES)
lenth_list = len(path_list)
# Creat Output file
output_file = open(output_filename, 'w')
log_file = open(log_filename, 'w')
# Read each .csv file
loop_counter = 0
while(loop_counter < lenth_list):
# set file_name
	if (loop_counter != lenth_list):
		file_name=path_list[loop_counter]
	else:
		print 'problem'
	print file_name
	loop_counter += 1
# read each .csv file attributes
	file_handle = open(file_name,"rU")
	file_read = csv.reader(file_handle)
	row_count = sum(1 for row in file_read)
	file_handle.seek(0)
	header = file_read.next()
	column_count = len(header)
# determine which coefficients to use (daily or not)
	# index string function
	indicator=file_name.find(Indicator_Daily_Data)
	if (indicator <= 0):
		coeff_precip = hundredthinch_inch_converstion #default
	else:
		#coeff_precip = mm_inch_conversion
		coeff_precip = hundredthinch_inch_converstion #default
		print coeff_precip
# process data in each .csv file
	enter_counter = 1
	gage_counter = 1
	loop_counter2 = 2
	line_match= Initial_Line_Match
	while (loop_counter2 <= row_count):
		line=file_read.next()
# Initial Gage
		if (line_match == Initial_Line_Match):
			if (line[7] == Blank_CSV_Cell):
				gage_total = float(line[6])
				line_match = line[1]
			elif (line[7] == Flag_A):
				gage_total = float(line[6])
				line_match = line[1]
			elif (line[7] == Flag_P):
				gage_total = float(line[6])
				line_match = line[1]
			elif (line[7] == Flag_T):
				gage_total = float(line[6])
				line_match = line[1]
			else:
				log_file.write('"%s" %s %s%s' %(file_name, 'flag:', line[7], '\n'))
				string = line[7]
				line_match = line[1]
# Continue Gage
		elif (line_match == line[1]):
			if (line[7] == Blank_CSV_Cell):
				gage_total += float(line[6])
				line_match = line[1]
			elif (line[7] ==  Flag_A):
				gage_total += float(line[6])
				line_match = line[1]
			elif (line[7] ==  Flag_P):
				gage_total += float(line[6])
				line_match = line[1]
			elif (line[7] ==  Flag_T):
				gage_total += float(line[6])
				line_match = line[1]
			else:
				log_file.write('"%s" %s %s%s' %(file_name, 'flag:', line[7], '\n'))
				line_match = line[1]
# New Gage
		else:
			output_tupple1 = (line_old[1], line_old[3], abs(float(line_old[4])), gage_total*coeff_precip,'2', line_old[1]+" "+str(gage_counter))
			output_file.write(format_output % output_tupple1)
			if (line[7] == Blank_CSV_Cell):
				gage_total = float(line[6])
				line_match = line[1]
			elif (line[7] ==  Flag_A):
				gage_total = float(line[6])
				line_match = line[1]
			elif (line[7] ==  Flag_T):
				gage_total = float(line[6])
				line_match = line[1]
			elif (line[7] ==  Flag_P):
				gage_total = float(line[6])
				line_match = line[1]
			else:
				log_file.write('"%s" %s %s%s' %(file_name, 'flag:', line[7], '\n'))
				line_match = line[1]
			gage_counter += 1
		line_old=line
		loop_counter2 += 1
	output_tupple2 = (line[1], line[3], abs(float(line[4])), gage_total*coeff_precip ,'2', line[1]+" "+str(gage_counter))
	output_file.write(format_output % output_tupple2)
print 'Total files processed above:' + str(lenth_list)
print 'Finished, please review flags_skipped.txt and ensure entry was not important.'
print 'Precip unit of csv files from ncdc should be hundredth of inches.'
print 'Results will be units of inches compatible with dss.'
output_file.close()
log_file.close()
