
// photo_open
function photo_open() {
    var photo_open = $(this);
    var photo_id = photo_open.data("id");

    $(".carousel-item").removeClass("active");
    $("#carousel-item-" + photo_id).addClass("active");
};

// photo_open click
$("[data-action='photo-open']").click(photo_open);


// photo_available AJAX
function photo_available() {
    var photo_available = $(this);
    var photo_id = photo_available.data('id');

    $.ajax({
        url: "../../photo-available/",
        type: "POST",
        data: { "photo_id": photo_id },

        success : function(json) {
            $("#figure-" + photo_id).toggleClass("figure-not-available");
            $("#img-" + photo_id).toggleClass("img-not-available");
        },
    });
};

// photo_available click
$("[data-action='photo-available']").click(photo_available);


// photo_cover AJAX
function photo_cover() {
    var photo_cover = $(this);
    var photo_id = photo_cover.data("id");

    $.ajax({
        url: "../../photo-cover/",
        type: "POST",
        data: { "photo_id": photo_id },

        success : function(json) {
            $(".img-is-cover").removeClass("img-is-cover");
            $("#img-" + photo_id).addClass("img-is-cover");
        },
    });
};

// photo_cover click
$("[data-action='photo-cover']").click(photo_cover);


// shuffle_photos AJAX
function shuffle_photos() {
    var button = $(this);
    var pr_id = button.data("id");

    $.ajax({
        url: "../../shuffle-photos/",
        type: "POST",
        data: { "pr_id": pr_id },

        success : function(json) {
            $("#gallery").empty();
            $("#carousel-photo-items").empty();

            for (let i = 0; i < json.sequence_photos.length; i++) {
                $("#gallery").append(
                    "<div id=\"" + json.sequence_photos[i] + "\" class=\"card col-md-4 g-mb-30 mt-1\">" +
                        "<figure id=\"figure-" + json.sequence_photos[i] + "\" class=\"\">" +
                            "<img id=\"img-" + json.sequence_photos[i] + "\" class=\"img-fluid\" src=\"" + json.thumbnail_url[i] + "\" data-toggle=\"modal\" data-target=\"#modal-photo\" data-action=\"photo-open\" data-id=\"" + json.sequence_photos[i] + "\">" +
                        "</figure>" +
                    "</div>"
                );

                if (!json.is_available[i]) {
                    $("#figure-" + json.sequence_photos[i]).addClass("figure-not-available");
                    $("#img-" + json.sequence_photos[i]).addClass("img-not-available");
                }
                if (json.is_cover[i]) {
                    $("#img-" + json.sequence_photos[i]).addClass("img-is-cover");
                }

                $("#carousel-photo-items").append(
                    "<div class=\"carousel-item\" id=\"carousel-item-" + json.sequence_photos[i] + "\">" +
                        "<img class=\"img-fluid\" src=\"" + json.image_url[i] + "\" style=\"max-height:" + (window.innerHeight - 150) + "px;\">" +

                        "<div class=\"form-group\">" +
                            "<div class=\"form-check\">" +
                                "<input type=\"checkbox\" class=\"form-check-input\" id=\"id_available\" data-action=\"photo-available\" data-id=\"" + json.sequence_photos[i] + "\" checked>" +
                                "<label class=\"form-check-label\" for=\"id_available\">Available</label>" +

                                "<input id=\"cover-{{ photo.id }}\" type=\"radio\" name=\"cover\" data-action=\"photo-cover\" data-id=\"" + json.sequence_photos[i] + "\">" +
                                "<label for=\"cover-" + json.sequence_photos[i] + "\">Cover</label>" +
                            "</div>" +
                        "</div>" +
                    "</div>"
                );
            }

            $("[data-action='photo-available']").click(photo_available);
            $("[data-action='photo-cover']").click(photo_cover);
            $("[data-action='photo-open']").click(photo_open);

        },
    });
};

// shuffle_photos click
$("[data-action='shuffle-photos']").click(shuffle_photos);
