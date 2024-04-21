class Websockets_comment extends Websockets_title {
    constructor() {
        super();

        this.comment_rating_post = new Comment_rating_post();
        this.textarea_comment_post = document.querySelector(".Input_inputAdornedEnd__5xGz7");
        const form_comment_post = document.querySelector('.form_comment_post');

        form_comment_post.addEventListener('submit', (event) => {
            event.preventDefault();
            this.update_websoket_data()
            super.send_websocket(this.websoket_data)

            this.textarea_comment_post.value = '';
        });
    }

    update_websoket_data() {
        const updated_websoket_data = JSON.parse(this.websoket_data);

        updated_websoket_data.content = this.textarea_comment_post.value;

        this.websoket_data = JSON.stringify(updated_websoket_data);
    }

    update_elements(response) {
        this.add_empty_comment(response);
        
        const comment_created = document.querySelector(".Comments_media__5h5tS");
        const comment_content = comment_created.querySelector('.jsx-918629f30f833e0'); 
        const comment_counter = document.querySelector(".Typography_h4__1eVxk.Typography_gutterBottom__mjtdd");
        const comment_counter_separeted_text = comment_counter.innerText.split(" ");
        const updated_comments_count = Number(comment_counter_separeted_text[1]) + 1;

        comment_content.innerText = response.content;
        comment_counter.innerText = comment_counter_separeted_text[0] + " " + updated_comments_count

        this.add_new_comment_rating_listeners(comment_created, response);
    }

    add_empty_comment(response) {
      const url_profile = `/manga/user/${response.user_id}`; 
      const user_avatar = response.user_avatar
        ? response.user_avatar
        : "/manga/media/users_avatars/no_avatar.jpg";
      const user_name = response.user_name;

      document.querySelector(".Comments_wrap__7NbKY").insertAdjacentHTML('afterbegin', `
          <div class="jsx-3914328852 Comments_media__5h5tS">
            <a href="${ url_profile }">
              <img src="${ user_avatar }" alt="..."
              class="jsx-3914328852 Comments_mediaAvatar__IuIbH" />
            </a>
          <div class="jsx-3914328852 Comments_mediaBody__d6xxB">
              <div class="jsx-3914328852 Comments_mediaContent__KYew0 scoreBorder">
              <div class="jsx-3914328852 Comments_mediaHeading___sytl flex items-center">
                  <a class="Comments_username__BIt0K"
                  href="${ url_profile }">${user_name}
                  </a><small class="jsx-3914328852">· 0 minutes </small>
                  <div class="jsx-3914328852 ml-auto flex items-center">
                  </div>
              </div>
              <div class="jsx-918629f30f833e0">
              </div>
              </div>
              <div class="jsx-3914328852 Comments_footer__4u_24 flex items-center">
              <form method="post" class="comment_like_form">
                  ${csrf_token}
                  <button class="Comments_iconButton__dwH2e" type="submit" name="form_name" value="like_" style="background-color: transparent;border: none;padding: 0;">
                    <svg fill="currentColor" viewBox="0 0 469.333 469.333" class="jsx-83d2bca1a5644a9 jsx-2719031823 SvgIcon_fontSize-small__i__5t Svg_rating">
                      <rect x="0" y="192" width="85.333" height="256" />
                      <path
                        d="M469.333,213.333c0-23.573-19.093-42.667-42.667-42.667h-134.72l20.373-97.493c0.427-2.133,0.747-4.373,0.747-6.72 c0-8.853-3.627-16.853-9.387-22.613l-22.72-22.507l-140.48,140.48C132.8,169.6,128,180.267,128,192v213.333 C128,428.907,147.093,448,170.667,448h192c17.707,0,32.853-10.773,39.253-26.027l64.32-150.4 c1.92-4.907,3.093-10.133,3.093-15.573v-40.853l-0.213-0.213L469.333,213.333z" />
                    </svg>
                  </button>
                  <span class="Comments_score__fxIQG"> 0 </span>
                  <button class="Comments_iconButton__dwH2e" type="submit" name="form_name" value="dislike_"
                  style="background-color: transparent;border: none;padding: 0;">
                    <svg fill="currentColor" viewBox="0 0 469.333 469.333"
                      class="jsx-83d2bca1a5644a9 jsx-2719031823 SvgIcon_fontSize-small__i__5t Svg_rating"
                      style="transform: rotate(180deg);">
                      <rect x="0" y="192" width="85.333" height="256" />
                      <path
                        d="M469.333,213.333c0-23.573-19.093-42.667-42.667-42.667h-134.72l20.373-97.493c0.427-2.133,0.747-4.373,0.747-6.72 c0-8.853-3.627-16.853-9.387-22.613l-22.72-22.507l-140.48,140.48C132.8,169.6,128,180.267,128,192v213.333 C128,428.907,147.093,448,170.667,448h192c17.707,0,32.853-10.773,39.253-26.027l64.32-150.4 c1.92-4.907,3.093-10.133,3.093-15.573v-40.853l-0.213-0.213L469.333,213.333z" />
                    </svg>
                  </button>
              </form>
              </div>
          </div>
          </div>
      `);
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
        
        this.comment_rating_post.first_form_submit(comment_rating_form_class)
    }    
}