NYT_API_CODE = '1737bb22228d4e6da754e533e1496be1';


function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview

    // YOUR CODE GOES HERE!
    var street = $('#street').val();
    var city = $('#city').val();
    var imgUrl = 'http://maps.googleapis.com/maps/api/streetview?size=600x300&location=' + street + ', ' + city;
    var image = '<img class="bgimg" src="'+ imgUrl +'">';
    $body.append(image);


    // load NYT articles
    var url = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
    url += '?' + $.param({
        'q': city | '',
        'api-key': NYT_API_CODE
    });
    $.getJSON(url, function(data) {
        var articles = Array.from(data.response.docs);
        articles.forEach(function (item) {
            var articleElem = '<li class="article">' + 
                '<a href="' + item.web_url + '">NYT Article about '+ city +'</a>' + 
                '<p>'+ item.snippet +'</p>' + 
            '</li>';
            $nytElem.append(articleElem);
        });
    }).error(function(e) {
        $nytHeaderElem.text('The ajax failed');
    });

    // load Wikipedia articles
    var wikiRequestTimeout = setTimeout(function() {
        $wikiElem.text("failed to get wiki data");
    }, 8000);

    var wiki_url = 'https://en.wikifpedia.org/w/api.php?action=opensearch&search="' + city + '"&format=json';
    $.ajax({
        url: wiki_url,
        dataType: 'jsonp',
        success: function (data) {
            var titles = data[1];
            var links = data[3];
            for (var i=0; i < 10; i++) {
                $wikiElem.append(
                    '<li><a href="' + links[i] + '">' + titles[i] + '</a></li>'
                );
            }
            clearTimeout(wikiRequestTimeout);
        }
    });

    return false;
}

$('#form-container').submit(loadData);
