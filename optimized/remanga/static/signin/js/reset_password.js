const handler_email_response_callback=data=>{const is_error="detail"in data;exceptions_element.innerHTML=is_error?data["detail"]:"";success_element.innerHTML=is_error?"":data["message"]};function listen_reset_password_link(){document.querySelector(".Reset_password").addEventListener("click",(()=>{const inputs=document.querySelectorAll(".jsx-261496919888b024");const input_email=inputs[0].querySelector("input");convert_signin_to_password_reset(inputs,input_email);listen_button_reset_password(input_email)}))}function convert_signin_to_password_reset(inputs,input_email){const label=document.querySelector(".Typography_h5__8pAxj");const button_span=document.querySelector(".Button_label__jamx3");const links=document.querySelectorAll(".Typography_body2__piveF");const old_button_reset_password=document.querySelector(".Button_button___CisL");const container=document.querySelector(".container");label.innerHTML="Восстановить пароль";inputs[1].remove();input_email.placeholder="Почта";input_email.value="";button_span.innerHTML="Восстановить пароль";for(const link of links)link.remove();const button_reset_password=old_button_reset_password.cloneNode(true);old_button_reset_password.remove();container.appendChild(button_reset_password,input_email)}function listen_button_reset_password(input_email){const button_reset_password=document.querySelector(".Button_button___CisL");const csrf_token=document.getElementsByName("csrfmiddlewaretoken")[0].value;button_reset_password.addEventListener("click",(event=>{const formData=new FormData;formData.append("csrfmiddlewaretoken",csrf_token);formData.append("email",input_email.value);ajax_post.Post_request(event,formData,handler_email_response_callback)}))}