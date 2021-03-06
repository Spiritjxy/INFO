var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {

    // 第一次进入的时候刷新页面
    updateNewsData()

    // 首页分类切换
    $('.menu li').click(function () {
        var clickCid = $(this).attr('data-cid')
        $('.menu li').each(function () {
            $(this).removeClass('active')
        })
        $(this).addClass('active')

        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            updateNewsData()
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            // TODO 判断页数，去更新新闻数据
            // 判断是否正在刷新,没有加载去刷新
            if(!data_querying){
                //进来之后设置成,正在加载
                data_querying = true

                //判断当前页数有没有到总页数
                if(cur_page < total_page){
                    //发送请求加载数据
                    updateNewsData()
                }else{
                    data_querying = false
                }
            }

        }
    })
})

function updateNewsData() {
    // TODO 更新新闻数据
    // 拼接参数
    var params = {
        "page":cur_page,
        "cid":currentCid,
        "per_page":5
    }

    // 发送get请求,获取数据

    $.get('/newslist',params,function (resp) {

        //设置正在加载数据
        data_querying = false

        //判断是否获取成功
        if(resp.errno == "0"){

            //记录总页数
            total_page = resp.data.total_page

            //判断如果是第一页
            //清空原有的数据
            if(cur_page == 1) {$(".list_con").html('');}

            // 改变当前的加载页数
            cur_page += 1

            //显示数据
            for(var i = 0; i<resp.data.news_li.length;i++){

                //取出对象中的内容
                var news = resp.data.news_li[i]

                //拼接一条完整的数据
                var content = '<li>'
                content = content + "<a href='/news/"+ news.id +"' class='news_pic fl'><img src="+news.index_image_url +"></a>"
                content = content + "<a href='/news/" + news.id +"' class='news_title fl'>"+ news.title +"</a>"
                content = content + "<a href='/news/" + news.id +"' class='news_detail fl'>"+ news.digest +"</a>"
                content = content + "<div class=\"author_info fl\">"
                content = content + "<div class='author fl'>"
                content = content + "<img src=\"../../static/news/images/person.png\" alt=\"author\">"
                content = content + "<a href='#'>"+ news.source +"</a>"
                content = content + "</div>"
                content = content + "<div class='time fl'>"+ news.create_time +"</div>"
                content = content + "</div>"
                content = content + "</li>"



                //将一条完整的数据,添加到标签中
                $(".list_con").append(content)
            }

        }

    })


}
