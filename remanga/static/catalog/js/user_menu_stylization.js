class User_menu_stylization {
    constructor() {
        this.user_avatar = document.querySelector(".Avatar_avatar__hG0bH");
        this.user_menu = null;

        document.addEventListener('click', (event) => this.toggle_user_menu(event));
        window.addEventListener('resize', this.set_transform_translate);
        window.addEventListener('scroll', () => {
        if (this.user_menu)
            this.user_menu.style.top = `${window.scrollY}px`;
        });
    }

    toggle_user_menu(event) {        
        if (!this.user_menu && this.user_avatar.contains(event.target)) {
            add_user_menu();
            this.set_transform_translate();
            document.querySelector(".user_menu").style.top = `${window.scrollY}px`;
        }
        else if (this.user_menu && !this.user_menu.contains(event.target))
            this.user_menu.remove();

        this.user_menu = document.querySelector(".user_menu");
    }   
    set_transform_translate() {
        const user_menu = document.querySelector(".user_menu");

        if (!user_menu) return;

        const pageWidth = window.innerWidth;
        let user_menu_translate_width = 0;

        if (pageWidth < 1024)
            user_menu_translate_width = 0;
        else if (pageWidth < 1600)
            user_menu_translate_width = -pageWidth / 10;
        else
            user_menu_translate_width = -pageWidth / 72 * 10;;

        user_menu.style.transform = `translate(${user_menu_translate_width}px, 55px)`;
    }           
}