function proxifyUrl(url) {
    return "proxy.php?url=" + encodeURIComponent(url);
}

function unproxifyUrl(url) {
    return decodeURIComponent(url.split("proxy.php?url=")[1]);
}

var jqAjax = $.ajax;
$.ajax = function(settings) {
    if (settings && settings.url) {
        settings.url = proxifyUrl(settings.url);

        var settingsCopy = {
            url: 'api/external/get_link_content',
            complete: settings.complete,
            success: settings.success,
            error: settings.error
        };

        settings.complete = function(jqXHR, textStatus) {
            settingsCopy.complete(jqXHR, textStatus);
        };

        settings.success = function(data, textStatus, jqXHR) {
            settingsCopy.success(data, textStatus, jqXHR);
        };

        settings.error = function(jqXHR, textStatus, errorThrown) {
            settingsCopy.error(jqXHR, textStatus, errorThrown);
        };
    }
    jqAjax(settings);
};
