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
        const index_button_highlight = is_description_button_highlighted ? 1 : 0;
        const index_button_unhighlight = is_description_button_highlighted ? 0 : 1;

        chapters_buttons[index_button_highlight].classList.add(button_selected_class);
        chapters_buttons[index_button_unhighlight].classList.remove(button_selected_class);
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
            
            this.add_rating_menu();
            this.highlight_active_rating();
            this.body.style.overflow = "hidden";
        }
    }    

    remove_rating_menu() { 
        const modal_window = document.querySelector(".modal");

        modal_window.remove();
        this.body.style.overflow = null;
    }

    add_rating_menu() {
        document.querySelector("body").insertAdjacentHTML('beforeend', `
        <div data-mui-test="Modal" role="presentation" class="jsx-24297ecd4e1681b6 jsx-3374786578 modal Dialog_root__IWQvZ">
        <div data-test="Backdrop" aria-hidden="true" class="jsx-abc0dc1e74fa3514 jsx-24297ecd4e1681b6 jsx-3374786578 "
            style="background-color: rgba(0, 0, 0, 0.667);"></div>
        <div tabindex="0" data-test="sentinelStart"></div>
        <div class="Dialog_container___8sF_ Dialog_scroll-body__nSP8j" tabindex="-1" style="opacity: 1;">
            <div
            class="jsx-7f4bbfca36e2b46d Dialog_paper__JNmkA Dialog_paperWidth-sm__1kKlh Dialog_paper-scroll-body__eos89 paper rounded">
            <div class="jsx-b4198a5461045988 root">
                <form method="post" class="form_title_rating">
                ${csrf_token}
                <button class="transparent jsx-b4198a5461045988 item" type="submit">
                    <span class="jsx-b4198a5461045988">10</span>
                    <span class="jsx-b4198a5461045988">Эпик вин</span>
                </button>

                <button class="transparent jsx-b4198a5461045988 item" type="submit" name="form_name" value="rating_9">
                <span class="jsx-b4198a5461045988">9</span>
                <span class="jsx-b4198a5461045988">Великолепно</span>
                </button>
                <button class="transparent jsx-b4198a5461045988 item" type="submit" name="form_name" value="rating_8">
                <span class="jsx-b4198a5461045988">8</span> 
                <span class="jsx-b4198a5461045988">Отлично</span>
                </button>
                <button class="transparent jsx-b4198a5461045988 item" type="submit" name="form_name" value="rating_7">
                <span class="jsx-b4198a5461045988">7</span>
                <span class="jsx-b4198a5461045988">Хорошо</span>
                </button>
                <button class="transparent jsx-b4198a5461045988 item" type="submit" name="form_name" value="rating_6">
                <span class="jsx-b4198a5461045988">6</span>
                <span class="jsx-b4198a5461045988">Нормально</span>
                </button>
                <button class="transparent jsx-b4198a5461045988 item" type="submit" name="form_name" value="rating_5">
                <span class="jsx-b4198a5461045988">5</span>
                <span class="jsx-b4198a5461045988">Более-менее</span>
                </button>
                <button class="transparent jsx-b4198a5461045988 item" type="submit" name="form_name" value="rating_4">
                <span class="jsx-b4198a5461045988">4</span>
                <span class="jsx-b4198a5461045988">Плохо</span>
                </button>
                <button class="transparent jsx-b4198a5461045988 item" type="submit" name="form_name" value="rating_3">
                <span class="jsx-b4198a5461045988">3</span>
                <span class="jsx-b4198a5461045988">Очень плохо</span>
                </button>
                <button class="transparent jsx-b4198a5461045988 item" type="submit" name="form_name" value="rating_2">
                <span class="jsx-b4198a5461045988">2</span>
                <span class="jsx-b4198a5461045988">Ужасно</span>
                </button>
                <button class="transparent jsx-b4198a5461045988 item" type="submit" name="form_name" value="rating_1">
                <span class="jsx-b4198a5461045988">1</span>
                <span class="jsx-b4198a5461045988">Хуже некуда</span>
                </button>
                </form>
            </div>
            </div>
        </div>
        <div tabindex="0" data-test="sentinelEnd"></div>
        </div>
        `)
    }

    highlight_active_rating() {
        if (this.title_rating_post.title_rating == "None") return;

        const divs_ratings = document.querySelectorAll(".item");
        const active_rating = divs_ratings[divs_ratings.length - this.title_rating_post.title_rating];

        active_rating.classList.add("itemActive");
    }    
}