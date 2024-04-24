class Comment_rating_post extends Ajax_post {
    constructor() {
        super();
        
        const comment_rating_form_class = ".comment_like_form";
        this.comment_rating_colors = ['SvgIcon_color-primary__TnNB7', 'SvgIcon_color-secondary__OvK95'];

        $(comment_rating_form_class).click((event) => this.set_comment_rating_element(event));
        this.Form_submit(comment_rating_form_class)

        this.update_data_callback = (response) => {
            this.update_data(response)
        };
    }
    
    set_comment_rating_element(event) {
        let button_comment_rating =  ["path", "rect"].includes(event.target.tagName) ? 
            event.target.parentNode.parentNode : event.target.parentNode;

        button_comment_rating = event.target.tagName == "BUTTON" ? event.target : button_comment_rating;
        this.comment_rating_element = button_comment_rating;
    }

    Form_submit(form_class) {
        $(form_class).submit((event) => this.send_comment_rating(event));
    }

    send_comment_rating(event) {
        const formData = new FormData($(event.target)[0]);

        formData.append('form_name', this.comment_rating_element.value);  
        super.Post_request(event, formData, this.update_data_callback)
    }

    first_form_submit(form_class) {
        document.querySelector(form_class).addEventListener('submit', (event) => this.send_comment_rating(event));
    }

    update_data(response) {
        if (user_id == "None") {
            return (window.location.href = "/manga/signin/");
        }

        const comment_rating_form = this.comment_rating_element.parentNode;
        const comment_score = comment_rating_form.querySelector(".Comments_score__fxIQG");
        const comment_rating_buttons = comment_rating_form.querySelectorAll(".jsx-2719031823.SvgIcon_fontSize-small__i__5t");
        
        comment_score.innerHTML = response['comment_likes'];

        for (let i = 0; i < comment_rating_buttons.length; i++)
            comment_rating_buttons[i].classList.remove(this.comment_rating_colors[i]);

        if (response['comment_rating'] != null) {
            const comment_rating_svg = this.comment_rating_element.querySelector('svg');
            const index_button_comment_rating = this.comment_rating_element.value.includes('dislike') ? 1 : 0;

            comment_rating_svg.classList.add(this.comment_rating_colors[index_button_comment_rating]);
        }
    }
}