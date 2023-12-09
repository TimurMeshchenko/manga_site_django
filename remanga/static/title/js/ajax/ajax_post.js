class Ajax_post {
    Form_submit(form_class, form_name, update_data_callback) {
        $(form_class).submit((event) => {
            const formData = new FormData($(event.target)[0]);
            const successCallback = (response) => {
                update_data_callback(response)
            };

            formData.append('form_name', form_name);  
            this.Post_request(event, formData, successCallback)
        });
    }

    Post_request(event, formData, successCallback) {
        event.preventDefault();

        $.ajax({
        type: 'POST',
        url: window.location.href,
        data: formData,
        processData: false,
        contentType: false,
        success: successCallback
        });
    }
}