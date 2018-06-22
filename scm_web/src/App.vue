<template>
  <div id="app">
    <transition><router-view></router-view></transition>
  </div>
</template>

<script>
export default {

}
</script>

<style>
  /*@import "./assets/reset.scss";*/
  /*@import "../statics/css/theme-green/theme_default.css";*/
  @import "./assets/hack.scss";
  @import "../statics/css/main.css";
  /*@import "../statics/css/color-dark.css";     !*深色主题*!*/
  /*@import "../statics/css/theme-green/color-green.css";   !*浅绿色主题*!*/
  @import "../statics/css/theme-pink/color-picker.css";
  @import "./assets/table.css";
  @font-face {
    font-family: 'iconfont';  /* project id 410775 */
    src: url('//at.alicdn.com/t/font_410775_ub1l9lwxqetjfw29.eot');
    src: url('//at.alicdn.com/t/font_410775_ub1l9lwxqetjfw29.eot?#iefix') format('embedded-opentype'),
    url('//at.alicdn.com/t/font_410775_ub1l9lwxqetjfw29.woff') format('woff'),
    url('//at.alicdn.com/t/font_410775_ub1l9lwxqetjfw29.ttf') format('truetype'),
    url('//at.alicdn.com/t/font_410775_ub1l9lwxqetjfw29.svg#iconfont') format('svg');
  }
</style>
