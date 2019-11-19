//最小页脚高度调节
var contentHeight = document.body.scrollHeight;
var winHeight = window.innerHeight;
if(contentHeight<winHeight){
	$(".myfooter").css({"bottom":"0px","left":"50%", "transform":"translate(-50%, 0)", "position":"fixed", "padding":"0"});
};

//富文本编辑器自适应宽度
$(".django-ckeditor-widget").removeAttr('style');