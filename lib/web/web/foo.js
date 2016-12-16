var extractThumbnail = function(html) {
    return html;
}

var getThumbnail = function(url, success) {
    $.get('/get_picture?' + $.param({'url': url}), function(data) {
        var image = new Image();
        image.src = 'data:image/png;base64,' + data;
        success(image);
    });
}

var get = function() {
    url = $('#url').val();
    getThumbnail(url, function(result) {
        $('#thumb').text('');
        $('#thumb').append(result);
    });
    $('#thumb').text('please wait');
}

$(document).ready(function() {
    $('#get').click(get);
});
