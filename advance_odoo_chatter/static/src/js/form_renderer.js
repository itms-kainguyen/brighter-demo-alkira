/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormRenderer } from "@web/views/form/form_renderer";
import { useEffect } from "@odoo/owl";

patch(FormRenderer.prototype, "advance_odoo_chatter.form_renderer", {
  setup() {
    this._super();
    useEffect(() => {
      $(".o_form_view").addClass("o_form_view_chatter");

      var elixir_sidebar = document.getElementsByClassName("sidebar_panel");
      var xxl_form_view = document.getElementsByClassName("o_xxl_form_view ");


      if (elixir_sidebar && elixir_sidebar.length == 0) {

        if (xxl_form_view && xxl_form_view.length > 0) {
          $(".o_main_navbar ").addClass("o_xxl_navbar_chatter");
          $(".o_form_view").addClass("o_xxl_form_chatter");
          $(".o_form_view").removeClass("o_form_view_chatter");
        } else {
          $(".o_main_navbar ").removeClass("o_xxl_navbar_chatter");
        }
      }
    });
  },
});
