$(function(){
    let $grid = $('.container').masonry({
        // options
        itemSelector: '.grid-item',
        columnWidth: 20,
        gutter: 10
    });

    $grid.imagesLoaded().progress(function () {
        $grid.masonry('layout');
    });

    let msnry = $grid.data('masonry');
    $grid.infiniteScroll({
        // options
        path: '.pagination__next',
        append: '.grid-item',
        history: false,
        outlayer: msnry
    });
});