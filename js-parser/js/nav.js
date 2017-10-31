$(document).on('change', '#book-select', function(){
  var versions = getBookInfo($(this).val(), function(versions){
    var titleSelect = '';
    var selected;
    for(var t = 0; t < versions.length; t++){
      selected = t === 0 ? ' selected' : '';
      titleSelect += '<option' + selected +' data-mss="' + versions[t].mss.join(',') + '">' + versions[t].title + '</option>';
    }
    $('#version-select').html(titleSelect);
    populateMsSelect(versions[0].mss);
  });
});

$(document).on('change', '#version-select', function(){
  var mss = $(this).find('option:selected').data('mss').split(',');
  populateMsSelect(mss);
});

$(document).on('change', '#ms-select', function(){
  getText($('#book-select').val(), $('#version-select').val(), $('#ms-select').val());
});

function populateMsSelect(mss){
  var selectElHtml = '';
  var selected;
  for(var i = 0; i < mss.length; i++){
    selected = i === 0 ? ' selected' : '';
    selectElHtml += '<option' + selected +'>' + mss[i] + '</option>';
  }
  $('#ms-select').html(selectElHtml);
  getText($('#book-select').val(), $('#version-select').val(), $('#ms-select').val());
}