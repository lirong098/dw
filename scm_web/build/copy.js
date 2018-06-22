// var fs = require('fs'); // 引入fs模块
//
// function deleteall(path) {
//   var files = [];
//   if(fs.existsSync(path)) {
//     files = fs.readdirSync(path);
//     files.forEach(function(file, index) {
//       var curPath = path + "/" + file;
//       if(fs.statSync(curPath).isDirectory()) { // recurse
//         deleteall(curPath);
//       } else { // delete file
//         fs.unlinkSync(curPath);
//       }
//     });
//     fs.rmdirSync(path);
//   }
// };
//
// // deleteall("./node_modules/element-ui/lib");
//
// // fs.symlinkSync("./node_modules/element-ui/lib","./statics/lib/element_lib");
//
// if (fs.existsSync("./node_modules/element-ui/newlib")) {
//   fs.rmdirSync("./node_modules/element-ui/newlib");
// }
//
// var path = fs.realpathSync("./statics/lib/element_lib/")
// console.log(path)
//
// fs.renameSync("./node_modules/element-ui/lib", "./node_modules/element-ui/lib1");
// fs.symlinkSync(path, "./node_modules/element-ui/lib", "dir");

var fs = require('fs'); // 引入fs模块

function deleteall(path) {
  var files = [];
  if(fs.existsSync(path)) {
    files = fs.readdirSync(path);
    files.forEach(function(file, index) {
      var curPath = path + "/" + file;
      if(fs.statSync(curPath).isDirectory()) { // recurse
        deleteall(curPath);
      } else { // delete file
        fs.unlinkSync(curPath);
      }
    });
    fs.rmdirSync(path);
  }
};


if (!fs.existsSync("./node_modules/element-ui/lib1")) {
  var path = fs.realpathSync("./statics/lib/element_lib/")
  console.log(path)
  fs.renameSync("./node_modules/element-ui/lib", "./node_modules/element-ui/lib1");
  fs.symlinkSync(path, "./node_modules/element-ui/lib", "dir");
}

