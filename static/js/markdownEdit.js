/**
 * Created by mhq on 17/1/8.
 */
var markdown_reg = /[\\\`\*\_\[\]\#\+\-\!\>]/g;
$(function () {
    $('.markdown-edit').markdown({
        height:'500',
        language:'zh',
        footer:'字数: <small id="markdown-counter" class="text-success">0</small>',
		onChange:function(e) {
            var content = e.getContent();
            content_length = content.replace(markdown_reg, '').length;
            $('#markdown-counter').html(content_length);
        },
    })
});