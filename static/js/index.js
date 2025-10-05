window.HELP_IMPROVE_VIDEOJS = false;

var INTERP_BASE = "https://homes.cs.washington.edu/~kpar/nerfies/interpolation/stacked";
var NUM_INTERP_FRAMES = 240;

var interp_images = [];
function preloadInterpolationImages() {
  for (var i = 0; i < NUM_INTERP_FRAMES; i++) {
    var path = INTERP_BASE + '/' + String(i).padStart(6, '0') + '.jpg';
    interp_images[i] = new Image();
    interp_images[i].src = path;
  }
}

function setInterpolationImage(i) {
  var image = interp_images[i];
  image.ondragstart = function () { return false; };
  image.oncontextmenu = function () { return false; };
  $('#interpolation-image-wrapper').empty().append(image);
}


$(document).ready(function () {
  // Check for click events on the navbar burger icon
  $(".navbar-burger").click(function (e) {
    console.log("=== 汉堡菜单被点击了！ ===");
    console.log("点击目标：", e.target);
    console.log("当前事件：", e);

    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");

    console.log("切换后的状态：");
    console.log("navbar-burger是否有is-active类：", $(".navbar-burger").hasClass("is-active"));
    console.log("navbar-menu是否有is-active类：", $(".navbar-menu").hasClass("is-active"));

    // 检查菜单项
    const menuItems = $(".navbar-menu.is-active .navbar-item");
    console.log("找到的菜单项数量：", menuItems.length);
    if (menuItems.length > 0) {
      const menuRect = $(".navbar-menu.is-active").get(0).getBoundingClientRect();
      const itemRect = menuItems.first().get(0).getBoundingClientRect();
      console.log("菜单尺寸：", {
        width: menuRect.width,
        height: menuRect.height,
        top: menuRect.top,
        left: menuRect.left
      });
      console.log("菜单项尺寸：", {
        width: itemRect.width,
        height: itemRect.height,
        top: itemRect.top,
        left: itemRect.left
      });
    }

    // 防止默认行为
    e.preventDefault();
    return false;
  });

  // 添加调试信息
  console.log("页面加载完成，找到的.navbar-burger元素：", $(".navbar-burger").length);
  console.log("找到的.navbar-menu元素：", $(".navbar-menu").length);

  // 检查汉堡按钮定位
  const burger = $(".navbar-burger").first();
  if (burger.length > 0) {
    const rect = burger.get(0).getBoundingClientRect();
    const navbarBrand = $(".navbar-brand");
    const brandRect = navbarBrand.get(0).getBoundingClientRect();
    console.log("汉堡按钮位置：", {
      left: rect.left,
      right: rect.right,
      width: rect.width,
      top: rect.top
    });
    console.log("导航栏位置：", {
      left: brandRect.left,
      right: brandRect.right,
      width: brandRect.width
    });
  }

  var options = {
    slidesToScroll: 1,
    slidesToShow: 5,
    loop: true,
    infinite: true,
    autoplay: false,
    autoplaySpeed: 3000,
  }

  // Initialize all div with carousel class
  var carousels = bulmaCarousel.attach('.carousel', options);

  // Loop on each carousel initialized
  for (var i = 0; i < carousels.length; i++) {
    // Add listener to  event
    carousels[i].on('before:show', state => {
      console.log(state);
    });
  }

  // Access to bulmaCarousel instance of an element
  var element = document.querySelector('#my-element');
  if (element && element.bulmaCarousel) {
    // bulmaCarousel instance is available as element.bulmaCarousel
    element.bulmaCarousel.on('before-show', function (state) {
      console.log(state);
    });
  }

  // preloadInterpolationImages();

  // $('#interpolation-slider').on('input', function(event) {
  //   setInterpolationImage(this.value);
  // });
  // setInterpolationImage(0);
  // $('#interpolation-slider').prop('max', NUM_INTERP_FRAMES - 1);

  // bulmaSlider.attach();

  // Check if video elements exist before setting playback rate
  const singleTaskVideo = document.getElementById("single-task-result-video");
  const multiTaskVideo = document.getElementById("multi-task-result-video");

  if (singleTaskVideo) {
    singleTaskVideo.playbackRate = 2.0;
  }

  if (multiTaskVideo) {
    multiTaskVideo.playbackRate = 2.0;
  }
})

