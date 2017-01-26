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

var url = '';

btPseudoSavePath.addEventListener('click', function(e) {
  btSavePath.click();
});

btSavePath.addEventListener('change', function(e) {
  tbSavePath.value = btSavePath.files[0].path;
  console.log('change')
})

tbUrl.clear = function() {
  this.value = '';
}

tbUrl.set = function(val) {
  this.value = val;
}

containerUrl.addEventListener('dragover', function(e) {
  containerUrl.style.background = 'lightcoral';
  tbUrl.clear();
});

containerUrl.addEventListener('drop', function(e) {
  containerUrl.style.background = 'white';
  tbUrl.style.visibility = 'visible';
});

btSubmit.addEventListener('click', function(e) {
  url = tbUrl.value;
  var savePath = tbSavePath.value;

  if (true) //if (checkInputs(url, savePath))
    callPython(url, savePath);
});


function callPython(url, savePath) {
  var python = pythonBridge();

  python.ex`import sys`;
  python.ex`sys.path.append('.')`;
  python.ex`import wrapper`
  .catch(e => console.log(e));

  python.ex`print('downloading', ${url}, 'and saving to', ${savePath})`
  .catch(e => {});

  python.ex`wrapper.call({'url': ${url},'dir': ${savePath}, 'verbose': ''})`
    .then(x => console.log('return code =', x))
    .catch(e => console.log(e));

  python.end();
}


function checkInputs(url, savePath) {
  return url && savePath;
}
