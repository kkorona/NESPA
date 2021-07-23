$(document).ready( function() {
    // attach files
    $("input[type=file]").change(function () {
        
        var fileInput = document.getElementById("attach_files");
        
        var files = fileInput.files;
        var file;
        var result = "<ul>";
        
        for (var i = 0; i < files.length; i++) {
            
            file = files[i];

            result += "<li>" + (i+1) + ": " + file.name + "</li>\n";
        }
        result += "</ul>";
        document.getElementById("attach_files_list").innerHTML=result;
    });

    // edit heading toolbar pop-up text of toast ui editor
    $("button.heading.toastui-editor-toolbar-icons").click(() => {
            $('.toastui-editor-popup-add-heading h1').text("H1 24px");
            $('.toastui-editor-popup-add-heading h2').text("H2 22px");
            $('.toastui-editor-popup-add-heading h3').text("H3 20px");
            $('.toastui-editor-popup-add-heading h4').text("H4 18px");
            $('.toastui-editor-popup-add-heading h5').text("H5 16px");
            $('.toastui-editor-popup-add-heading h6').text("H6 14px");
    });
});

function writeArticle() {
    var writeForm = document.write_form;
    var content = editor.getMarkdown();
    writeForm.post_contents.value = content;
    writeForm.submit();
}

