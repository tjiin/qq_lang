#!/bin/bash

# Colors
ESC_SEQ="\x1b["
COL_RESET=$ESC_SEQ"39;49;00m"
COL_RED=$ESC_SEQ"31;01m"
COL_GREEN=$ESC_SEQ"32;01m"
COL_YELLOW=$ESC_SEQ"33;01m"
COL_CYAN=$ESC_SEQ"34;01m"
COL_MAGENTA=$ESC_SEQ"35;01m"
COL_CYAN=$ESC_SEQ"36;01m"

program_name=$0

function usage {
	echo "Takes .c or .cpp files, compiles and runs it"
	echo "(if -a is present)."
	echo "usage: $program_name [-ah] [-f infile] [-o outfile]"
	echo "   -a		  avoid running the exe, just compile"
	echo "   -h		  display help"
	echo "   -f infile	  specify input file infile"
	echo "   -o outfile	  specify output file outfile"
	exit 1
}

infile="test.c"
outfile="test.exe"
avoid_run=0
while [ "$1" != "" ]; do
    case $1 in
        -f | --infile )         shift
                                infile=$1
                                ;;			
        -o | --outfile )        shift
           						outfile=$1
           						;;
		-a | --avoid_run )  	avoid_run=1
        						;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

if [ "$infile" = "" ]; then echo "No infile given, assuming default filename test.c"; fi
if [ "$outfile" = "" ]; then echo "No outfile given, assuming default filename test.exe"; fi
if [ ! -f $infile ]; then
	while [ ! -f $infile ]; do
	echo "The file '$infile' doesn't seem to exist!.."
	echo "Do you want to enter the filename again? (yes/no)"
	read -p "(If not, I'm going to exit): " -n 1 -r
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		echo -e " \n "
		read -e -p "Enter input filename: " -r  # -e adds tab complete for filenames
		infile=$REPLY
	else
		printf "\nBye\n"
		exit 1
	fi
	done
	echo "Good that'll work."
fi

ext="$(echo $infile | awk -F . '{print $NF}')"
echo $ext
if [[ "$ext" == "cpp" ]]
then sudo g++ -o $outfile $infile && echo -e "$COL_CYAN sudo g++ -o  $outfile $infile $COL_RESET" ;
elif [[ "$ext" == "c" ]]
then sudo gcc $infile -o $outfile && echo -e "$COL_CYAN gcc $infile -o $outfile $COL_RESET" ;	
else echo "Error: Unknown input file type" && exit 1
fi

sudo chmod +x $outfile
echo -e "$COL_CYAN chmod +x $outfile $COL_RESET"
if [ 0 -eq $avoid_run ]
then echo -e "$COL_CYAN./$outfile $COL_RESET" ; sudo ./$outfile ; echo -e "\n "
else echo "Compile finished, didn't run program"
fi

exit 1