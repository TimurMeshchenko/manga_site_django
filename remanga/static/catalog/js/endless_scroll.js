class Endless_scroll {
    constructor(num_pages) {
        this.page = 1;

        this.grid = document.querySelector(".grid");
        this.gridPlaceholder = this.grid.querySelector(".gridPlaceholder");

        this.listen_scroll(Number(num_pages));
    }

    listen_scroll(num_pages) {
        window.addEventListener('scroll', () => {
            const is_not_all_titles_loaded = this.page < num_pages;
            
            if (this.is_last_title_scrolled() && is_not_all_titles_loaded)
                this.load_more_titles_post()
        });
    }

    load_more_titles_post() {
        this.page++;
        
        $.ajax({
            url: window.location.href,
            type: 'GET',
            dataType: 'json',
            data: {
                next_page: this.page
            },
            success: (response) => {
                this.gridPlaceholder.insertAdjacentHTML("beforebegin", response.html);
            }
        });
    }

    is_last_title_scrolled() {
      const footer = document.querySelector("footer");
      const all_titles = this.grid.querySelectorAll(".gridItem");
      const last_title = all_titles[all_titles.length - 1];
      const scrolledHeight = window.innerHeight + window.scrollY;
      const height_from_last_title_to_end = last_title.offsetHeight + footer.offsetHeight;
      
      return scrolledHeight + height_from_last_title_to_end >= document.documentElement.scrollHeight;
    }    
}