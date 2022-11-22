#!/bin/bash
# @name: solr_import.sh
# @creation_date: 2022-03-11
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Runs imports of files into Solr indexes
# @acknowledgements:
# https://www.redhat.com/sysadmin/arguments-options-bash-scripts

############################################################
# subprograms                                              #
############################################################
License()
{
  echo 'Copyright 2022 Simon Bowie <ad7588@coventry.ac.uk>'
  echo
  echo 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:'
  echo
  echo 'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.'
  echo
  echo 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
}

Help()
{
   # Display Help
   echo "This script performs Solr import functions for different cores."
   echo
   echo "Syntax: solr_import.sh [-l|h|z|e|a|x|d|p|w|r|t]"
   echo "options:"
   echo "l     Print the MIT License notification."
   echo "h     Print this Help."
   echo "z     Index all."
   echo "e     Index EXPANDING folder."
   echo "a     Index ACTIVE folder."
   echo "x     Index SECRET folder."
   echo "d     Index SELF-DEFENDING folder."
   echo "p     Index LEAKING folder."
   echo "w     Index WORKING folder."
   echo "r     Index RESOURCEFUL folder."
   echo "t     Index all themes folders."
   echo
}

Import()
{
  docker exec -it solr bin/solr delete -c $core

  docker exec -it solr solr create_core -c $core -d custom

  #docker exec -ti --user=solr solr bash -c "cp -r /opt/solr/example/files/conf/* /var/solr/data/$core/conf/"

  #docker restart solr

  sleep 30

  docker run --rm -v "$main_directory/$location:/$core" --network=host solr:8.11.1 post -c $core /$core
}

Import_recursive()
{
  docker run --rm -v "$main_directory/$subdirectory:/$core" --network=host solr:8.11.1 post -c $core /$core
}
############################################################
############################################################
# main program                                             #
############################################################
############################################################

# set variables
main_directory="/Users/ad7588/projects/patent_site_python"
expanding_directory="data/pop_rtfs/EXPANDING (169)"
active_directory="data/pop_rtfs/ACTIVE (160)"
secret_directory="data/pop_rtfs/SECRET (92)"
leaking_directory="data/pop_rtfs/LEAKING (168)"
working_directory="data/pop_rtfs/WORKING (101)"
resourceful_directory="data/pop_rtfs/RESOURCEFUL (166)"

# error message for no flags
if (( $# == 0 )); then
    Help
    exit 1
fi

# get the options
while getopts ":lhzeaxdpwrt" option; do
   case $option in
      l) # display License
        License
        exit;;
      h) # display Help
        Help
        exit;;
      z) # index all
        core="all"
        docker exec -it solr bin/solr delete -c $core
        docker exec -it solr solr create_core -c $core -d custom
        location="data/POP_Dataset_2022"
          for subdirectory in $location/*/
          do
            subdirectory=${subdirectory%*/}      # remove the trailing "/"
            Import_recursive
          done
        exit;;
      e) # index EXPANDING folder
        core="expanding"
        location=$expanding_directory
        Import
        exit;;
      a) # index ACTIVE folder
        core="active"
        location=$active_directory
        Import
        exit;;
      x) # index SECRET folder
        core="secret"
        location=$secret_directory
        Import
        exit;;
      p) # index LEAKING folder
        core="leaking"
        location=$leaking_directory
        Import
        exit;;
      w) # index WORKING folder
        core="working"
        location=$working_directory
        Import
        exit;;
      r) # index RESOURCEFUL folder
        core="resourceful"
        location=$resourceful_directory
        Import
        exit;;
      t) # index all themes folders
        core="expanding"
        location=$expanding_directory
        Import
        core="active"
        location=$active_directory
        Import
        core="secret"
        location=$secret_directory
        Import
        core="leaking"
        location=$leaking_directory
        Import
        core="working"
        location=$working_directory
        Import
        core="resourceful"
        location=$resourceful_directory
        Import
        exit;;
      \?) # Invalid option
        Help
        exit;;
   esac
done
