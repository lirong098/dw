<template>
  <el-input :class="'dW-date-editor'+id"
            :placeholder="placeholder"
            :value="currentValue"
            :disabled="disabled"
            :icon="value ? 'close':'date'"
            :on-icon-click="value ? iconClose:iconDate ">
  </el-input>
</template>
<script>
  import {formatDate, getWeekNumber} from '../common.js';

  export default {
    name: "date_picker",
    props: {
      format: {
        type: String,
        default: 'Y-m-d'
      },
      position: {
        type: String,
        default: 'bottom'
      },
      starts: {
        type: Number,
        default: 1
      },
      mode: {
        type: String,
        default: 'single'
      },
      placeholder: {
        type: String,
        default: ''
      },
//      readonly: Boolean,
      disabled: Boolean,
//      clearable: {
//        type: Boolean,
//        default: true
//      },
//      editable: {
//        type: Boolean,
//        default: true
//      },
      value: {},
      defaultValue: {},
      showWeek: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        id: parseInt(Math.random() * 1000)
      }
    },

    watch: {},
    computed: {
      currentValue: function () {
        let val = this.value
        if (typeof val !== 'string' && val) {
          val = formatDate(val)
        }
        if ((this.showWeek || this.mode === 'range') && val) {
          val = val + ' (' + getWeekNumber(val) + '周)'
        }
        return val
      },
      displayValue: function () {
        return this.value
      }
    },
    created() {
    },
    methods: {
      iconClose(event) {
        if (this.disabled) {
          event.stopPropagation();
          return
        }
        this.$emit('input', '');
        event.stopPropagation();
      },
      iconDate() {
      },
      datepicker() {
        let that = this;
        $('.dW-date-editor' + this.id).DatePicker({
          date: that.value ? that.value : new Date(),
          current: that.value ? that.value : new Date(),
          mode: this.mode,
          starts: this.starts,
          position: this.position,
          format: this.format,
          onBeforeShow: function () {
            $('.dW-date-editor' + that.id).DatePickerSetDate($('.dW-date-editor' + that.id).children('input').val() ? that.value : '', false);
          },
          onChange: function (formated, dates, week) {
            if (that.mode === 'range') {
              week = getWeekNumber(formated[0])
            } else {
              week = getWeekNumber(formated)
            }
            that.change(formated, dates, week)
            $('.dW-date-editor' + that.id).DatePickerHide();
          }
        });
      },
      change(formated, dates, week) {
        if (this.disabled) return;
        if (!this.showWeek && this.mode != 'range') {
          this.$emit('input', formated);
          this.$emit('change', formated, dates, week);
        } else {
          if (this.mode != 'range') {
            this.$emit('input', formated);
            this.$emit('change', formated, dates, week);
          } else {
            this.$emit('input', formated[0]);
            this.$emit('change', formated[0], dates, week);
          }
        }
      }
    },
    mounted() {
      this.datepicker()
    },
    watch: {}
  };

</script>
