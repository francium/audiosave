const remote = require('electron').remote;
var pythonBridge = remote.getGlobal('pythonBridge');

var btPseudoSavePath = document.getElementById('btPseudoSavePath');
var btSavePath = document.getElementById('btSavePath');
var btSubmit = document.getElementById('btSubmit');
var tbUrl = document.getElementById('tbUrl');
    //tbUrl.style.visibility = 'hidden';
    tbUrl.style.visibility = 'visible';
var tbSavePath = document.getElementById('tbSavePath');

var containerUrl = document.getElementById('container-url');
var url_drop_label = document.getElementById('url-drop-label');

var url = '';

btPseudoSavePath.addEventListener('click', function(e) {
  btSavePath.click();
});

btSavePath.addEventListener('change', function(e) {
  tbSavePath.value = btSavePath.files[0].path;
})

tbUrl.clear = function() {
  this.value = '';
}

tbUrl.set = function(val) {
  this.value = val;
}

// containerUrl.addEventListener('click', function(e) {
//   if (tbUrl.style.visibility == 'visible') {
//     tbUrl.style.visibility = 'hidden';
//     url_drop_label.style.visibility = 'visible';
//   } else {
//     tbUrl.style.visibility = 'visible';
//     url_drop_label.style.visibility = 'hidden';
//   }
// });

// containerUrl.addEventListener('dragover', function(e) {
//   containerUrl.style.border = '1.5px dashed gray';
//   tbUrl.set('');
//   console.log(url);
// });

// containerUrl.addEventListener('dragleave', function(e) {
//   tbUrl.style.border = 'none';
//   tbUrl.style.display = 'block';
//   containerUrl.style.border = '1.5px dashed gray';
//   console.log(url);
//   tbUrl.set(url);
// });

// containerUrl.addEventListener('drop', function(e) {
//   console.log(e);
//   url = tbUrl.value;
//   console.log(url);
// });

btSubmit.addEventListener('click', function(e) {
  url = tbUrl.value;
  var savePath = tbSavePath.value;

  callPython(url, savePath);
});


function callPython(url, savePath) {
  var python = pythonBridge();

  python.ex`import sys`;
  python.ex`sys.path.append('.')`;
  python.ex`import wrapper`;
  python.ex`print('downloading', ${url}, 'and saving to', ${savePath})`;
  //python.ex`wrapper.call({'url': 'https://youtu.be/Ilz-4mtdpOM', 'verbose': ''})`;
  python.end();
}
