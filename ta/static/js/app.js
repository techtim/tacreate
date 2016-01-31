'use strict';

$(function () {
  $('.carousel').jcarousel({
    list: '.carousel-wrapper',
    vertical: $('.carousel').hasClass('is-vertical')
  });

  $('.carousel-prev').on('jcarouselcontrol:active', function () {
    $(this).removeClass('inactive');
  }).on('jcarouselcontrol:inactive', function () {
    $(this).addClass('inactive');
  }).jcarouselControl({
    target: '-=1'
  });

  $('.carousel-next').on('jcarouselcontrol:active', function () {
    $(this).removeClass('inactive');
  }).on('jcarouselcontrol:inactive', function () {
    $(this).addClass('inactive');
  }).jcarouselControl({
    target: '+=1'
  });
});
//# sourceMappingURL=app.js.map
