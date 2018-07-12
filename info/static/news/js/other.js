// 解析url中的查询字符串
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(function(){
    // 页面加载完毕，获取新闻列表
    getNewsList(1)

    // TODO 关注当前作者
    $(".focus").click(function () {

    })

    // TODO 取消关注当前作者
    $(".focused").click(function () {

    })
})

// TODO 获取新闻列表
function getNewsList(page) {
    // 截取所有的参数
    var query = decodeQuery()

    // 拼接请求参数
    var params = {
        "p": page,
        "user_id": query["id"]
    }

    // 发送请求
    /*
    $.get("/user/other_news_list", params, function (resp) {

        // 判断请求是否成功
        if (resp.errno == "0") {
            // 先清空原有的数据
            $(".article_list").html("");
            // 拼接数据
            for (var i = 0; i<resp.data.news_list.length; i++) {
                var news = resp.data.news_list[i];
                var html = '<li><a href="/news/'+ news.id +'" target="_blank">' + news.title + '</a><span>' + news.create_time + '</span></li>'
                // 添加数据
                $(".article_list").append(html)
            }

            // 设置页数和总页数
            // 请求成功之后,通过js设置当前页和总页数
            $("#pagination").pagination("setPage", resp.data.current_page, resp.data.total_page);
        }else {
            alert(resp.errmsg)
        }
    })
    */
}
