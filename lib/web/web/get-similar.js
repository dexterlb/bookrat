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

var getSimilarBooks = function(title, success) {
    $.get('/search?' + $.param({'query': title}), function(data) {
        success(data);
    });
}

var bookInfo = function(bookId, bookJSON) {
    bookCover('#'+ bookId + '-cover', bookJSON.url);
    $('#' + bookId + '-title').text(bookJSON.title);
    $('#' + bookId + '-author').text(bookJSON.author);
    // $('#book-words').text(bookJSON.words);
}

var booksInfo = function(JSON_data) {
    bookInfo("book", JSON_data.book);                   
    for(var index in JSON_data.recommended){
        var target_id = "recommended" + index;
        var bookJSON = JSON_data.recommended[index];
        bookInfo(target_id, bookJSON);
    }
}

$(document).ready(function() {
    $('#get-similar').click(function(){
        query =  $('#title').val();
        getSimilarBooks(query, function(data) {
            JSON_data = JSON.parse(data);
            booksInfo(JSON_data);
        });
    });
});

