/*
# @name: main.js
# @version: 0.1
# @creation_date: 2022-09-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: JavaScript functions for various functions
# @acknowledgements:
*/

function hideShowInfo () {
      var iDiv = document.querySelectorAll('.info'), i;
  for (i = 0; i < iDiv.length; ++i) {
     if ( iDiv[i].style.display == 'none') {
        iDiv[i].style.display = 'initial'; }
     else { iDiv[i].style.display = 'none'; }
  }
}
