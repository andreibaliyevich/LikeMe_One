$(function () {

    $("#js-upload-photos").click(function () {
        $("#photo-upload").click();
    });

    $("#photo-upload").fileupload({
        dataType: 'json',
        sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */

        start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
            $("#modal-progress").modal("show");
        },

        stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
            $("#modal-progress").modal("hide");
            $("[data-action='photo-available']").click(photo_available);
            $("[data-action='photo-cover']").click(photo_cover);
            $("[data-action='photo-open']").click(photo_open);
        },

        progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({"width": strProgress});
            $(".progress-bar").text(strProgress);
        },

        done: function (e, data) {
            if (data.result.is_valid) {
                $("#gallery").append(
                    "<div id=\"" + data.result.id + "\" class=\"card col-md-4 g-mb-30 mt-1\">" +
                        "<figure id=\"figure-" + data.result.id + "\" class=\"\">" +
                            "<img id=\"img-" + data.result.id + "\" class=\"img-fluid\" src=\"" + data.result.thumbnail_url + "\" data-toggle=\"modal\" data-target=\"#modal-photo\" data-action=\"photo-open\" data-id=\"" + data.result.id + "\">" +
                        "</figure>" +
                    "</div>"
                );

                $("#carousel-photo-items").append(
                    "<div class=\"carousel-item\" id=\"carousel-item-" + data.result.id + "\">" +
                        "<img class=\"img-fluid\" src=\"" + data.result.image_url + "\" style=\"max-height:" + (window.innerHeight - 150) + "px;\">" +

                        "<div class=\"form-group\">" +
                            "<div class=\"form-check\">" +
                                "<input type=\"checkbox\" class=\"form-check-input\" id=\"id_available\" data-action=\"photo-available\" data-id=\"" + data.result.id + "\" checked>" +
                                "<label class=\"form-check-label\" for=\"id_available\">Available</label>" +

                                "<input id=\"cover-{{ photo.id }}\" type=\"radio\" name=\"cover\" data-action=\"photo-cover\" data-id=\"" + data.result.id + "\">" +
                                "<label for=\"cover-" + data.result.id + "\">Cover</label>" +
                            "</div>" +
                        "</div>" +
                    "</div>"
                );
            }
        }

    });

});
