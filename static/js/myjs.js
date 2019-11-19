//侧边栏选中变色
$(function(){
	$("ul li").click(function(){
        $("ul li").removeClass("selected");
        $(this).addClass("selected");
        });
	})

//导航栏下拉菜单
$(function(){
	$("a.dropdown-toggle").click(function(){
		$(this).css({"background":"rgba(0,0,0,0)"})
	})
})

// 返回顶部按钮向上滚动、触发
$(function () {
	$('#BackTop').click(function () {
		$('html,body').animate({scrollTop: 0}, 500);
	});
	$(window).scroll(function () {
		if ($(this).scrollTop() > 300) {
			$('#BackTop').fadeIn(300);
		} else {
			$('#BackTop').stop().fadeOut(300);
		}
	}).scroll();
});

//全选
var inputs = document.getElementsByName('cb');
function all_check(){
	var checkFlag = false;
	for(var i=0; i<inputs.length; ++i){
		if(!inputs[i].checked){
          checkFlag = true;
          break;
          }}
	for(let i=0; i<inputs.length; ++i){
        inputs[i].checked = checkFlag;
        }}
        
//反选
function re_check(){
	for(var i=0; i<inputs.length; ++i){
		inputs[i].checked = !inputs[i].checked
        }}
    
//删除选中topic
function confirm_dels(){
    var allcheck = document.getElementsByName("cb");
    var allchecked = [];
    var n = 0;
    for(var i=0; i<allcheck.length; ++i){
    	if(allcheck[i].checked){
    		allchecked[n] = allcheck[i].id;
    		++n;
    	}
    }
    	
    if(allchecked==""){
    	layer.tips("选择为空", "#b1", {tips:[1, 'SteelBlue'], time:1500})
    }else{
    	var a = layer.open({
    		type: 1,
    		skin: 'layui-layer-lan',
            area: ['320px', '200px'],
            title: "提示",
            content: '<div class="text-center" style="margin-top:30px"><p>确定删除所选主题？</p><p>注意：这些主题下的所有文章将会被一同删除</p></div>',
            btn: ['Yes', 'No'],
            yes: function(){
            	var m = 0;
            	for(var j=0; j<allchecked.length; ++j){
            		$.ajax({
            			url: '/del_topic/',
            			type:"POST",
            			data: {"topic_id":allchecked[j]},
            			success:function(e){
            				if(e!="1"){
            					++m;
            				}
            			}
            		})
            	}
            	if(m=="0"){
            		layer.close(a);
            		layer.msg("删除成功！", {time: 800}, function(){
                      parent.location.reload()});
	                }else{
	                  layer.msg("注意：部分主题删除失败！");
	                }
            }
    	})
    }
}
    
//删除单个topic
function confirm_del(topic_name, topic_id){
	//var topic_name = $(the).parents("tr").children("td").eq(1).text();
	var a = layer.open({
		type: 1,
        skin: 'layui-layer-lan',
        area: ['320px', '200px'],
        title: "提示",
        content: '<div class="text-center" style="margin-top:30px"><p>确定删除主题： " ' + topic_name + ' " ？</p><p>注意：该主题下的所有文章将会被一同删除</p></div>',
        btn: ['Yes', 'No'],
        yes: function(){
          $.ajax({
            url: '/del_topic/',
            type:"POST",
            data: {"topic_id":topic_id},
            success: function(e){
            	if(e=="1"){
            		layer.close(a);
            		layer.msg("删除成功！", {time: 800}, function(){
                      parent.location.reload()});
            	}else{
            		layer.msg("删除失败！");
              }
            },
          })
        },
      });
	}
    
//删除条目
function confirm_dele(the, entry_id, entry_title){
    var a = layer.open({
          type: 1,
          skin: 'layui-layer-lan',
          area: ['320px', '200px'],
          title: "提示",
          content: '<div class="text-center" style="margin-top:45px"><p>确定删除文章： " ' + entry_title + ' " ？</p></div>',
          btn: ['Yes', 'No'],
          yes: function(){
            $.ajax({
              url: '/del_entry/',
              type: 'POST',
              data: {"entry_id":entry_id},
              success: function(e){
                if(e=="1"){
                  layer.close(a);
                  layer.msg("删除成功！", {time: 800}, function(){
                	  if($(the).attr("id")=="del_in"){
                		  window.location.href="/entries/";
                	  }else{
                		  window.location.reload()
                	  }
                    });
                }else{
                  layer.msg("删除失败！");
                }
              },
            })
          },
        });
      }

//删除选中entry
function confirm_delse(){
    var allcheck = document.getElementsByName("cb");
    var allchecked = [];
    var n = 0;
    for(var i=0; i<allcheck.length; ++i){
    	if(allcheck[i].checked){
    		allchecked[n] = allcheck[i].id;
    		++n;
    	}
    }
    	
    if(allchecked==""){
    	layer.tips("选择为空", "#b1", {tips:[1, 'SteelBlue'], time:1500})
    }else{
    	var a = layer.open({
    		type: 1,
    		skin: 'layui-layer-lan',
            area: ['320px', '200px'],
            title: "提示",
            content: '<div class="text-center" style="margin-top:47px"><p>确定删除所选文章？</p></div>',
            btn: ['Yes', 'No'],
            yes: function(){
            	var m = 0;
            	for(var j=0; j<allchecked.length; ++j){
            		$.ajax({
            			url: '/del_entry/',
            			type:"POST",
            			data: {"entry_id":allchecked[j]},
            			success:function(e){
            				if(e!="1"){
            					++m;
            				}
            			}
            		})
            	}
            	if(m=="0"){
            		layer.close(a);
            		layer.msg("删除成功！", {time: 800}, function(){
                      parent.location.reload()});
	                }else{
	                  layer.msg("注意：部分文章删除失败！");
	                }
            }
    	})
    }
}

//添加主题
function new_topic(){
	layer.prompt({title:'请输入主题名', formType: 3}, function(text, index){
		layer.close(index);
		$.ajax({
			url: '/new_topic/',
			type: 'POST',
			data: {"text":text},
			success:function(e){
				if(e=="1"){
					window.location.reload()
				}else{
					layer.msg('创建主题失败，请重试！', {time:1000});
				}
			}
		})
	})
}

//重命名主题
function edit_topic(topic_id, topic_name){
	var title_name = '请为主题 " ' + topic_name +' " 输入新的主题名';
	layer.prompt({title:title_name, formType: 3}, function(text, index){
		layer.close(index);
		$.ajax({
			url: '/edit_topic/',
			type: 'POST',
			data: {"text":text, "topic_id":topic_id},
			success:function(e){
				if(e=="1"){
					window.location.reload()
				}else{
					layer.msg('重命名失败，请重试！', {time:1000});
				}
			}
		})
	})
}

//触发多级评论框
function load_ch(comment_id){
	//清空评论框
	$(".on_off").empty();
	//加载外部新评论框
	load_id = '#load_' + comment_id;
	$(load_id).load('/static/html/child_comment_form.html')
}

//点赞功能
function validate_is_like(url, id, likes) {
    // 取出 LocalStorage 中的数据
    let storage = window.localStorage;
    const storage_str_data = storage.getItem("my_blog_data");
    let storage_json_data = JSON.parse(storage_str_data);
    // 若数据不存在，则创建空字典
    if (!storage_json_data) {
        storage_json_data = {}
    };
    // 检查当前文章是否已点赞。是则 status = true
    const status = check_status(storage_json_data, id);
    if (status) {
        layer.msg('已经点过赞了哟~');
        // 点过赞则立即退出函数
        return;
    } else {
        // 用 Jquery 找到点赞数量，并 +1
        $('span#likes_number').text(likes + 1).css('color', 'red');
        $('span#likes_text').css('color', 'red');
    }
    // 用 ajax 向后端发送 post 请求
    $.ajax({
        url: url,
        type: 'POST',
        // post 只是为了做 csrf 校验，因此数据为空
        data: {},
        success: function(result) {
            if (result === '1') {
                // 尝试修改点赞数据
                try {
                    storage_json_data[id] = true;
                } catch (e) {
                    window.localStorage.clear();
                };
                // 将字典转换为字符串，以便存储到 LocalStorage
                const d = JSON.stringify(storage_json_data);
                // 尝试存储点赞数据到 LocalStorage
                try {
                    storage.setItem("my_blog_data", d);
                } catch (e) {
                    // code 22 错误表示 LocalStorage 空间满了
                    if (e.code === 22) {
                        window.localStorage.clear();
                        storage.setItem("my_blog_data", d);
                    }
                };
            }else {
                layer.msg("与服务器通信失败..过一会儿再试试呗~");
            }

        }
    });
};

// 验证点赞状态
function check_status(data, id) {
    // 尝试查询点赞状态
    try {
        if (id in data && data[id]) {
            return true;
        } else {
            return false;
        }
    } catch (e) {
        window.localStorage.clear();
        return false;
    };
};