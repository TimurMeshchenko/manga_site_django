class Comment_post extends Ajax_post {
    constructor(comment_rating_post, user) {
        super();
        
        this.comment_rating_post = comment_rating_post;
        this.textarea_comment_post = document.querySelector(".Input_inputAdornedEnd__5xGz7");

        const update_data_callback = (response) => {
            this.update_data(response)
        };

        super.Form_submit(".form_comment_post", 'comment', update_data_callback);     
    }
    
    update_data(response) {
        add_empty_comment();
    
        const comment_created = document.querySelector(".Comments_media__5h5tS");
        const comment_content = comment_created.querySelector('.jsx-918629f30f833e0'); 
        const comment_counter = document.querySelector(".Typography_h4__1eVxk.Typography_gutterBottom__mjtdd");
        const comment_counter_separeted_text = comment_counter.innerText.split(" ");
        const updated_comments_count = Number(comment_counter_separeted_text[1]) + 1;

        comment_content.innerHTML = this.textarea_comment_post.value;
        comment_counter.innerText = comment_counter_separeted_text[0] + " " + updated_comments_count

        this.add_new_comment_rating_listeners(comment_created, response);
    }

    add_new_comment_rating_listeners(comment_created, response) {
        const comment_rating_form_class = ".comment_like_form";
        const comment_rating_form = comment_created.querySelector(comment_rating_form_class);
        const comment_rating_buttons = comment_created.querySelectorAll("button.Comments_iconButton__dwH2e");

        for (let comment_rating_button of comment_rating_buttons)
            comment_rating_button.value += response["comment_id"];

        comment_rating_form.addEventListener("click", (event) => { 
            this.comment_rating_post.set_comment_rating_element(event) 
        });

        $(comment_rating_form_class).off('submit');
        this.comment_rating_post.Form_submit(comment_rating_form_class)
    }
}