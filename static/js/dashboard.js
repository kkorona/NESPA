/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

  /*
  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
  */
}())

$(document).ready( function() {
  var file_input_container = $('.js-input-file');
  if (file_input_container[0]) {
      file_input_container.each(function () {
          var that = $(this);
          var fileInput = that.find(".input-file");
          var info = that.find(".input-file__info");

          fileInput.on("change", function () {
              var fileName;
              fileName = $(this).val();

              if (fileName.substring(3,11) == 'fakepath') {
                  fileName = fileName.substring(12);
              }

              if(fileName == "") {
                  info.text("선택된 파일이 없습니다.");
              } else {
                  info.text(fileName);
              }
          })
      });
  }

  /* post와 comment의 모델의 author가 forienkey가 아니므로 무지성 admin 계정 구별 */
  var admin_list = ["조교", "prof","assist"];
  var admin_color = "#AF143C"

  admin_list.forEach((admin_id) => {
    $("td.table_info:nth-child(3)").each((idx, el) => {
        if(el.innerText.indexOf(admin_id)!==-1)
          $(el).css('color',admin_color);
    });
  
    var user_name = $("div.post_info > h5 > span:last-child").text();
    if(user_name.indexOf(admin_id)!==-1)
      $("div.post_info > h5 > span:last-child").html(`<i name="display" class="fa fa-medium"> ` + user_name + `</i>`);

    $("i.fa.fa-user + span").each((idx, el) => {
      if(el.innerText.indexOf(admin_id)!==-1){
        $(el).css('color',admin_color);
        $(el).prev().css('color',admin_color);;
        $(el).prev().addClass("fa-medium");
      }
    });
  });

  $('#moblie-hamburger').click(function() {
    if($('#sidebarMenu').css("display") == "none"){
      $('#sidebarMenu').css("display","block").animate({right : "0"}, 300);
    } else {
      $('#sidebarMenu').animate({right : "-50%"}, 300, function() {
        $('#sidebarMenu').css("display","none");
      });
    }
  });
});


