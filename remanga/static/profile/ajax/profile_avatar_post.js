class Profile_avatar_post extends Ajax_post {
    constructor() {
        super();
        
        this.fileInput = $('#id_avatar')[0];

        document.querySelector(".relative").addEventListener('click', () =>  this.activate_avatar_uploader());

        this.form_submit("#id_avatar", "avatar");     
    }

    activate_avatar_uploader() {
        document.querySelector("#id_avatar").click();
    }    

    form_submit(form_class, form_name) {
        $(form_class).change((event) => {
            const formData = new FormData($(".form_avatar")[0]);
            const successCallback = (response) => {
                this.update_data()
            };

            formData.append(form_name, this.fileInput.files[0]);  
            super.Post_request(event, formData, successCallback)
        });
    }

    update_data() {
        const imgs_avatar = document.querySelectorAll(".profile-pic");
        const have_not_avatar = imgs_avatar[0].src.includes('no_avatar');

        if (have_not_avatar) {
            const url_splited = window.location.href.split("/");
            const user_id = url_splited[url_splited.length -2]

            for (const img_avatar of imgs_avatar) 
                img_avatar.src = img_avatar.src.split("no_avatar")[0] + user_id + '.jpg';
            
            return
        } 

        const timestamp = new Date().getTime();

        for (const img_avatar of imgs_avatar) 
            img_avatar.src = img_avatar.src.split("?")[0] + "?" + timestamp; 
    }
}