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

var bookCover = function(target_id, url) {
    getThumbnail(url, function(result) {
        $(target_id).text('');
        $(target_id).append(result);
    });
    $(target_id).text('please wait');
}

var getSimilarBooks = function(url, success) {
    $.get('/get_picture?' + $.param({'url': url}), function(data) {
        var image = new Image();
        image.src = 'data:image/png;base64,' + data;
        success(image);
    });
}

var bookInfo = function() {
    bookCover('#book-cover', "https://chitanka.info/text/1");
    $('#book-title').text('Черната кула');
    $('#book-author').text('Дейвид Едингс');
    $('#book-words').text('мех, кула')
}

$(document).ready(function() {
    $('#get-book-cover').click(bookCover);
});

$(document).ready(function() {
    $('#get-similar').click(bookInfo);
});

