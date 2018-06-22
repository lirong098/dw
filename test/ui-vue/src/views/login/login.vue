<template>
  <div class="login-container">
    <component :is="currentView" @setViews="setViews"></component>
  </div>
</template>

<script>
import loginForm from './login_form.vue'
import registerForm from './register_form.vue'
export default {
  name: 'login',
  components: {
    'login_form': loginForm,
    'register_form': registerForm
  },
  data () {
    return {
      currentView: 'login_form'
    }
  },
  methods: {
    setViews (name) {
      this.currentView = name
    }
  }
}
</script>
<style rel="stylesheet/scss" lang="scss" scoped>
$bg:#2d3a4b;

.login-container {
  width: 100%;
  height: 100%;
  background-color: $bg;
  box-sizing: border-box;
  overflow-y: auto;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
