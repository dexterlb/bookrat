var extractThumbnail = function(html) {
    return html;
}

var getThumbnail = function(url, success) {
    if(url) {
        $.get('/get_picture?' + $.param({'url': url}), function(data) {
            var image = new Image();
            image.src = 'data:image/png;base64,' + data;
            success(image);
        });
    }
    else {
        var image1 = new Image();
        image1.src = "logo/noimg.png";
        console.log(image1);
        success(image1);
    }
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

var bookInfo = function(section, bookId, bookJSON) {
    var book = document.createElement("div");
    book.className = "book";

    var book_cover = document.createElement("div");
    book_cover.className = "book-cover";
    book_cover.id = bookId + "-cover";
    bookCover('#'+ bookId + '-cover', bookJSON.url);
    book.appendChild(book_cover);

    var book_info = document.createElement("div");
    book_info.className = "book-info";
    book.appendChild(book_info);

    var book_attrs = document.createElement("ul");
    book_info.appendChild(book_attrs);
    
    // li
    var title = document.createElement("li");
    book_attrs.appendChild(title);

    var title_lable = document.createElement("span");
    title_lable.className = "lable";
    title_lable.appendChild(document.createTextNode("Загалвие:"));
    title.appendChild(title_lable);
    
    var title_name = document.createElement("span");
    title_name.className = "text";
    title_name.appendChild(document.createTextNode(bookJSON.title));
    title.appendChild(title_name);
    // li
    var author = document.createElement("li");
    book_attrs.appendChild(author);

    var author_lable = document.createElement("span");
    author_lable.className = "lable";
    author_lable.appendChild(document.createTextNode("Автор:"));
    author.appendChild(author_lable);
    
    var author_name = document.createElement("span");
    author_name.className = "text";
    author_name.appendChild(document.createTextNode(bookJSON.author));
    author.appendChild(author_name);
    // li
    var words = document.createElement("li");
    book_attrs.appendChild(words);

    var words_lable = document.createElement("span");
    words_lable.className = "words";
    words_lable.appendChild(document.createTextNode("Често срещани думи:"));
    words.appendChild(words_lable);
    
    var friquent_words = document.createElement("span");
    friquent_words.className = "text";
    friquent_words.appendChild(document.createTextNode(bookJSON.words));
    words.appendChild(friquent_words);

    $("#" + section).append(book);
}

var booksInfo = function(JSON_data) {
    bookInfo("searched-book", "book", JSON_data.book);                   
    for(var index in JSON_data.recommended){
        var target_id = "recommended" + index;
        var bookJSON = JSON_data.recommended[index];
        bookInfo("suggested-books", target_id, bookJSON);
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

