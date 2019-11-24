function appendHistory(type, query, uuid) {
    if (query == '' || !uuid) return;
    if (type == 0) {
        // 用户消息
        $('.history').append(`
              <div class="right">
                 <div class="bubble bubble-green">
                   <div class="bubble-avatar"><i class="fas fa-user"></i></div>
                   <p style="text-align: left" id="${uuid}">${query}</p>
                 </div>
              </div>
`);
    } else {
        $('.history').append(`
              <div class="left">
                 <div class="bubble bubble-white">
                   <div class="bubble-avatar"><image src="./static/robot.png" width=32px attr="robot" /></div>
                   <p style="text-align: left" id="${uuid}">${query}</p>
                 </div>
              </div>
`);
    }
//    $("#"+uuid).fadeIn(2000);
    var scrollHeight = $('.history').prop("scrollHeight");
    $('.history').scrollTop(scrollHeight, 500);
}


function getHistory () {
    $.ajax({
        url: '/history',
        type: "GET",
        success: function(res) {
            res = JSON.parse(res);
            if (res.code == 0) {
                historyList = JSON.parse(res.history);
                for (let i=0; i<historyList.length; ++i) {
                    h = historyList[i];
                    // 是否已绘制
                    if (!$('.history').find('#'+h['uuid']).length>0) {
                        appendHistory(h['type'], h['text'], h['uuid']);
                    }
                }
            } else {
                console.error('get history failed!');
            }
        },
        error: function() {
            console.error('get history failed!');
        }
    });
}


$(function() {
    setInterval('getHistory();', 5000);
    $('.CHAT').on('click', function(e) {
        e.preventDefault();
        var query = $('input#query')[0].value;
        $('input#query').val('');
        args = {'query': query}
        $.ajax({
            url: '/chat',
            type: 'POST',
            data: $.param(args),
            success: function(res) {
                var data = JOSN.parse(res);
                if (data.code == 0){
                    console.log('指令发送成功');
                } else{
                    console.error('指令发送失败');
                }
            },
            error: function() {
                console.error('指令发送失败');
            }
        })
    });
});