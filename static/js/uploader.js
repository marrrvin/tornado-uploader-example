
var Uploader = function(form, message_box, upload_url, progress_url) {
    if (typeof(form) == 'string') {
        var form = document.getElementById(form)
    }

    if (typeof(message_box) == 'string') {
        var message_box = document.getElementById(message_box)
    }

    this.form = form
    this.message_box = message_box
    this.upload_url = upload_url
    this.progress_url = progress_url

    this._init()
}

Uploader.prototype = {
    _init: function() {
        var that = this

        var id = that._generateId()
        var iframe = that._createIFrame(id)

        that.form.parentNode.appendChild(iframe)

        that.form.addEventListener('submit', function(event) {
            var loaded = false

            that.form.setAttribute('target', iframe.id)
            that.form.setAttribute('action', that.upload_url + '?id=' + id)

            iframe.addEventListener('load', function() {
                loaded = true

                var doc = that._getIFrameDocument(iframe)

                result = JSON.parse(doc.documentElement.textContent)

                console.log(result)

                that.message_box.innerHTML = '<a href="' + result['download_url'] + '">' + 'Скачать' + '</a>'
            })

            that.form.submit();

            var getProgress = function() {
                if (loaded) {
                    clearInterval(intervalId)
                    return false
                }

                var xhr = new XMLHttpRequest();
                xhr.open('GET', that.progress_url + '?id=' + id + '&r=' + Math.random(), true)
                xhr.send();

                xhr.onreadystatechange = function() {
                    if (this.readyState != 4) {
                        return;
                    }

                    if (xhr.status != 200) {
                        console.log(xhr.status + ': ' + xhr.statusText)
                    } else {
                        result = JSON.parse(xhr.responseText)

                        console.log('OK: ' + result['progress']);

                        that.message_box.innerHTML = result['progress'] + '%'
                    }
                }
            }

            var intervalId = setInterval(getProgress, 1000)

            getProgress()

            return false
        })
    },

    _generateId: function() {
        return Math.floor(Math.random() * 99999)
    },

    _createIFrame: function(id) {
        var id = 'uploader_iframe_' + id

        var iframe = document.createElement('iframe')

        iframe.setAttribute('id', id)
        iframe.setAttribute('name', id)
        iframe.setAttribute('src', 'about:blank')
        iframe.setAttribute('style', 'display:none')

        return iframe
    },

    _getIFrameDocument: function(obj) {
        return obj.document || obj.contentDocument || obj.contentWindow.document;
    }
}
