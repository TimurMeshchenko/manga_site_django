class Signup_post extends Ajax_post {
    constructor() {
        super();

        const signup_form_class = ".form";
        const exceptions_element = document.querySelector(".exceptions");

        const update_data_callback = (data) => {
            const is_error = 'detail' in data; 
            
            if (is_error) {
                const errors = data['detail'];
                
                exceptions_element.innerHTML = '';

                for (const [key, value] of Object.entries(errors))
                    exceptions_element.innerHTML = value[0];
            }
            else
                location.reload();
        }

        super.Form_submit(signup_form_class, "signup", update_data_callback);
    }
}