class Password_post extends Ajax_post {
    constructor() {
        super();

        const change_password_form_class = ".form";
        const exceptions_element = document.querySelector(".exceptions");
        const success_element = document.querySelector(".success");
        const old_password = document.querySelector("#id_old_password");
        const new_password = document.querySelector("#id_new_password1");
        const new_password2 = document.querySelector("#id_new_password2");

        const update_data_callback = (data) => {
            const is_password_changed = "message" in data;

            if (is_password_changed) {
                old_password.value = '';
                new_password.value = '';
                new_password2.value = '';
                exceptions_element.innerHTML = '';
                success_element.innerHTML = data['message'];
            }
            else {
                const errors = data['detail'];

                exceptions_element.innerHTML = '';
                success_element.innerHTML = '';

                for (const [key, value] of Object.entries(errors))
                    exceptions_element.innerHTML += value[0] + "<br>";
            }
        }

        super.Form_submit(change_password_form_class, "password", update_data_callback);
    }
}