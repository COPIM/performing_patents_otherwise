/*
# @name: main.js
# @creation_date: 2022-09-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @author: Joana Chicau <web@joanachicau.com>
# @purpose: JavaScript functions for various functions
# @acknowledgements:
*/

function hideShowInfo(){
      var iDiv = document.querySelectorAll('.info'), i;
      for (i = 0; i < iDiv.length; ++i) {
      if ( iDiv[i].style.display == 'none') {
        iDiv[i].style.display = 'initial';
        document.querySelector('#notes-operations').style.boxShadow = 'inset 0.1rem 0.1rem 0.5rem var(--color-pink)';
      }
      else { iDiv[i].style.display = 'none';
      document.querySelector('#notes-operations').style.boxShadow = 'initial';
    }
  }
}

function toggleMenu(){
      var iDiv = document.querySelectorAll('.interferences'), i;
      for (i = 0; i < iDiv.length; ++i) {
      if ( iDiv[i].style.display == 'none') {
        iDiv[i].style.display = 'flex';
        document.querySelector('#interfere').style.boxShadow = '0.25rem 0.25rem 0.5rem var(--color-dark)';
      }
      else { iDiv[i].style.display = 'none';
      document.querySelector('#interfere').style.boxShadow = 'initial';
    }
  }
}

function refresh(){
      window.location.reload("Refresh")
}

function highlightSearchTerms(search){
  let search_string = search;
  const search_array = search_string.split(" ");
  for (const term of search_array){
    $("span[class=result-entry]:contains('" + term + "')").html(function(_, html) {
      var replace = "(" + term + ")";
      var re = new RegExp(replace, "g");
      return html.replace(re, '<span class="search_term">$1</span>');
    });
  }
}

function removeRandomTitle() {
  var elts = document.getElementsByClassName("title");
  var RandomSpan = elts[Math.floor(Math.random() * elts.length)];
  RandomSpan.innerHTML = "";
  RandomSpan.style.width = "16rem";
  RandomSpan.style.display = "inline-block";
}

function removeRandomImage() {
  var elts = document.getElementsByClassName("img-fluid");
  var RandomImg = elts[Math.floor(Math.random() * elts.length)];
  RandomImg.remove();
}

// code adapted from w3collective
function readingTime(text) {
  const wpm = 200;
  const words = text.trim().split(/\s+/).length;
  const time = Math.ceil(words / wpm);
  document.getElementById("time").innerText = time;
}
