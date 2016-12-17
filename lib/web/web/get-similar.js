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

var bookCover = function() {
    url = $('#url').val();
    getThumbnail(url, function(result) {
        $('#thumb').text('');
        $('#thumb').append(result);
    });
    $('#thumb').text('please wait');
}

var similarBooks = function() {
    $('#selected-book').text('Book title');
}

$(document).ready(function() {
    $('#get-book-cover').click(bookCover);
});

$(document).ready(function() {
    $('#get-similar').click(similarBooks);
});

