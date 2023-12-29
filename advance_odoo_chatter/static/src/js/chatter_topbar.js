
function followButton() {
  if ($(".sidebar_chatter_bottom").hasClass("follow-btn")) {
    $(".sidebar_chatter_bottom").removeClass("follow-btn");
  } else {
    $(".sidebar_chatter_bottom").addClass("follow-btn");
  }
}

document.addEventListener("click", function (event) {
  var formRenderer = document.querySelector(
    ".o_FormRenderer_chatterContainer "
  );

  if (formRenderer) {
    if (!formRenderer.contains(event.target)) {
      const classesToCheck = [
        "btn-close",
        "o_EmojiView",
        "o_EmojiCategoryView",
        "o_EmojiSearchBarView_searchInput",
      ];

      // Check if the target has any of the specified classes
      const hasAnyClass = event.target && classesToCheck.some((className) =>
        event.target.classList.contains(className)
      );

      if (!hasAnyClass) {
        $(".test-ribbon").removeClass("elixir-theme-footer");
        $(".sidebar_chatter_top").removeClass("chatter_icon_top");
        $(".o_ChatterContainer").removeClass("chatter_shadow");
        $(".o_FormRenderer_chatterContainer").removeClass("chatter_form");
        $(".o_Chatter_scrollPanel").css({ display: "none" });
        $(".messages").css({ display: "none" });
        $(".notes").css({ display: "none" });
        $(".activity-container").css({ display: "none" });
        $(".expand-icon").css({ display: "block" });
        $(".collapse-icon").css({ display: "none" });
        $(".sidebar_chatter_bottom").css({ right: "1rem" });

        $(".o_Composer").addClass("o-composer-hide");

      }
    }
  }
});
