class Title_rating_post extends Ajax_post {
    constructor(title_rating, title_menu_switcher) {
        super();
        
        this._title_rating = title_rating;
        this.title_menu_switcher = title_menu_switcher;
        this.avg_rating = document.querySelector(".title_avg_rating");
        this.rating_count = document.querySelector(".ratingCount");
        this.body = document.querySelector("body");

        this.update_data_callback = (response) => {
            this.update_data(response)
        };
    }
    
    update_data(response) {
        this.avg_rating.innerHTML = Number(response['avg_rating']).toFixed(1);
        this.rating_count.innerHTML = response['count_rating'];
        this._title_rating = response['title_rating'];

        this.title_menu_switcher.remove_rating_menu();
    }

    Form_submit(event) {
        const title_rating_type = this.get_title_rating_type(event.target);
        
        super.Form_submit('.form_title_rating', title_rating_type, this.update_data_callback); 
    }

    get_title_rating_type(target) {
        let button_rating = target;

        if (target.tagName != "BUTTON")
            button_rating = target.tagName == "path" ? button_rating.parentNode.parentNode : button_rating.parentNode;

        return "rating_" + button_rating.querySelector("span").textContent;
    }

    get title_rating() {
        return this._title_rating;
    }

    set title_rating(value) {
        this._title_rating = value;
    }
}