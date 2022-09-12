#!/bin/bash
# @name: solr_import.sh
# @version: 0.1
# @creation_date: 2022-03-11
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Runs imports of files into Solr indexes
# @acknowledgements:
# https://www.redhat.com/sysadmin/arguments-options-bash-scripts

############################################################
# Subprograms                                              #
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
   echo "Syntax: solr_import.sh [-l|h|z|a|e|i|m|p|x|d|s|w]"
   echo "options:"
   echo "l     Print the MIT License notification."
   echo "h     Print this Help."
   echo "z     Index all."
   echo "a     Index ACTIVE folder."
   echo "e     Index EXPANDING folder."
   echo "i     Index INVISIBLE folder."
   echo "m     Index MULTI-SPECIES folder."
   echo "p     Index PISSING & LEAKING folder."
   echo "x     Index SECRET folder."
   echo "d     Index SELF-DEFENDING folder."
   echo "s     Index SURVIVING folder."
   echo "w     Index WORKING folder."
   echo
}

Import()
{
  docker exec -it solr bin/solr delete -c $core

  docker exec -it solr solr create_core -c $core -d custom

  #docker exec -ti --user=solr solr bash -c "cp -r /opt/solr/example/files/conf/* /var/solr/data/$core/conf/"

  #docker restart solr

  sleep 30

  docker run --rm -v "$directory/$location:/$core" --network=host solr:latest post -c $core /$core
}

Import_recursive()
{
  docker run --rm -v "$directory/$subdirectory:/$core" --network=host solr:latest post -c $core /$core
}
############################################################
############################################################
# Main program                                             #
############################################################
############################################################

# Set variables
directory="/Users/ad7588/projects/patent_site"

# Get the options
while getopts ":hlimzaespxdw" option; do
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
      a) # index ACTIVE folder
        core="active"
        location="data/pop_rtfs/ACTIVE (160)"
        Import
        exit;;
      e) # index EXPANDING folder
        core="expanding"
        location="data/pop_rtfs/EXPANDING (169)"
        Import
        exit;;
      i) # index INVISIBLE folder
        core="invisible"
        location="data/pop_rtfs/IN.VISIBLE (204)"
        Import
        exit;;
      m) # index MULTI-SPECIES folder
        core="multispecies"
        location="data/pop_rtfs/MULTI-SPECIES (180)"
        Import
        exit;;
      p) # index PISSING & LEAKING folder
        core="pissing"
        location="data/pop_rtfs/PISSING & LEAKING (168)"
        Import
        exit;;
      x) # index SECRET folder
        core="secret"
        location="data/pop_rtfs/SECRET (92)"
        Import
        exit;;
      d) # index SELF-DEFENDING folder
        core="defending"
        location="data/pop_rtfs/SELF-DEFENDING (115)"
        Import
        exit;;
      s) # index SURVIVING folder
        core="surviving"
        location="data/pop_rtfs/SURVIVING (166)"
        Import
        exit;;
      w) # index WORKING folder
        core="working"
        location="data/pop_rtfs/WORKING (101)"
        Import
        exit;;
      \?) # Invalid option
        echo "Error: Invalid option"
        exit;;
   esac
done
