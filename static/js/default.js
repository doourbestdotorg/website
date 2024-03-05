function get_language() {
    var browserLang = navigator.language ? navigator.language : navigator.browserLanguage;
    var defaultBrowserLang = "";
    if (
        browserLang.toLowerCase() === "us" ||
        browserLang.toLowerCase() === "en" ||
        browserLang.toLowerCase() === "en_us"
    ) {
        defaultBrowserLang = "en-US";
    } else {
        defaultBrowserLang = "zh-CN";
    }
    return defaultBrowserLang;
};

function local_datetime(s){
    const d = new Date(s);
    var tz=Intl.DateTimeFormat().resolvedOptions().timeZone;
    const formatter = new Intl.DateTimeFormat(get_language(), {
        timeZone: tz,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
    });
    return formatter.format(d);
}

/**
 * This function is same as PHP's nl2br() with default parameters.
 *
 * @param {string} str Input text
 * @param {boolean} replaceMode Use replace instead of insert
 * @param {boolean} isXhtml Use XHTML 
 * @return {string} Filtered text
 */
function nl2br (str, replaceMode, isXhtml) {
	var breakTag = (isXhtml) ? '<br />' : '<br>';
	var replaceStr = (replaceMode) ? '$1'+ breakTag : '$1'+ breakTag +'$2';
	return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, replaceStr);
}

/**
 * This function inverses text from PHP's nl2br() with default parameters.
 *
 * @param {string} str Input text
 * @param {boolean} replaceMode Use replace instead of insert
 * @return {string} Filtered text
 */
function br2nl (str, replaceMode) {   
	var replaceStr = (replaceMode) ? "\n" : '';
	// Includes <br>, <BR>, <br />, </br>
	return str.replace(/<\s*\/?br\s*[\/]?>/gi, replaceStr);
}

function get_json(data){
    if(typeof(data)!=='object')
        return eval('(' + data + ')');
    else
        return data;
}