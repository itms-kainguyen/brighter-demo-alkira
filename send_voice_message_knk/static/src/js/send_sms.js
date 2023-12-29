/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";
patch(FormController.prototype, "sale_order", {
       setup(){
          this._super.apply();
          this.action = useService("action")
       },
       buttonClicked(){
        console.log("this",this, this.action)
           this.action.doAction({
               type: 'ir.actions.act_window',
               name: 'Send SMS',
               view_mode: 'form',
               views:[[false,"form"]],
               res_model: 'send.sms',
               target: 'new',
               //context: "{'create' : False}",
           })
       }
});
