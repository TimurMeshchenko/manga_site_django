class Comment_input_stylization {
    constructor() {
        this.comment_textarea = document.querySelector(".Input_input__F9Zao");
        this.button_submit_comment = document.querySelector(".Button_button__JOS9_.Button_text__LI0qb.Button_text-primary__NSm_C");
        this.characters_counter = document.querySelector(".Input_formHelperText__EwCsr");

        this.comment_textarea.addEventListener('input', () => this.change_comment_post_state());
    }

    change_comment_post_state() {
        const textarea_length = this.comment_textarea.value.replace(/\s/g, '').length;

        if (textarea_length == 0 || textarea_length > 500)
            this.button_submit_comment.type = 'button'
        else
            this.button_submit_comment.type = 'submit'

        this.comment_textarea.style.height = 'auto';
        this.comment_textarea.style.height = this.comment_textarea.scrollHeight + 'px';

        this.follow_characters_count(textarea_length);
    }

    follow_characters_count(textarea_length) {
        this.characters_counter.innerHTML = textarea_length.toString() +
        this.characters_counter.innerHTML.substring(this.characters_counter.innerHTML.indexOf("/"));

        this.characters_counter.style.color = textarea_length > 500 ? 'red' : null;
    }    
}