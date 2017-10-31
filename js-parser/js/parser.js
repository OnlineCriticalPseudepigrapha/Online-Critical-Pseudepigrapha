var ocp = {
  html: '',
  pathToTexts: '../test/docs/'
};

function getText(b, v, m){
  window.location.hash = b.split('.')[0];
  $('.notes').html('');
  ocp.html = '';
  ocp.ms = m;
  $.get(ocp.pathToTexts + b, function(data){
    xml = $.parseXML(data);
    $xml = $(xml);
    $xml.find('w').remove();
    var title =  $xml.find('book').attr('title');
    var divisions = [];
    $xml.find('version').eq(0).find('divisions').find('division').each(function(){
      divisions.push($(this).attr('label'));
    });
    $('#text').html('<h1>' + title + '</h1>' + getSections($xml.find('version[title="' + v + '"]').find('text'), divisions));
  });
}

function getSections(container, divisions){
  container.find('> [number]').each(function(){
    if($(this).find('> [number]').length === 0){
      ocp.html += getVerses($(this));
    }else{
      var level = $(this).parents('[number]').length;
      ocp.html += '<section><h1>' + divisions[level] + ' ' + $(this).attr('number') + '</h1>';
      getSections($(this), divisions);
      ocp.html += '</section>';
    }
  });
  return ocp.html;
}

function getVerses(verse){
  var textHTML = '<span data-number="' + verse.attr('number') + '">';
  verse.find('reading[mss*=" ' + ocp.ms + ' "], reading[mss^="' + ocp.ms + ' "]').each(function(){
    var hasVariants = $(this).siblings().length > 0;
    if(hasVariants){
      var variants = '';
      $(this).siblings().each(function(i){
        if(i > 0){
          variants += ',';
        }
        variants += '{"ms":"' + $.trim($(this).attr('mss')) + '", "text":"' + $.trim($(this).text()).replace(/'/g, '&apos;') + '"}';
      });
      textHTML += '<a data-variants=\'[' + variants + ']\'>';
    }
    textHTML += $(this).text();
    if(hasVariants){
        textHTML += '</a>';
    }
  });
  textHTML += '</span>';
  return textHTML;
}

function getBookInfo(book, cb){
  $.get(ocp.pathToTexts + book, function(data){
    xml = $.parseXML(data);
    $xml = $(xml);
    var versions = [];
    $xml.find('version').each(function(){
      var $this = $(this);
      var mss = [];
      var title = $this.attr('title');
      var language = $this.attr('language');
      $this.find('manuscripts').find('ms').each(function(){
        mss.push($(this).attr('abbrev'));
      });
      versions.push({title: title, language: language, mss: mss});
    });
    cb(versions);
  });

}