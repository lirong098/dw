let getWeekNumber = {
  /**
   * 判断年份是否为润年
   *
   * @param {Number} year
   */
  isLeapYear(year) {
    return (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0);
  },
  /**
   * 获取某一年份的某一月份的天数
   *
   * @param {Number} year
   * @param {Number} month
   */
  getMonthDays(year, month) {
    return [31, null, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month] || (this.isLeapYear(year) ? 29 : 28);
  },
  /**
   * 获取某年的某天是第几周
   * @param {Number} y
   * @param {Number} m
   * @param {Number} d
   * @returns {Number}
   */
  getWeekNumber(y, m, d) {
    var now = new Date(y, m - 1, d),
      year = now.getFullYear(),
      month = now.getMonth(),
      days = now.getDate();
    //那一天是那一年中的第多少天
    for (var i = 0; i < month; i++) {
      days += this.getMonthDays(year, i);
    }
    //那一年第一天是星期几
    var yearFirstDay = new Date(year, 0, 1).getDay() || 7;

    var week = null;
    if (yearFirstDay == 1) {
      week = Math.ceil(days / yearFirstDay);
    } else {
      days -= (7 - yearFirstDay + 1);
      week = Math.ceil(days / 7) + 1;
    }
    return week;
  },


  theWeek(val) {
    var totalDays = 0;
    let now = val
    let years = now.getYear()
    if (years < 1000)
      years += 1900
    let days = new Array(12);
    days[0] = 31;
    days[2] = 31;
    days[3] = 30;
    days[4] = 31;
    days[5] = 30;
    days[6] = 31;
    days[7] = 31;
    days[8] = 30;
    days[9] = 31;
    days[10] = 30;
    days[11] = 31;

    //判断是否为闰年，针对2月的天数进行计算
    if (Math.round(now.getYear() / 4) == now.getYear() / 4) {
      days[1] = 29
    } else {
      days[1] = 28
    }

    if (now.getMonth() == 0) {
      totalDays = totalDays + now.getDate();
    } else {
      var curMonth = now.getMonth();
      for (var count = 1; count <= curMonth; count++) {
        totalDays = totalDays + days[count - 1];
      }
      totalDays = totalDays + now.getDate();
    }
    //得到第几周
    var week = Math.round(totalDays / 7);
    return week;
  }
};
module.exports = getWeekNumber;
