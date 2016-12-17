var stub = {"book": {"title":"Gs", "author":"Bash Gs", "url":"https://chitanka.info/text/1"},
            "recommended":[{"title":"Gs1", "author":"Bash Gs1", "url":"https://chitanka.info/text/2"},
                           {"title":"Gs2", "author":"Bash Gs2", "url":"https://chitanka.info/text/3"}]}

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
    console.log(target_id);
    console.log(url);
    getThumbnail(url, function(result) {
        $(target_id).text('');
        $(target_id).append(result);
    });
    $(target_id).text('please wait');
}

// var getSimilarBooks = function(url, success) {
//     $.get('/get_picture?' + $.param({'url': url}), function(data) {
//         var image = new Image();
//         image.src = 'data:image/png;base64,' + data;
//         success(image);
//     });
// }

var bookInfo = function(bookId, bookJSON) {
    bookCover('#'+ bookId + '-cover', bookJSON.url);
    $('#' + bookId + '-title').text(bookJSON.title);
    $('#' + bookId + '-author').text(bookJSON.author);
    // $('#book-words').text(bookJSON.words);
}

var booksInfo = function(JSON) {
    bookInfo("book", JSON.book);
    console.log(JSON.recommended);                      
    for(var index in JSON.recommended){
        var target_id = "recommended" + index;
        var bookJSON = JSON.recommended[index];
        bookInfo(target_id, bookJSON);
    }
}

$(document).ready(function() {
    $('#get-similar').click(function(){
    var JSON = {"book": {"title":"Gs", "author":"Bash Gs", "url":"https://chitanka.info/text/1"},
            "recommended":[{"title":"Gs1", "author":"Bash Gs1", "url":"https://chitanka.info/text/2"},
                           {"title":"Gs2", "author":"Bash Gs2", "url":"https://chitanka.info/text/17472"}]}
        booksInfo(JSON)
    });
});

