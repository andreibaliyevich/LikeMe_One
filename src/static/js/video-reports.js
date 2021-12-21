
// video_report_like AJAX
function video_report_like() {
    var vr_like = $(this);
    var vr_id = vr_like.data("id");

    $.ajax({
        url: "../../video/like/",
        type: "POST",
        data: { "vr_id": vr_id },

        success : function(json) {
            $("#fa-thumbs-up").toggleClass("far fas text-muted text-warning");
            $("#likes-count").text(json.likes_count);
        },
    });
};

// video-report-like click
$("[data-action='video-report-like']").click(video_report_like);
