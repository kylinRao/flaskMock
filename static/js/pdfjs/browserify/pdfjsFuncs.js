// Any copyright is dedicated to the Public Domain.
// http://creativecommons.org/licenses/publicdomain/

// Hello world example for browserify.

require('pdfjs-dist');
$ = require("jquery");
console.log("开始获取pdf的url");
var pdfPath = $("#theCanvas").attr("class");
console.log(pdfPath);
var currentPage = 1;
currentPage = parseInt( $("#currentPage").val() );
console.log("当前页面为："+currentPage+" 页");

// Setting worker path to worker bundle.
PDFJS.workerSrc = '/static/js/pdfjs/browserify/pdf.worker.bundle.js';

// It is also possible to disable workers via `PDFJS.disableWorker = true`,
// however that might degrade the UI performance in web browsers.

// Loading a document.
var loadingTask = PDFJS.getDocument(pdfPath);
var doc = loadingTask.promise;
var totalPage;
var pdfInfo;
loadingTask.promise.then(function (doc) {
  //这个函数相当于初始化函数
  //初始化pdf总页数
  totalPage = doc.numPages ;
  $("#totalPage").val(totalPage)
  gotoPage(currentPage);

  console.log("这个pdf一共" +totalPage + "页！");
//////我添加的内容（pdf文档参数信息）
  var lastPromise; // will be used to chain promises
  lastPromise = doc.getMetadata().then(function (data) {
    //初始化pdf的详情信息
    pdfInfo = data.info;
    console.log('# Metadata Is Loaded');
    console.log('## Info');
    console.log(JSON.stringify(data.info, null, 2));
    console.log();
    if (data.metadata) {
      pdfInfo = data.metadata.metadata;

      console.log('## Metadata');
      console.log(JSON.stringify(data.metadata.metadata, null, 2));
      console.log();
    }
  });



}).catch(function (reason) {
  console.error('Error: ' + reason);
});

////html事件响应函数
///下一页事件触发函数
$(document).on('click', "#nextPage", function () {
  console.log("nextPage");
  $(".oneCommet").remove("div");
  currentPage = parseInt( $("#currentPage").val() );
  currentPage = currentPage + 1;
  gotoPage(currentPage);

  getBookPageComments();
});
// 上一页事件触发函数
$(document).on('click', "#prePage", function () {
  console.log("prePage");
  $(".oneCommet").remove("div");
  currentPage = parseInt( $("#currentPage").val() );
  currentPage = currentPage - 1;
  gotoPage(currentPage);

  getBookPageComments();

});
// 当前页码变化事件触发函数
$("#currentPage").change(function () {
    console.log("currentPage change ");
  $(".oneCommet").remove("div");
  currentPage = parseInt( $("#currentPage").val() );
  gotoPage(currentPage);
  getBookPageComments(currentPage);
  $("#currentPage").val(currentPage);
})

/////内部定义函数
function gotoPage(pageNum) {

  if(pageNum < 1){
    currentPage = 1;
    window.alert("没有上一页了");
  }else if (pageNum > totalPage){
    currentPage = totalPage;
    window.alert("没有下一页了");
  }else {
      loadingTask.promise.then(function (doc) {
    return doc.getPage(pageNum).then(function (pdfPage) {

      // Display page on the existing canvas with 100% scale.
      var viewport = pdfPage.getViewport(1.0);
      var canvas = document.getElementById('theCanvas');
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      var ctx = canvas.getContext('2d');
      var renderTask = pdfPage.render({
        canvasContext: ctx,
        viewport: viewport
      });
      $("#currentPage").val(currentPage);
      return renderTask.promise;
    });
  });
  }
};
//提交评论信息函数
function addComment() {
        var url = "/add_comment_json/" + $(".bookId").attr("id") + "/" + currentPage;
        console.log("url:" + url);
        if ("" == $("textarea").val()) {
            alert("评论信息不能为空！");
        }
        else {
            $.ajax({
                url: url,
                type: 'post',
                dateType: 'json',
                data: $("#commentForm").serialize(),
                success: function (data) {
                    console.log(data);
                    console.log(eval(data));
                    //刷新评论区
                    var entry = {};
                    eval(data).forEach(function (entry, index) {
                        console.log(entry);
                        var appendcontent = '<div class="oneCommet">' +
                    '<div class="{0}" style="float: left" >'.format(entry.id) +
                        '<a style="color: black">{0} </a>'.format(entry.comment) +
                    '</div>' +
                    '<div  style="float: none" class="{0}">'.format(entry.id) +
                        '<button class="deleteComment" id = "{0}">delete</button>'.format(entry.id) +
                    '</div></div>';
                        $("#commentsContent").prepend(appendcontent);
                    });
                },
                error: function () {
                    alert("error!");
                }
            });
        }
    }
//删除评论函数
function deleteComment() {
        var commentid = $(this).attr("id");
        var url = "/delete_comment_json/" + commentid;
        console.log("url:" + url);
        $.ajax({
            url: url,
            type: 'post',
            dateType: 'json',
            success: function (data) {
                console.log(data);
                //刷新评论区
                var entry = {};
                $("." + commentid).remove("div");
            },
            error: function () {
                alert("error!");
            }
        });
    }
//查询评论函数
function getBookPageComments(pageNum) {
      if(pageNum < 1){
    currentPage = 1;
    window.alert("你这个页面好远啊，跳不过去啦，就近歇下了");
  }else if (pageNum > totalPage){
    currentPage = totalPage;
    window.alert("你这个页面好远啊，跳不过去啦，就近歇下了");
  }else {


          var url = "/getBookPageComments/" + $(".bookId").attr("id") + "/" + currentPage;
          console.log("url:" + url);
          $.ajax({
              url: url,
              type: 'post',
              dateType: 'json',
              success: function (data) {
                  console.log(data);
                  console.log(eval(data));
                  //刷新评论区
                  var entry = {};
                  eval(data).forEach(function (entry, index) {
                      console.log(entry);
                      var appendcontent = '<div class="oneCommet">' +
                          '<div class="{0}" style="float: left" >'.format(entry.id) +
                          '<a style="color: black">{0} </a>'.format(entry.comment) +
                          '</div>' +
                          '<div  style="float: none" class="{0}">'.format(entry.id) +
                          '<button class="deleteComment" id = "{0}">delete</button>'.format(entry.id) +
                          '</div></div>';
                      $("#commentsContent").prepend(appendcontent);
                  });
              },
              error: function () {
                  alert("error!");
              }
          });
      }



}