//"use strict";

/*
 * Window object 
 * Javascript objects visibility
 */

window.Array    = Array;
window.Boolean  = Boolean;
window.Date     = Date;
window.Math     = Math;
window.Number   = Number;
window.RegExp   = RegExp;

//window.unescape = unescape;
unescape 	    = window.unescape;
eval		    = window.eval;

window.String       = String;
window.charAt       = String.charAt;
window.charCodeAt   = String.charCodeAt;
window.concat       = String.concat;	
window.fromCharCode = String.fromCharCode;
window.indexOf      = String.indexOf;
window.lastIndexOf  = String.lastIndexOf;
window.match        = String.match;	
window.replace      = String.replace;
window.search       = String.search;
window.slice        = String.slice;
window.split        = String.split;
window.substr       = String.substr;
window.substring    = String.substring;
window.toLowerCase  = String.toLowerCase;
window.toUpperCase  = String.toUpperCase;
window.valueOf      = String.valueOf;

window._Function = Function;
Function = function(code) {
	if (navigator.appName == 'Microsoft Internet Explorer') {
		if (code.indexOf("@cc_on!@") >= 0) {
			code = code.replace("@cc_on!@", "*/!/*");
		}
	}
	return window._Function(code);
}
