class Title_menu_switcher {
    constructor(title_rating, user_is_authenticated, signin_url) {
        this.title_rating_post = new Title_rating_post(title_rating, this);
        this.body = document.querySelector("body");
        this.rating = document.querySelector(".jsx-7324287667afa997.jsx-2767723650")
        this.user_is_authenticated = user_is_authenticated;
        this.signin_url = signin_url;

        document.addEventListener('click', (event) => this.toggle_menu(event));
    }

    toggle_menu(event) {
        if (this.switch_chapters(event)) return;

        this.toggle_rating_menu(event);
    }

    switch_chapters(event) {
        const button_selected_class = "Tab_selected__952d4";
        const is_switch_chapters = event.target.tagName == "BUTTON" &&
        event.target.className.includes("Button_button__JOS9_ Tab_root__aAqqc") &&
        !event.target.className.includes(button_selected_class);

        if (!is_switch_chapters) return false;

        const chapters_buttons = document.querySelectorAll(
        ".Button_button__JOS9_.Tab_root__aAqqc"
        );

        const description_element = document.querySelector(".px-4.py-2");
        const is_description_button_highlighted = chapters_buttons[0].className.includes(button_selected_class)

        description_element.style.display = description_element.style.display == '' ? "none" : null;
        
        if (is_description_button_highlighted)
            add_chapters_menu(description_element);
        else {
            const chapters_menu = document.querySelector(".px-4.py-2:last-child"); 
            chapters_menu.remove();
        }

        this.highlight_chapter_button(chapters_buttons, button_selected_class, is_description_button_highlighted);

        return true;
    }

    highlight_chapter_button(chapters_buttons, button_selected_class, is_description_button_highlighted) {
        const underline_element = document.querySelector(".jsx-f8919b3175e5971e");
        const index_button_highlight = is_description_button_highlighted ? 1 : 0;
        const index_button_unhighlight = is_description_button_highlighted ? 0 : 1;

        chapters_buttons[index_button_highlight].classList.add(button_selected_class);
        chapters_buttons[index_button_unhighlight].classList.remove(button_selected_class);
        underline_element.style.left = underline_element.style.left  == "0px" ? underline_element.style.width : "0px";
    }    

    toggle_rating_menu(event) {
        const rating_menu = document.querySelector(".jsx-7f4bbfca36e2b46d.Dialog_paper__JNmkA");
        const form_title_rating = document.querySelector(".form_title_rating");
        const is_rating_clicked = form_title_rating && form_title_rating.contains(event.target); 

        if (is_rating_clicked)
            this.title_rating_post.Form_submit(event)
        else if (rating_menu && !rating_menu.contains(event.target))
            this.remove_rating_menu();
        else if (this.rating.contains(event.target)) {
            if (this.user_is_authenticated == "False")
                return window.location.href = this.signin_url;
            
            add_rating_menu();
            this.highlight_active_rating();
            this.body.style.overflow = "hidden";
        }
    }    

    remove_rating_menu() { 
        const modal_window = document.querySelector(".modal");

        modal_window.remove();
        this.body.style.overflow = null;
    }

    highlight_active_rating() {
        if (this.title_rating_post.title_rating == "None") return;

        const divs_ratings = document.querySelectorAll(".item");
        const active_rating = divs_ratings[divs_ratings.length - this.title_rating_post.title_rating];

        active_rating.classList.add("itemActive");
    }    
}