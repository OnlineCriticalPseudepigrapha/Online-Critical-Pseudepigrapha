$(document).on('click', '#search-container-button', function(){
  $('body').addClass('search-active');
});

$(document).on('click', '#search-close', function(){
  $('body').removeClass('search-active');
});

$(document).on('click', '.choice-list li', function(){
  var $this = $(this);
  $this.addClass('active');
  $this.siblings().removeClass('active');
});

$(document).on('click', '.ms-choice', function(){
  var $this = $(this);
  var ms = $this.data('ms');
  var $searchExcerpt = $this.closest('.search-result').find('.search-excerpt');
  $searchExcerpt.find('.active').removeClass('active');
  $searchExcerpt.find('[data-ms="' + ms + '"]').addClass('active');
});

$(document).on('click', '.search-alphabet li', function(){
  $this = $(this);
  $('.keyboard').attr('data-lang', $this.attr('data-lang'));
  if($this.attr('data-lang') === 'syriac'){
    $('#search-input').attr('dir', 'rtl');
  }else{
    $('#search-input').attr('dir', 'ltr');
  }
});

$('[data-key] > span > button').each(function(){
  var $this = $(this);
  var hammertime = new Hammer(this);
  hammertime.get('press').set({time: 1000});
  hammertime.on('press', function(ev) {
    $this.closest('[data-key]').addClass('hold');
    $('.search-container').append('<div id="keyboard-hold-overlay"></div>');
  });
});

$(document).on('click', '[data-key]> span > button', function(){
  var $this = $(this);
  var char = $this.text();
  insertAtCaret('search-input', char);
});

$(document).on('click', '.char-alternates button', function(){
  insertAtCaret('search-input', $(this).text());
  $('#keyboard-hold-overlay').remove();
  $(this).closest('[data-key]').removeClass('hold');
});

$(document).on('click', '#keyboard-hold-overlay', function(){
  $('#keyboard-hold-overlay').remove();
  $(this).closest('[data-key]').removeClass('hold');
});

$(document).on('click', '.backspace', function(){
  $('#search-input').backspaceAtCaret();
});

$(document).on('click', '.search-button', function(){
  showResults();
});

function showResults(){
  $('.search-container').find('.panel-heading[aria-expanded="true"]').trigger('click');
  $('.search-results').addClass('active');
}

// https://stackoverflow.com/questions/1064089/inserting-a-text-where-cursor-is-using-javascript-jquery
function insertAtCaret(areaId, text) {
  var txtarea = document.getElementById(areaId);
  var scrollPos = txtarea.scrollTop;
  var caretPos = txtarea.selectionStart;

  var front = (txtarea.value).substring(0, caretPos);
  var back = (txtarea.value).substring(txtarea.selectionEnd, txtarea.value.length);
  txtarea.value = front + text + back;
  caretPos = caretPos + text.length;
  txtarea.selectionStart = caretPos;
  txtarea.selectionEnd = caretPos;
  txtarea.focus();
  txtarea.scrollTop = scrollPos;
}

// https://stackoverflow.com/questions/1735518/how-might-i-simulate-a-backspace-action-in-a-text-field
jQuery.fn.extend({
  backspaceAtCaret: function(dir){
    return this.each(function(i) {
      if (document.selection)
      {
          this.focus();
          sel = document.selection.createRange();
          if(sel.text.length > 0)
          {
              sel.text="";
          }
          else
          {
              sel.moveStart("character",-1);
              sel.text="";
          }
          sel.select();
      }
      else if (this.selectionStart || this.selectionStart == "0")
      {
          var startPos = this.selectionStart;
          var endPos = this.selectionEnd;

          this.value = this.value.substring(0, startPos-1) + this.value.substring(endPos, this.value.length);
          this.selectionStart = startPos-1;
          this.selectionEnd = startPos-1;
          this.focus();
      }
      else
      {
          this.value=this.value.substr(0,(this.value.length-1));
          this.focus();
      }
    })
  }
  });