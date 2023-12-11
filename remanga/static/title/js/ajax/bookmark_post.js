class Bookmark_post extends Ajax_post {
    constructor() {
        super();
        
        this.bookmark_button = document.querySelector(".Button_button__JOS9_.Button_button__JOS9_.Button_contained__C0zVd");
        this.title_count_bookmarks = document.querySelector(".title_count_bookmarks");

        const update_data_callback = (response) => {
            this.update_data(response)
        };

        super.Form_submit('.form_bookmark', "bookmark", update_data_callback);     
    }
    
    update_data(response) {
        if (response['is_bookmark_added'])
            this.bookmark_button.innerHTML = "Убрать из списка";
        else
            this.bookmark_button.innerHTML = "Добавить в список";

        this.title_count_bookmarks.innerHTML = response['title_count_bookmarks'];
    }
}