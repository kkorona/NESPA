$(document).ready( function() {

    $("button.heading.toastui-editor-toolbar-icons").click(() => {
            $('.toastui-editor-popup-add-heading h1').text("H1 24px");
            $('.toastui-editor-popup-add-heading h2').text("H2 22px");
            $('.toastui-editor-popup-add-heading h3').text("H3 20px");
            $('.toastui-editor-popup-add-heading h4').text("H4 18px");
            $('.toastui-editor-popup-add-heading h5').text("H5 16px");
            $('.toastui-editor-popup-add-heading h6').text("H6 14px");
    });
    
    var file = $('input[type="file"]');

    file.on('change', function (e){  
        $("#files-box").find('.upload-name').val(e.target.files[0].name); 
        $("#files-box").find('.upload-name').addClass("uploaded-name");
        $("#files-box").find('.upload-name').removeClass("upload-name");
    });
    
});


function writeArticle() {
    var writeForm = document.write_form;
    var content = editor.getMarkdown();
    writeForm.post_contents.value = content;
    writeForm.submit();
}

