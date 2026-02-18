var _pxId = "";
var _pxRegUrl = "http://pxreg.onlineservicesas.com/pxreg/";
var _pxRegUrlHttps = "https://syndication.prospectxtractor.no/pxreg/";



function _pxReg() {
	var img=new Image(1,1);
	
	if(document.location.protocol != "https:"){
		img.src=_pxRegUrl+"?"+_pxPar();
	}
	else{
		img.src=_pxRegUrlHttps+"?"+_pxPar();
	}

	img.onload=function() { _pxVoid(); }
}






function _pxVoid() { return; }
function _pxPar(){
	var p="";
	if (_pxId != "") { p+="&id="+_pxId; }
	p+="&ref="+escape(_pxRef());
	p+="&dt="+escape(document.title);
	p+="&sr="+screen.width+"x"+screen.height;
	p+="&sd="+screen.colorDepth;
	p+="&fv="+_pxFV();
	p+="&pageUrl="+escape(document.location.href);
	p+="&osas_id="+readID();
	return p;
}
function _pxRef(){
	try{
		if (top.document.referrer){
			return top.document.referrer;
		} else{
			return document.referrer;
		}		
	}
	catch(err){
		return document.referrer;
	}
}
function _pxFV(){
	var f=0,n=navigator;
	if (n.plugins && n.mimeTypes.length) {
		var x=n.plugins["Shockwave Flash"];
		if(x && x.description) {
			var y=x.description;
			f=y.charAt(y.indexOf('.')-1);
		}
	}
	else {
		r=false;
		for(var i=15;i>=3&&r!=true;i-=1){
			execScript('on error resume next: r=IsObject(CreateObject("ShockwaveFlash.ShockwaveFlash.'+i+'"))','VBScript');
			f=i;
		}
	}
	return f;
}




// ** ** START Handle OSAS ID ** **

function readID() {
	var expDays = 365; // number of days the cookie should last
	var expDate = new Date();
	expDate.setTime(expDate.getTime() +  (24 * 60 * 60 * 1000 * expDays));
	var id = GetCookie('osas_id');
	
	if (id == null || id == "no id" || id == "") {
		
		var generated_id = generateId();
		
		id = generated_id;
		
		if (id != GetCookie('osas_id')){
			SetCookie('osas_id', generated_id, expDate);
		}
	}
	
	return id;
}


function getCookieVal (offset) {  
	var endstr = document.cookie.indexOf (";", offset);  
	if (endstr == -1)    
	endstr = document.cookie.length;  
	return unescape(document.cookie.substring(offset, endstr));
}


function GetCookie (name) {  
	var arg = name + "=";  
	var alen = arg.length;  
	var clen = document.cookie.length;  
	var i = 0;  
	while (i < clen) {    
		var j = i + alen;    
		if (document.cookie.substring(i, j) == arg)      
		return getCookieVal (j);    
		i = document.cookie.indexOf(" ", i) + 1;    
		if (i == 0) break;   
	}  
	return null;
}


function SetCookie (name, value) {  
	var argv = SetCookie.arguments;  
	var argc = SetCookie.arguments.length;  
	var expires = (argc > 2) ? argv[2] : null;  
	var path = (argc > 3) ? argv[3] : null;  
	var domain = (argc > 4) ? argv[4] : null;  
	
	var secure = (argc > 5) ? argv[5] : false;  
	document.cookie = name + "=" + escape (value) + 
	((expires == null) ? "" : ("; expires=" + expires.toGMTString())) + 
	((path == null) ? "" : ("; path=" + path)) +  
	((domain == null) ? "" : ("; domain=" + domain)) +    
	((secure == true) ? "; secure" : "");
}


function generateId(){

	var timestamp = new Date().getTime();
	timestamp = timestamp.toString() + "";


	if(timestamp.charAt(0) == '0'){
		timestamp = timestamp.substring(1, timestamp.length);
		timestamp = "1" + timestamp;
	}

	var randomnumber = Math.floor(Math.random()*10);
	var random_temp;
	var return_id = 1;

	for(var i=0;i<4;i++){
		random_temp = Math.floor(Math.random()*10);
		randomnumber = randomnumber + "" + random_temp;
	}

	return_id = timestamp + "" + randomnumber;

	return return_id;
	
}

// ** ** END Handle OSAS ID ** **


