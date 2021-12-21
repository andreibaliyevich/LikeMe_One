
$(window).on("load", function() {
    if($("div").is(".page-loader")) {
        $(".page-loader").delay(500).fadeOut(800);
    }
});


$(document).ready(function() {
    var $initScope = $("#js-lightgallery");
    if ($initScope.length) {
        $initScope.justifiedGallery({
            border: -1,
            rowHeight: 150,
            margins: 8,
            waitThumbnailsLoad: true,
            randomize: false,
        }).on("jg.complete", function() {
            $initScope.lightGallery({
                thumbnail: true,
                animateThumb: true,
                showThumbByDefault: true,
                preload: 0,
            });
        });
    };
    $initScope.on("onAfterOpen.lg", function(event) {
        $("body").addClass("overflow-hidden");
    });
    $initScope.on("onCloseAfter.lg", function(event) {
        $("body").removeClass("overflow-hidden");
    });
    $initScope.on("onSlideItemLoad.lg", function(event) {
        var gallery = $(this);
        var pr_id = gallery.data("id");

        $.ajax({
            url: "../../photo/view/",
            type: "POST",
            data: { "pr_id": pr_id },

            success : function(json) {
                $("#views-count").text(json.views_count);
            },
        });
    });
});


// photo_like AJAX
function photo_like() {
    var photo_like = $(this);
    var photo_id = photo_like.data("id");
    
    $.ajax({
        url: "../../photo/like/",
        type: "POST",
        data: { "photo_id": photo_id },

        success : function(json) {
            $("#fa-thumbs-up-" + photo_id).toggleClass("far fas text-warning");
            $(".likes-count-" + photo_id).text(json.photo_likes_count);
            $("#likes-count").text(json.likes_count);
        },
    });
};


// photo_share click
function photo_share() {
    javascript:window.open(this.href, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600");
    return false;
}
