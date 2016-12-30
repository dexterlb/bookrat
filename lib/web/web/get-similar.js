var extractThumbnail = function(html) {
    return html;
}

var getThumbnail = function(url, success) {
    var fail = function() {
        var image1 = new Image();
        image1.src = "images/noimg.png";
        success(image1);
    }
    if(url) {
        $.get('get_picture?' + $.param({'url': url}), function(data) {
            if(!data) {
                fail();
            } else {
                var image = new Image();
                image.src = 'data:image/png;base64,' + data;
                success(image);
            }
        });
    }
    else {
        fail();
    }
}

var bookCover = function(target_id, url) {
    getThumbnail(url, function(result) {
        // console.log($(target_id));
        $(target_id).text('');
        // console.log(result);

        $(target_id).append(result);
    });
    $(target_id).text('please wait');
}

var getSimilarBooks = function(title, success) {
    $.get('search?' + $.param({'query': title}), function(data) {
        success(data);
    });
}

var bookInfo = function(section, bookId, bookJSON) {
    var book = document.createElement("div");
    book.className = "book";
    var book_cover = document.createElement("div");
    book_cover.className = "book-cover";
    book_cover.id = bookId + "-cover";
    var img = document.createElement("img");
    img.src = "./images/noimg.png";
    book_cover.appendChild(img);
    bookCover('#'+ bookId + '-cover', bookJSON.url);
    book.appendChild(book_cover);

    var book_info = document.createElement("div");
    book_info.className = "book-info";
    book.appendChild(book_info);

    var book_attrs = document.createElement("ul");
    book_info.appendChild(book_attrs);
    
    if (bookJSON.title) {
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
        if(bookJSON.score) {
        var score = document.createElement("li");
        book_attrs.appendChild(score);

        var score_lable = document.createElement("span");
        score_lable.className = "lable";
        score_lable.appendChild(document.createTextNode("Съвпадения:"));
        score.appendChild(score_lable);
        
        var score_val = document.createElement("span");
        score.className = "text";
        score.appendChild(document.createTextNode(bookJSON.score));
        score.appendChild(score_val);
        }
    }
    else {
        var title = document.createElement("li");
        book_attrs.appendChild(title);
        
        var title_name = document.createElement("span");
        title_name.className = "text";
        title_name.appendChild(document.createTextNode("Все още не сме обработили тази книга."));
        title.appendChild(title_name);
    }
    // put everything in a link
    var link = document.createElement("a");
    link.setAttribute("href",bookJSON.url);
    link.setAttribute("target", "_blank")
    link.appendChild(book);
    

    $("." + section).append(link);
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
    $('#get-similar').click(function(e){
        e.preventDefault();
        var el = $(this);
        el.attr("disabled", "disabled");
        query =  $('#title').val();
        getSimilarBooks(query, function(data) {
            JSON_data = JSON.parse(data);
            booksInfo(JSON_data);
        });
    });
});

$(document).ready(function() {
    $('#title').keydown(function(e) {
        $(".searched-book").empty();
        $(".suggested-books").empty();
        $("#get-similar").removeAttr("disabled");
    })
});
