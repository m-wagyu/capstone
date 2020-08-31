var btn = document.getElementById('reload_btn');

window.onload = function(){
  btn.addEventListener('click', function(){
    var req = new XMLHttpRequest();
    req.open('GET','http://localhost:5000/home/?json=True')
    req.onload = function(){
  	var data = JSON.parse(req.responseText);
  	console.log(data[1]);
  }
  });
};